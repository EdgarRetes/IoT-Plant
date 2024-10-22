from ubidots import ApiClient

API_TOKEN = 'BBUS-7gy0fmUxQrLjugWyMtslFV1pvT68aF'
api = ApiClient(token=API_TOKEN)

# variables = api.get_variables()
# for variable in variables:
#     print(f"Label: {variable.label}, ID: {variable.id}")

def get_temperature():  
    variable_id = '6716fedd50888d0a565184a4'
    registry = api.get_variable(variable_id)
    return registry.last_value
# print(variable.last_value)

