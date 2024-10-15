import adafruit_dht
import board
# from sensor_data.models import SensorData

def read_and_store_sensor_data():
    dht_device = adafruit_dht.DHT11(board.D4)

    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if humidity is not None and temperature is not None:
            # SensorData.objects.create(temperature=temperature, humidity=humidity)
            print(f'Temperature: {temperature}°C, Humidity: {humidity}%')
        else:
            print('Failed to get reading. Try again!')
    except RuntimeError as error:
        print(f"Error reading DHT11: {error}")
    finally:
        dht_device.exit()
