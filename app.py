import secrets
import re

from flask import Flask, render_template, redirect, request, url_for
from services.scrapy_manager import ScrapyManager
from forms.flat_form import FilterForm
from services.scrapy_modules.foto_casa_module import FotoCasa
from services.scrapy_modules.idealista_module import Idealista
from utils.utils import format_rules_for_web, get_regex_rules

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


if __name__ == "__main__":
    app.run()
