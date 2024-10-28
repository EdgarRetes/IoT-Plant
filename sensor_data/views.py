from django.shortcuts import render
from .models import TempSensor
from .sensor import get_temperature  # Import get_temperature function

def main(request):
    # Get the latest temperature data
    temperature = get_temperature()
    temperature_value = temperature['value']
    timestamp = temperature['timestamp']

    # Save to the database
    new_registry = TempSensor(value=temperature_value, timestamp=timestamp)
    new_registry.save()

    # Get all temperature records
    registries = TempSensor.objects.all()
    return render(request, 'main.html', {'registries': registries})
