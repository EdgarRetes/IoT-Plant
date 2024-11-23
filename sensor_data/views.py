from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Sensor, Plant, Data, Pot
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
            Plant(specie="Swiss Cheese Plant", max_temp=29, min_temp=18, max_soil_humidity=50, min_soil_humidity=70, max_air_humidity=60, min_air_humidity=40),
            Plant(specie="Rubber Plant", max_temp=29, min_temp=16, max_soil_humidity=40, min_soil_humidity=30, max_air_humidity=50, min_air_humidity=40),
            Plant(specie="Snake Plant", max_temp=29, min_temp=13, max_soil_humidity=20, min_soil_humidity=10, max_air_humidity=40, min_air_humidity=30),
            Plant(specie="Photos", max_temp=29, min_temp=19, max_soil_humidity=40, min_soil_humidity=30, max_air_humidity=60, min_air_humidity=40),
            Plant(specie="Dracaena", max_temp=27, min_temp=18, max_soil_humidity=40, min_soil_humidity=30, max_air_humidity=60, min_air_humidity=40),
            Plant(specie="Peace Lily", max_temp=27, min_temp=18, max_soil_humidity=60, min_soil_humidity=50, max_air_humidity=70, min_air_humidity=50),
        ])
    
    if not Pot.objects.exists():
       if not Pot.objects.exists():
        default_plant = Plant.objects.first()  
        temp_sensor = Sensor.objects.get(id=1)  
        soil_sensor = Sensor.objects.get(id=2) 
        air_sensor = Sensor.objects.get(id=3) 
        default_plant = Plant.objects.first() 
        Pot.objects.bulk_create([
            Pot(plant=default_plant, temp_sensor=temp_sensor, soil_sensor=soil_sensor, air_sensor=air_sensor)  
        ])

def main(request):
    load_data()   

    if request.method == 'POST':
        pot = Pot.objects.first()
        if request.POST.get('selected_color'):
            pot.color = request.POST.get('selected_color')
            pot.save()
        if request.POST.get('selected_plant'):
            pot.plant = Plant.objects.get(id=request.POST.get('selected_plant'))
            pot.save()
        if request.POST.get('selected_name'):
            pot.name = request.POST.get('selected_name')
            pot.save()
     



    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        temperature = get_temperature()
        air_humidity = get_air_humidity()
        soil_humidity = get_soil_humidity()

        Data.objects.bulk_create([
            Data(sensor=Sensor.objects.get(sensor_type="Temperature"), lecture=temperature['value'], timestamp=temperature['timestamp']),
            Data(sensor=Sensor.objects.get(sensor_type="Air Humidity"), lecture=air_humidity['value'], timestamp=air_humidity['timestamp']),
            Data(sensor=Sensor.objects.get(sensor_type="Soil Humidity"), lecture=soil_humidity['value'], timestamp=soil_humidity['timestamp']),
        ])
        
        latest_data = Data.objects.order_by('-timestamp')[:3]
        return JsonResponse({
            'temperature': latest_data[0].lecture,  
            'air_humidity': latest_data[1].lecture, 
            'soil_humidity': latest_data[2].lecture,  
            'timestamp': latest_data[0].timestamp
        })

    registries = Data.objects.all()
    plants = Plant.objects.all()
    pot = Pot.objects.get(id=1)

    return render(request, 'main.html', { 
        'registries': registries, 
        'plant_name': pot.name, 
        'plants': plants,
        'selected_color': pot.color, 
        'selected_plant' : pot.plant.id,
    })
