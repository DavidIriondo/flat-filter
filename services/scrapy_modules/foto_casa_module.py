from selenium.webdriver import Chrome

from services.scrapy_modules.scrapy_base import ScrapyBase
from dtos.flat import Flat

class FotoCasa(ScrapyBase):

    def start_scrapy_process(self):
        #driver = Chrome(executable)
        print("Iniciando proceso de scrapy para fotocasa")
        return [
            Flat("Apartamento 1", "Calle 1", 400.0, "678139548","description", "#", "#"),
            Flat("Apartamento 2", "Calle 1", 400.0, "678139548","description", "#", "#"),
            Flat("Apartamento 3", "Calle 1", 400.0, "678139548","description", "#", "#"),
            Flat("Apartamento 4", "Calle 1", 400.0, "678139548","description", "#", "#")
            ]
    
