from django.db import models


class CubesensorsData(models.Model):
    sensorId = models.TextField(db_column='SensorId')
    measurementTime = models.DateTimeField(
        db_column='MeasurementTime', primary_key=True)
    temperature = models.IntegerField(
        db_column='Temperature', blank=True, null=True)
    pressure = models.IntegerField(db_column='Pressure', blank=True, null=True)
    humidity = models.IntegerField(db_column='Humidity', blank=True, null=True)
    voc = models.IntegerField(db_column='Voc', blank=True, null=True)
    light = models.IntegerField(db_column='Light', blank=True, null=True)
    noise = models.IntegerField(db_column='Noise', blank=True, null=True)
    battery = models.IntegerField(db_column='Battery', blank=True, null=True)
    cable = models.IntegerField(db_column='Cable', blank=True, null=True)
    vocResistance = models.IntegerField(
        db_column='VocResistance', blank=True, null=True)
    rssi = models.IntegerField(db_column='Rssi', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cubesensors_data'


class OutsideTemperature(models.Model):
    measurementTime = models.DateTimeField(
        db_column='MeasurementTime', blank=True, primary_key=True)
    temperature = models.IntegerField(
        db_column='Temperature', blank=True, null=True)

    class Meta:
        db_table = 'outside_temperature'
