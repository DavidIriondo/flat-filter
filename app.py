import secrets
import re

from flask import Flask, render_template, redirect, request, url_for, abort

from services.scrapy_manager import ScrapyManager
from forms.flat_form import FilterForm
from services.scrapy_modules.foto_casa_module import FotoCasa
from services.scrapy_modules.idealista_module import Idealista
from utils.utils import format_rules_for_web, get_regex_rules
from dtos.flat import Flat

secret_key = secrets.token_hex(64)

#Configuration app class
app = Flask(__name__)
app.config['SECRET_KEY'] = str(secret_key)

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


mock_list = []
for i in range(1, 91):
    flat = Flat()
    flat.address = f"Address: {i}"
    flat.description = "This is an example of a short text description"
    flat.price = "800"
    flat.rooms = "2"
    flat.origin = "Example"
    mock_list.append(flat)
    

#Pagina principal
@app.route("/api/v1/flat/main", methods=["GET", "POST"])
def main_page():
    #Formulario que envia el usuario
    form = FilterForm()

    #El usuario ha enviado el formulario y el metodo 
    if request.method == "POST" and form.validate():

        form_fields={
            "province": form.province.data,
            "municipality": form.municipality.data,
            "min_price": form.min_price.data,
            "max_price": form.max_price.data,
            "room_numbers": form.room_numbers.data
            }
        
        #Aplicamos el filtro seleccionado y las reglas de matcheo
        #scrapy_manger.start_process(compiled_rules, form_fields)
        flat_list = scrapy_manger.get_flatList()

        return render_template("index.html", flat_list = mock_list,  form=form, key_words= key_words)
        
    #Al realizar la peticion GET usamos el filtro por defecto y usamos las reglas de matcheo
    #scrapy_manger.start_process(compiled_rules)
    flat_list = scrapy_manger.get_flatList()

    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(mock_list) + per_page - 1) // per_page

    items_on_page = mock_list[start:end]

    return render_template("index.html", flat_list = mock_list,  form=form, key_words=key_words, 
                           items_on_page = items_on_page, total_pages = total_pages, page = page)

"""
#Pagina principal
@app.route("/api/v1/flat/main", methods=["GET", "POST"])
def main_page():
    #Formulario que envia el usuario
    form = FilterForm()

    #El usuario ha enviado el formulario y el metodo 
    if request.method == "POST" and form.validate():

        form_fields={
            "province": form.province.data,
            "municipality": form.municipality.data,
            "min_price": form.min_price.data,
            "max_price": form.max_price.data,
            "room_numbers": form.room_numbers.data
            }
        
        #Aplicamos el filtro seleccionado y las reglas de matcheo
        scrapy_manger.start_process(compiled_rules, form_fields)
        flat_list = scrapy_manger.get_flatList()

        return render_template("index.html", flat_list = flat_list,  form=form, key_words= key_words)
        
    #Al realizar la peticion GET usamos el filtro por defecto y usamos las reglas de matcheo
    scrapy_manger.start_process(compiled_rules)
    flat_list = scrapy_manger.get_flatList()

    return render_template("index.html", flat_list = flat_list,  form=form, key_words=key_words)
"""


#-------------Paginas de errores-----------
@app.errorhandler(404)
def page_not_found(error):
    # Redirige a una página de error personalizada
    return render_template("error/error.html", code=404, description="Page not found"), 404

#Paginas de errores
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
    app.run(debug=True)
