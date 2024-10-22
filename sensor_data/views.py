from django.shortcuts import render
from .models import TempSensor
from .sensor import *

def main(request):
    
    temperature = get_temperature()
    temperature_value = temperature['value'] 
    timestamp = temperature['timestamp'] 

    new_registry = TempSensor(value=temperature_value, timestamp=timestamp)
    new_registry.save()
    
    registries = TempSensor.objects.all()
    return render(request, 'main.html', {'registries': registries})