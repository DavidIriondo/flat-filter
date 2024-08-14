import json
import requests
from urllib.parse import urlencode

from services.scrapy_modules.scrapy_base import ScrapyBase
from dtos.flat import Flat

class FotoCasa(ScrapyBase):

    def start_scrapy_process(self, rules, filters):

        #Construimos la url y los headers
        url = self.build_url(filters)
        headers = self.build_headers()
        flat_list = []
        invalid_flat_list = []
        
        """
        response = requests.get(url, headers=headers)
        real_states = response.json()
        """

        #Leemos de un archivo local
        with open("../fotocasa.json", 'r', encoding='utf-8') as file:
            # Read the entire file content
            json_content = file.read()
            real_states = json.loads(json_content)
        
        #Obtenemos la informacion del json
        json_flat_list = real_states["realEstates"]
        
        #Sin aplicar las reglas
        """
        for element in json_flat_list:
             flat_list.append(self.retrieve_elements(element))
        """

        #Aplicando las reglas
        for element in json_flat_list:
            flat = self.retrieve_elements(element)
            #Solo si el contenido cumple las reglas se añade a la lista final
            if self.apply_rules(rules, flat):
                flat_list.append(flat)
            else:
                invalid_flat_list.append(flat)
        
        
        return flat_list

    def retrieve_elements(self, element):
        flat = Flat()
    
        # Valor predeterminado para los campos en caso de excepción
        valor_predeterminado = "No especificado"
        
        # Asignar 'origin' directamente
        flat.origin = "Foto casa"
        
        # Asignar 'address' con manejo de errores
        try:
            flat.address = f"{element['address']['ubication']}-{element['address']['location']['level5']}"
        except KeyError:
            flat.address = valor_predeterminado

        # Asignar 'description' con manejo de errores
        try:
            flat.description = element['description']
        except KeyError:
            flat.description = valor_predeterminado

        # Asignar 'rooms' con manejo de errores
        try:
            for feature in element['features']:
                if feature['key'] == 'rooms' and feature['value']:
                    flat.rooms = feature['value'][0]
                    break
        except (KeyError, IndexError):
            flat.rooms = valor_predeterminado

        # Asignar 'price' con manejo de errores
        try:
            flat.price = element['transactions'][0]['value'][0]
        except (KeyError, IndexError):
            flat.price = valor_predeterminado

        # Asignar 'original_link' con manejo de errores
        try:
            flat.original_link = f"https://www.fotocasa.es{element['detail']['es']}?from=list"
        except KeyError:
            flat.original_link = valor_predeterminado

        # Asignar 'image_link' con manejo de errores
        try:
            flat.image_link = element['multimedias'][0]['url']
        except (KeyError, IndexError):
            flat.image_link = valor_predeterminado

        return flat

    def build_url(self, filters):
        province = filters["province"] #valor por defecto es 'malaga'
        municipality = filters["municipality"] #valor por defecto es 'fuengirola'
        min_price = filters["min_price"] #valor por defecto es '100'
        max_price = filters["max_price"] #valor por defecto es '900'
        room_numbers = filters["room_numbers"] 

        # Base URL de Fotocasa
        base_url = 'https://web.gw.fotocasa.es/v2/propertysearch/search'

        # Parámetros dinámicos
        params = {
            'combinedLocationIds': '724,1,29,322,559,29054,0,0,0',
            'culture': 'es-ES',
            'includePurchaseTypeFacets': 'true',
            'isMap': 'false',
            'isNewConstructionPromotions': 'false',
            'maxPrice': max_price,
            'minPrice': min_price,
            'minRooms': room_numbers,
            'platformId': '1',
            'propertyTypeId': '2',  # 2 generalmente corresponde a apartamentos
            'sortOrderDesc': 'true',
            'sortType': 'scoring',
            'transactionTypeId': '3'  # 3 generalmente corresponde a alquileres
        }

        # Convertir parámetros a cadena de consulta
        query_string = urlencode(params, doseq=True)

        # Construir la URL completa
        url = f"{base_url}?{query_string}"
        return url
    
    def build_headers(self):
        # Headers de la solicitud
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'es-BO,es-419;q=0.9,es;q=0.8,en;q=0.7',
            'origin': 'https://www.fotocasa.es',
            'priority': 'u=1, i',
            'referer': 'https://www.fotocasa.es/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }

        return headers