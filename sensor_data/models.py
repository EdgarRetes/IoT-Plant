from django.db import models
from django.urls import reverse

class TempSensor(models.Model):
    value = models.FloatField()
    timestamp = models.IntegerField()
    
    def __str__(self):
        return f"TempSensor: {self.value}°C at {self.timestamp}"




