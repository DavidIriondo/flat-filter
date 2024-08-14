import secrets
import re

from flask import Flask, render_template, redirect, request, url_for, abort

from services.scrapy_manager import ScrapyManager
from forms.flat_form import FilterForm
from services.scrapy_modules.foto_casa_module import FotoCasa
from services.scrapy_modules.idealista_module import Idealista
from utils.utils import format_rules_for_web, get_regex_rules
from dtos.flat import Flat


#Configuration app class
app = Flask(__name__)

#Scrapy manager para orquestar los componentes web
scrapy_manger = ScrapyManager()
scrapy_manger.add_web_component(FotoCasa())
scrapy_manger.add_web_component(Idealista())

#Obtenemos las lista de palabras clave para mostrarlas en la web
rules = get_regex_rules()
key_words = format_rules_for_web(rules.keys())

#Compilamos las palabras clave y las convertimos en objetos regex una vez para reutilizarlos
compiled_rules = []
for r in rules.values():
    lower_case_regex = r.lower()
    compiled_rules.append(re.compile(lower_case_regex))

#Pagina principal
@app.route("/api/v1/flat/main", methods=["GET"])
def main_page():
    #Creamos el formulario con la informcion recogida de la URL, asi cuando abra los filtros verá el formulario
    #con los filtros que quiere usar
    form = FilterForm()
    form.province.data = request.args.get('province', default="malaga")
    form.municipality.data = request.args.get('municipality', default="fuengirola")
    form.min_price.data = request.args.get('min_price', default="100")
    form.max_price.data = request.args.get('max_price', default="900")
    form.room_numbers.data = request.args.get('room_numbers', default="2")

    #Convierto la informacion de mi formulario en un diccionario para que el scrapy manager lo use
    form_fields={
            "province": form.province.data,
            "municipality": form.municipality.data,
            "min_price": form.min_price.data,
            "max_price": form.max_price.data,
            "room_numbers": form.room_numbers.data
            }

    #Al realizar la peticion GET usamos el filtro por defecto y usamos las reglas de matcheo
    scrapy_manger.start_process(compiled_rules, form_fields)
    flat_list = scrapy_manger.get_flatList()

    return render_template("index.html", flat_list = flat_list,  form=form, key_words=key_words)


#-------------Paginas de errores-----------
@app.errorhandler(404)
def page_not_found(error):
    # Redirige a una página de error personalizada
    return render_template("error/error.html", code=404, description="Page not found"), 404

@app.errorhandler(400)
def bad_request(error):
    # Redirige a una página de error personalizada
    return render_template("error/error.html", code=400, description="Bad Request"), 400

@app.errorhandler(500) 
def internal_server_error(error):
    # Redirige a una página de error personalizada
    return render_template("error/error.html", code=500, description="Internal Server Error"), 500


#Punto de entrada
if __name__ == "__main__":
    app.run()
