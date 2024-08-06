from flask import Flask, render_template, redirect, request, url_for
from services.scrapy_manager import ScrapyManager
from forms.flat_form import FilterForm
from services.scrapy_modules.foto_casa_module import FotoCasa
from services.scrapy_modules.idealista_module import Idealista

app = Flask(__name__)
app.config['SECRET_KEY'] = "my_key"

#Lista de componentes web para las distintas plataformas de pisos
#foto_casa = FotoCasa()
idealista = Idealista()

#Scrapy manager para orquestar los componentes web
scrapy_manger = ScrapyManager()
scrapy_manger.add_web_component(idealista)


RULE_LIST = []


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
        
        print(form_fields)
        
        scrapy_manger.start_process(form_fields, RULE_LIST)
        flat_list = scrapy_manger.get_flatList()
        #flat_list = []

        return render_template("index.html", flat_list = flat_list,  form=form)
        
    scrapy_manger.start_process()
    flat_list = scrapy_manger.get_flatList()
    #flat_list = []

    return render_template("index.html", flat_list = flat_list,  form=form)
