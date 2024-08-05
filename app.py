from flask import Flask, render_template
from services.scrapy_manager import ScrapyManager
from services.scrapy_modules.foto_casa_module import FotoCasa
from services.scrapy_modules.idealista_module import Idealista

app = Flask(__name__)

#Lista de componentes web para las distintas plataformas de pisos
#foto_casa = FotoCasa()
idealista = Idealista()

#Scrapy manager para orquestar los componentes web
scrapy_manger = ScrapyManager()
scrapy_manger.add_web_component(idealista)


@app.route("/api/v1/flat/filter")
def hello_world():
    scrapy_manger.start_process("Añadir filtros", "Añadir reglas")
    flat_list = scrapy_manger.get_flatList()
    return render_template("index.html", flat_list = flat_list)