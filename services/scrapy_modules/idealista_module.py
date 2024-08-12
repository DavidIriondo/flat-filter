import re
import html
import json
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import requests

from services.scrapy_modules.scrapy_base import ScrapyBase
from dtos.flat import Flat


class Idealista(ScrapyBase):

    def start_scrapy_process(self, rules, filters):

        #Construimos la url y los headers
        url = self.build_url(filters)
        headers = self.build_headers()
        flat_list = []
        invalid_flat_list = []
        
        # Realizar la solicitud GET
        """
        response = requests.get(url, headers=headers)

        #Obtenemos la info de los pisos y decodificamos la informacion a utf-8
        content = response.content
        decode_content = content.decode("utf-8")

        #Mapeamos a json la respuesta
        json_response = json.loads(decode_content.strip())

        #Obtenemos la parte que nos hace falta
        html_content = json_response["plainText"]
        """
        
        # Open the file in read mode ('r')
        with open("../idealista.html", 'r', encoding='utf-8') as file:
                # Read the entire file content
                html_content = file.read()
        
        #Scrapeamos el contenido html
        soup = BeautifulSoup(html.unescape(html_content), "lxml")
        article_elements = soup.find_all("article", class_="item-multimedia-container")

        #Obtenemos objetos flat del html
        """
        #Sin aplicar las reglas
        for article in article_elements:
             flat_list.append(self.retrieve_elements(article))
        """

        #Aplicando las reglas
        for article in article_elements:
            flat = self.retrieve_elements(article)
            #Solo si el contenido cumple las reglas se añade a la lista final
            if self.apply_rules(rules, flat):
                flat_list.append(flat)
            else:
                invalid_flat_list.append(flat)
             
        return flat_list
    
    def retrieve_elements(self, html_element):
        flat = Flat()
    
        # Valor predeterminado para los campos en caso de excepción
        default_value = "No especificado"
        
        flat.origin = "Idealista"
        
        try:
            price = html_element.find("span", class_="item-price").get_text(strip=True)
            flat.price = re.search(r'\d+', price.replace('.', '')).group()
        except:
            flat.price = default_value
        
        try:
            rooms = html_element.find("div", class_="item-detail-char").find_next("span").get_text(strip=True)
            flat.rooms = re.search(r'\d+', rooms).group()
        except:
            flat.rooms = default_value
        
        try:
            description = html_element.find("div", class_="item-description description").find_next("p").get_text().strip().replace('\n', '')
            flat.description = re.sub(r'\s+', ' ', description).strip()  # Quitamos espacios en blanco entre palabras
        except:
            flat.description = default_value
        
        try:
            flat.address = html_element.find("div", class_="item-info-container").find_next("a", class_="item-link").get_text().strip()
        except:
            flat.address = default_value
        
        try:
            flat.original_link = "https://www.idealista.com" + html_element.find("div", class_="item-info-container").find_next("a", class_="item-link").get("href")
        except:
            flat.original_link = default_value
        
        try:
            flat.image_link = html_element.find("img").get("src")
        except:
            flat.image_link = default_value
        
        return flat

    def build_url(self, filters):

        province = filters["province"] #valor por defecto es 'malaga'
        municipality = filters["municipality"] #valor por defecto es 'fuengirola'
        min_price = filters["min_price"] #valor por defecto es '100'
        max_price = filters["max_price"] #valor por defecto es '900'
        room_numbers = filters["room_numbers"] 

        # URL de la solicitud
        #url = f'https://www.idealista.com/ajax/listingcontroller/listingajax.ajax?locationUri=fuengirola-malaga&typology=1&operation=2&freeText=&adfilter_pricemin=default&adfilter_price={max_price}&adfilter_area=default&adfilter_areamax=default&adfilter_amenity=default&adfilter_apartment=&adfilter_rooms_0=&adfilter_rooms_1=&adfilter_rooms_2=2&adfilter_rooms_3=3&adfilter_rooms_4_more=4&adfilter_baths_1=&adfilter_baths_2=&adfilter_baths_3=&adfilter_newconstruction=&adfilter_goodcondition=&adfilter_toberestored=&adfilter_housingpetsallowed=&adfilter_hasairconditioning=&adfilter_wardrobes=&adfilter_lift=&adfilter_flatlocation=&adfilter_parkingspace=&adfilter_garden=&adfilter_swimmingpool=&adfilter_hasterrace=&adfilter_boxroom=&adfilter_accessibleHousing=&adfilter_seaviews=&adfilter_luxury=&adfilter_top_floor=&adfilter_intermediate_floor=&adfilter_ground_floor=&adfilter_hasplan=&adfilter_digitalvisit=&adfilter_agencyisabank=&adfilter_published=default&ordenado-por=&adfilter_onlyflats=&adfilter_penthouse=&adfilter_duplex=&adfilter_homes=&adfilter_independent=&adfilter_semidetached=&adfilter_terraced=&adfilter_countryhouses=&adfilter_chalets=&device=mobile'
        # Base URL
        base_url = 'https://www.idealista.com/ajax/listingcontroller/listingajax.ajax'

        # Parámetros dinámicos
        params = {
            'locationUri': f'{municipality.lower()}-{province.lower()}',
            'typology': '1',
            'operation': '2',
            'freeText': '',
            'adfilter_pricemin': min_price,
            'adfilter_price': max_price,  # Ejemplo de parámetro dinámico
            'adfilter_area': 'default',
            'adfilter_areamax': 'default',
            'adfilter_amenity': 'default',
            'adfilter_apartment': '',
            'adfilter_rooms_0': '',
            'adfilter_rooms_1': set_room_number_to_one(room_numbers),
            'adfilter_rooms_2': set_room_number_to_two(room_numbers),
            'adfilter_rooms_3': set_room_number_to_three(room_numbers),
            'adfilter_rooms_4_more': set_room_number_to_four(room_numbers),
            'adfilter_baths_1': '',
            'adfilter_baths_2': '',
            'adfilter_baths_3': '',
            'adfilter_newconstruction': '',
            'adfilter_goodcondition': '',
            'adfilter_toberestored': '',
            'adfilter_housingpetsallowed': '',
            'adfilter_hasairconditioning': '',
            'adfilter_wardrobes': '',
            'adfilter_lift': '',
            'adfilter_flatlocation': '',
            'adfilter_parkingspace': '',
            'adfilter_garden': '',
            'adfilter_swimmingpool': '',
            'adfilter_hasterrace': '',
            'adfilter_boxroom': '',
            'adfilter_accessibleHousing': '',
            'adfilter_seaviews': '',
            'adfilter_luxury': '',
            'adfilter_top_floor': '',
            'adfilter_intermediate_floor': '',
            'adfilter_ground_floor': '',
            'adfilter_hasplan': '',
            'adfilter_digitalvisit': '',
            'adfilter_agencyisabank': '',
            'adfilter_published': 'default',
            'ordenado-por': '',
            'adfilter_onlyflats': '',
            'adfilter_penthouse': '',
            'adfilter_duplex': '',
            'adfilter_homes': '',
            'adfilter_independent': '',
            'adfilter_semidetached': '',
            'adfilter_terraced': '',
            'adfilter_countryhouses': '',
            'adfilter_chalets': '',
            'device': 'mobile'
        }

        # Convertir parámetros a cadena de consulta
        query_string = urlencode(params, doseq=True)

        # Construir la URL completa
        url = f"{base_url}?{query_string}"
        return  url
    
    def build_headers(self):
         # Headers de la solicitud
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'es-BO,es-419;q=0.9,es;q=0.8,en;q=0.7',
            'cookie': '_pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1ldWQ2cTB0fGx6NXk5OG90In0%3D; _pcid=%7B%22browserId%22%3A%22lz5y98os3oozfgdc%22%2C%22_t%22%3A%22meud6q2s%7Clz5y98qs%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbKGFYA2AI4AmfAB9UALwCsATwCcADjF8AvkA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22EB0AwNZuHmPRWQfU2F9w%22%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkwZmFjZDktOGY5Mi02NzgxLTkzMWItZmM1NDVlOGZiNDFkIiwiY3JlYXRlZCI6IjIwMjQtMDctMjhUMTk6MjQ6NTYuNDQxWiIsInVwZGF0ZWQiOiIyMDI0LTA3LTI4VDE5OjI0OjU3LjUzM1oiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQCd2QAQCd2QAAHABBENA-FgAAAAAAAAAAAAAAAAAACkoAMAAQUuKQAYAAgpcQgAwABBS4dABgACClwSADAAEFLg.YAAAAAAAAAAA; utag_main__prevCompleteClickName=; galleryHasBeenBoosted=true; askToSaveAlertPopUp=false; userUUID=b1f6d604-ef32-4b38-b985-52b6c1fc410c; contact58c03337-8f82-4242-adf9-e4c3d2e8c945="{\'maxNumberContactsAllow\':10}"; cookieSearch-1="/alquiler-viviendas/fuengirola-malaga/con-precio-hasta_850,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas/:1722846849334"; SESSION=f8a4ee08984fb0bc~58c03337-8f82-4242-adf9-e4c3d2e8c945; utag_main__sn=6; utag_main_ses_id=1722846855438%3Bexp-session; utag_main__pn=1%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Falquiler-viviendas%2Ffuengirola-malaga%2Fcon-precio-hasta_850%2Cde-dos-dormitorios%2Cde-tres-dormitorios%2Cde-cuatro-cinco-habitaciones-o-mas%2F%3Bexp-1722850455484; utag_main__prevVtUrlReferrer=%3Bexp-1722850455484; utag_main__prevVtSource=Direct traffic%3Bexp-1722850455484; utag_main__prevVtCampaignName=organicWeb%3Bexp-1722850455484; utag_main__prevVtCampaignCode=%3Bexp-1722850455484; utag_main__prevVtCampaignLinkName=%3Bexp-1722850455484; utag_main__prevVtRecipientId=%3Bexp-1722850455484; utag_main__prevVtProvider=%3Bexp-1722850455484; utag_main__se=2%3Bexp-session; utag_main__ss=0%3Bexp-session; utag_main__st=1722848655673%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1722850455684; utag_main__prevLevel2=005-idealista/portal%3Bexp-1722850455684; _last_search=officialZone; dicbo_id=%7B%22dicbo_fetch%22%3A1722846856278%7D; datadome=DzYd0lnoI4QCp5Zn8G1zkhLwk9K0DMErSp~i2a9V6tv_9YGkPJuAOldCw3tQQmOTNW5C7JX9SntRqOqe6UzVIOlHlyY~HAAw2NCsZ~a~X1Vrnoehc4zRHJTyckk7SJhC',
            'priority': 'u=1, i',
            'referer': 'https://www.idealista.com/alquiler-viviendas/fuengirola-malaga/con-precio-hasta_850,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas/',
            'sec-ch-device-memory': '8',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.89", "Chromium";v="127.0.6533.89"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        return headers
    
def set_room_number_to_one(value):
    if value == '1' :
        return '1'
    
    return ''

def set_room_number_to_two(value):
    if value == '1' or value == '2':
        return '2'
    
    return ''

def set_room_number_to_three(value):
    if value == '1' or value == '2' or value == '3':
        return '3'
    
    return ''

def set_room_number_to_four(value):
    if value == '1' or value == '2' or value == '3' or value == '4':
        return '4'
    
    if int(value) >= 4:
        return '4'
    
    return ''