from django.db import models

class TempSensor(models.Model):
    value = models.FloatField()
    timestamp = models.IntegerField()
    
    def __str__(self):
        return f"TempSensor: {self.value}°C at {self.timestamp}"