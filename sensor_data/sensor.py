from ubidots import ApiClient

API_TOKEN = 'BBUS-7gy0fmUxQrLjugWyMtslFV1pvT68aF'
api = ApiClient(token=API_TOKEN)

# variables = api.get_variables()
# for variable in variables:
#     print(f"Label: {variable.label}, ID: {variable.id}")

def get_temperature():  
    temp_id = '6716fedd50888d0a565184a4'
    temp = api.get_variable(temp_id)
    return temp.last_value

def get_soil_humidity():  
    soil_id = '6716fedd26764b0ac9e53f6b'
    soil = api.get_variable(soil_id)
    return soil.last_value

def get_air_humidity():  
    air_id = '6716fedd5596a50c7c6a029d'
    air = api.get_variable(air_id)
    return air.last_value

