from django.test import TestCase
from temperatures.models import CubesensorsData, OutsideTemperature
from datetime import timedelta
from django.utils import timezone
from temperatures.views import SummaryView, DiffView


class CubesensorsDataTest(TestCase):
    def setUp(self):
        CubesensorsData.objects.create(
            sensorId="1", temperature=100, measurementTime=timezone.now()).save()
        CubesensorsData.objects.create(
            sensorId="1", temperature=200, measurementTime=timezone.now() + timedelta(hours=1)).save()
        CubesensorsData.objects.create(
            sensorId="3", temperature=300, measurementTime=timezone.now()).save()

        OutsideTemperature.objects.create(
            measurementTime=timezone.now(), temperature=400).save()
        OutsideTemperature.objects.create(
            measurementTime=timezone.now() - timedelta(hours=1), temperature=500).save()

    def test_aggregation_is_correct(self):
        response = SummaryView.get_grouped_data(self)
        self.assertEqual(response,
                         [{'sensorId': '1', "count": 2, "avgTemp": 1.5},
                          {'sensorId': '3', "count": 1, "avgTemp": 3.0}])

    def test_outside_temp_cache(self):
        response = DiffView.should_fetch_data(self,
                                              OutsideTemperature.objects.get(temperature=400))
        self.assertFalse(response)
        response = DiffView.should_fetch_data(self,
                                              OutsideTemperature.objects.get(temperature=500))
        self.assertTrue(response)
