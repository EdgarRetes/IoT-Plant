from django.shortcuts import render, redirect
from .models import *
from .sensor import get_temperature, get_air_humidity, get_soil_humidity

def load_data():
    if not Sensor.objects.exists():
        Sensor.objects.bulk_create([
        Sensor(sensor_type="Temperature"),
        Sensor(sensor_type="Soil Humidity"),
        Sensor(sensor_type="Air Humidity"),
        ])

    if not Plant.objects.exists():
        Plant.objects.bulk_create([
        Plant(specie="Fern", max_temp=30, min_temp=15, max_soil_humidity=70, min_soil_humidity=40, max_air_humidity=80, min_air_humidity=50),
        Plant(specie="Cactus", max_temp=40, min_temp=20, max_soil_humidity=30, min_soil_humidity=10, max_air_humidity=40, min_air_humidity=10),
        ])



def main(request):
    load_data()
    plant_name = None

    if request.method == "POST":
        plant_name = request.POST.get("name")

    temperature = get_temperature()
    temperature_value = temperature['value']
    temp_timestamp = temperature['timestamp']
    
    air_humidity = get_air_humidity()
    air_humidity_value = air_humidity['value']
    air_timestamp = air_humidity['timestamp']
    
    soil_humidity = get_soil_humidity()
    soil_humidity_value = soil_humidity['value']
    soil_timestamp = soil_humidity['timestamp']
    
    Data.objects.bulk_create([
        Data(sensor=Sensor.objects.get(id=1), lecture=temperature_value, timestamp=temp_timestamp),
        Data(sensor=Sensor.objects.get(id=2), lecture=air_humidity_value, timestamp=air_timestamp),
        Data(sensor=Sensor.objects.get(id=3), lecture=soil_humidity_value, timestamp=soil_timestamp),
    ])

    registries = Data.objects.all()
    return render(request, 'main.html', { 'registries': registries, 'plant_name' : plant_name })

    



