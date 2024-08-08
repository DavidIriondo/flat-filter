import secrets

from flask import Flask, render_template, redirect, request, url_for
from services.scrapy_manager import ScrapyManager
from forms.flat_form import FilterForm
from services.scrapy_modules.foto_casa_module import FotoCasa
from services.scrapy_modules.idealista_module import Idealista

secret_key = secrets.token_hex(64)

app = Flask(__name__)
app.config['SECRET_KEY'] = str(secret_key)

#Lista de componentes web para las distintas plataformas de pisos
foto_casa = FotoCasa()
idealista = Idealista()

#Scrapy manager para orquestar los componentes web
scrapy_manger = ScrapyManager()
scrapy_manger.add_web_component(foto_casa)
scrapy_manger.add_web_component(idealista)


RULE_LIST = [
    "piso vacacional",
    "CORTA TEMPORADA",
    "por temporada",
    "NO LARGA TEMPORADA",
    "Alquiler de temporada",
    "Alquiler temporada",
    "Alquiler corta temporada",
    "Alquiler de corta temporada",
    "Short Term Rental",
    "ALQUILER TEMPORADA DE VERANO",
    "Vacacional",
    "NO SE ALQUILA LARGA TEMPORADA",
    "SOLO EN EL LOS MESES DE INVIERNO",
    "de Septiembre a Junio",
    "SOLO PARA PROFESORES"
    #r"Se\s+Alquila\s+desde\s+([A-ZÁÉÍÓÚÑ\s]+)\s+a\s+([A-ZÁÉÍÓÚÑ\s]+)", #Ex:Se Alquila desde Julio a Septiembre
    #r"(\d+)\s+de\s+([A-ZÁÉÍÓÚÑ\s]+)\s+(\d{4})\s+hasta\s+(\d+)\s+de\s+([A-ZÁÉÍÓÚÑ\s]+)\s+(\d{4})",# Ex 1 de Septiembre 2024 hasta 30 de Junio 2025
    #r"TEMPORADA\s+([A-ZÁÉÍÓÚÑ\s]+)\s+A\s+([A-ZÁÉÍÓÚÑ\s]+)", #Ex: temporada septiembre a enero
    #r"SEPTIEMBRE\s+\d{4}\s+A\s+([A-ZÁÉÍÓÚÑ\s]+)\s+(\d{4})", #Ex: SEPTIEMBRE 2024 A JUNIO 2025
    #r"SEPTIEMBRE\s+\d{4}\s+HASTA\s+([A-ZÁÉÍÓÚÑ\s]+)\s+(\d{4})", #Ex: SEPTIEMBRE 2024 HASTA JUNIO 2025
    #r"SEPTIEMBRE\s+DEL\s+\d{4}\s+A\s+([A-ZÁÉÍÓÚÑ\s]+)\s+DE\s+(\d{4})", #Ex: SEPTIEMBRE DEL 2024 A JUNIO DE 2025
    #r"(\d+)\s+DE\s+([A-ZÁÉÍÓÚÑ\s]+)\s+AL\s+(\d+)\s+DE\s+([A-ZÁÉÍÓÚÑ\s]+)", #Ex: 15 SEPTIEMBRE AL 15 JUNIO
    #r"de\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+)\s+a\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+)",#Ex: Disponible de septiembre a junio
    #r"desde\s+el\s+(\d+)\s+de\s+([A-ZÁÉÍÓÚÑa-záéíóúñ]+)\s+de\s+(\d{4})\s+hasta\s+(?:finales\s+de\s+)?([A-ZÁÉÍÓÚÑa-záéíóúñ]+)\s+de\s+(\d{4})" #Ex: desde el 5 de septiembre de 2024 hasta finales de junio de 2025
]
formatted_values = [f"#{value.upper()} " for value in RULE_LIST]

key_words = "".join(formatted_values)


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
        scrapy_manger.start_process(RULE_LIST, form_fields)
        flat_list = scrapy_manger.get_flatList()

        return render_template("index.html", flat_list = flat_list,  form=form, key_words= key_words)
        
    #Al realizar la peticion GET usamos el filtro por defecto y usamos las reglas de matcheo
    scrapy_manger.start_process(RULE_LIST)
    flat_list = scrapy_manger.get_flatList()

    return render_template("index.html", flat_list = flat_list,  form=form, key_words=key_words)


if __name__ == "__main__":
    app.run()
