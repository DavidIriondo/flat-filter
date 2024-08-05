from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup

from services.scrapy_modules.scrapy_base import ScrapyBase
from dtos.flat import Flat

class FotoCasa(ScrapyBase):

    def start_scrapy_process(self):
        print("Iniciando proceso de scrapy para fotocasa")

        service = Service(executable_path="C:/Users/david/ChomeDriver/chromedriver_127.0.6533.88.exe")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
        driver = webdriver.Chrome(service=service, options=options)

        #Cargamos la pagina
        driver.get("https://www.fotocasa.es/es/alquiler/viviendas/fuengirola/todas-las-zonas/l?maxPrice=900&minRooms=2")

        #Empezamos a scrapear
        #soup = BeautifulSoup(driver.page_source, "html")
        #article_element = soup.find("article", class_="re-CardPackMinimal")
        
        #print(soup.prettify())

        print(driver.page_source)

        test = driver.find_elements(By.CLASS_NAME, 're-CardPackMinimal')
        print(test)


        # Cerramos el navegador
        driver.quit()    
        
        return [
            Flat("Apartamento 1", "Calle 1", 400.0, "678139548","description", "#", "#"),
            Flat("Apartamento 2", "Calle 1", 400.0, "678139548","description", "#", "#"),
            Flat("Apartamento 3", "Calle 1", 400.0, "678139548","description", "#", "#"),
            Flat("Apartamento 4", "Calle 1", 400.0, "678139548","description", "#", "#")
            ]
    
    def retrieveElements(self, html_element):
        flat = Flat()

        flat.name = html_element.find_next("a").get('title')
        flat.price = html_element.find("span", class_="re-CardPrice")
        flat.description = html_element