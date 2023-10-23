import requests
import json
import psycopg2
from conect import conexion
class MakeApiCall:
    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
    def get_user_data(self, api, parameters):
        response = requests.get(f"{api}", params=parameters)
        if response.status_code == 200:
            print("sucessfully fetched the data with parameters provided")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
    def formatted_print(self, obj):
        
        try:
            with conexion.cursor() as cursor:
                i=1
                for pais in obj:
                    codigo=pais['cca2']
                    nombre=pais['name']['common']
                    print(codigo)
                    country = "INSERT INTO country(id, code) VALUES (%s,%s);"
                    # Podemos llamar muchas veces a .execute con datos distintos
                    cursor.execute(country, (i,codigo,))
                    country_translation = "INSERT INTO country_translation(id, name, language_id, country_id) VALUES (%s,%s,%s,%s);"
                    cursor.execute(country_translation, (i,nombre,None,i,))
                    
                    i += 1
                    conexion.commit()  # Si no haces commit, los cambios no se guardan

        except psycopg2.Error as e:
            print("Ocurrió un error al insertar: ", e)
        finally:
            conexion.close()    


    def __init__(self, api):
        # self.get_data(api)
        parameters = {
            "username": "kedark"
        }
        self.get_user_data(api, parameters)

if __name__ == "__main__":
    api_call = MakeApiCall("https://restcountries.com/v3.1/all")
         