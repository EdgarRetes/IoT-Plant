from django.db import models
from django.urls import reverse


class Plant(models.Model):
    specie = models.CharField(max_length=100)
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    max_soil_humidity = models.FloatField()
    min_soil_humidity = models.FloatField()
    max_air_humidity = models.FloatField()
    min_air_humidity = models.FloatField()
    
    def __str__(self):
        return self.specie
    
    
class Sensor(models.Model):
    sensor_type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.sensor_type

class Pot(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    temp_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="temp_sensor_pot")
    soil_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="soil_sensor_pot")
    air_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="air_sensor_pot")
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def __str__(self):
        return  self.name
    
class Data(models.Model):
    lecture = models.FloatField()
    timestamp = models.IntegerField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Data: {self.lecture} at {self.timestamp}"




