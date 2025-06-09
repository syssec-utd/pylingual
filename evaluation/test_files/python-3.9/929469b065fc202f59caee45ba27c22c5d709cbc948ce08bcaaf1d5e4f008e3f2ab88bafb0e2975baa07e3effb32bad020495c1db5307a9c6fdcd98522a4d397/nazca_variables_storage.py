from nazca4sdk.datahandling.nazcavariables.nazca_variable import NazcaVariables, NazcaVariable
from nazca4sdk.datahandling.open_data_client import OpenDataClient

class NazcaVariablesStorage:

    def __init__(self, https=True):
        self.__openData = OpenDataClient(https)

    def read_variables(self):
        response = self.__openData.read_nazca_variables()
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print('Read nazca variable failure')
                return None
            variables_list = NazcaVariables.parse_raw(response.content)
            return variables_list.variables()
        print('Read nazca variables error')
        return None

    def read_variable(self, identifier: str):
        response = self.__openData.read_nazca_variable(identifier)
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print('Read nazca variable failure')
                return None
            variable = NazcaVariable.parse_raw(response.content)
            return variable
        if response.status_code == 404:
            print(f'Nazca variable {identifier} not found')
            return None
        print(f'Read nazca variable {identifier} error')
        return None