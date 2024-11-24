# Generated by Django 5.1.2 on 2024-11-23 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specie', models.CharField(max_length=100)),
                ('max_temp', models.FloatField()),
                ('min_temp', models.FloatField()),
                ('max_soil_humidity', models.FloatField()),
                ('min_soil_humidity', models.FloatField()),
                ('max_air_humidity', models.FloatField()),
                ('min_air_humidity', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensor_data.plant')),
                ('air_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='air_sensor_pot', to='sensor_data.sensor')),
                ('soil_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soil_sensor_pot', to='sensor_data.sensor')),
                ('temp_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_sensor_pot', to='sensor_data.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture', models.FloatField()),
                ('timestamp', models.IntegerField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensor_data.sensor')),
            ],
        ),
    ]
