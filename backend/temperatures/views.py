from django.shortcuts import render
from django.db.models import Avg, Count
from temperatures.models import CubesensorsData, OutsideTemperature
from django.http import JsonResponse
from django.views.generic import View
from bs4 import BeautifulSoup
from datetime import timedelta
from django.utils import timezone
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG)


class AllowCORSMixin(object):
    """Mixin to allow CORS. As front is not served via a webserver, this must be done. 
        Otherwise we could just allow access to our own domain"""

    def add_access_control_headers(self, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


class DiffView(AllowCORSMixin, View):
    def get_weather_data(self, user_agent):
        """Returns current Helsinki temperature - if fails, returns None"""
        try:
            response = requests.get(
                "http://wttr.in/Helsinki", headers={'User-Agent': user_agent})
            soup = BeautifulSoup(response.text, features="html.parser")
            temp = int(soup.find("span", {"class": "ef046"}).text) * 100
            outside_data = OutsideTemperature.objects.create(
                measurementTime=timezone.now(), temperature=temp)
            outside_data.save()
            return outside_data
        except Exception as exc:
            logger.warning("Data couldn't be queried! ", exc)
            return None

    def should_fetch_data(self, outside_data):
        return not outside_data or outside_data.measurementTime < timezone.now() - \
            timedelta(minutes=1)

    def get(self, *args, **kwargs):
        """Returns a temperature difference between internet data and recorded data"""
        id = self.kwargs['id']
        sensor_data = CubesensorsData.objects.filter(
            sensorId=id).order_by('-measurementTime').first()
        outside_data = OutsideTemperature.objects.order_by(
            '-measurementTime').first()
        if self.should_fetch_data(outside_data):
            logging.debug("Fetching new data!")
            outside_data = self.get_weather_data(
                args[0].META['HTTP_USER_AGENT'])
        # Display sensor data if web data unavailable
        temp = outside_data.temperature if outside_data else 0
        response = JsonResponse(
            {'difference': (sensor_data.temperature - temp) / 100})
        self.add_access_control_headers(response)
        return response


class SummaryView(AllowCORSMixin, View):
    def get_grouped_data(self):
        """Groups the data by sensorId and aggregates averages and counts"""
        qs = CubesensorsData.objects.values(
            "sensorId").annotate(Count("temperature"), Avg("temperature"))
        return [{"sensorId": x['sensorId'],
                 "count": x['temperature__count'],
                 "avgTemp": x['temperature__avg'] / 100} for x in qs]

    def get(self, *args, **kwargs):
        """Returns a list of sensors and their reading counts and averages"""
        json = self.get_grouped_data()
        response = JsonResponse(
            {'sensors': json})
        self.add_access_control_headers(response)
        return response
