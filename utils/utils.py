"""File containing utility methods"""
import re


def format_months_for_regex():
    """returns a string containings every months of the year separated by |. Usefully to used in regex expressions
       Result example: (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)
    """
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
        "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    #Añadimos meses mal escritos
    months.append("setiembre")
    # Asegúrate de que todos los nombres de los meses estén en mayúsculas
    months = [month for month in months]

    # Une los nombres de los meses con el símbolo '|'
    regex_pattern = '|'.join(months)
    # Coloca los nombres de los meses entre paréntesis
    return f"({regex_pattern})"


def get_regex_rules():
    """return a dictionary containing and example of key word and the regex to find it:
        dictionary key -> example
        dictionary value -> regex
    """
    rules = {
        "alquiler de temporada" : "alquiler de temporada",
        "temporada de invierno" : "temporada de invierno",
        "alquiler temporada" : "alquiler temporada",
        "alquiler corta temporada" : "alquiler corta temporada",
        "alquiler de corta temporada" : "alquiler de corta temporada",
        "piso vacacional" : "piso vacacional",
        "corta temporada" : "corta temporada",
        "cortas temporadas" : "cortas temporadas",
        "por temporada" : "por temporada",
        "no larga temporada" : "no larga temporada",
        "short term rental" : "short term rental",
        "alquiler temporada de verano" : "alquiler temporada de verano",
        "vacacional" : "vacacional",
        "no se alquila larga temporada" : "no se alquila larga temporada",
        "solo en el los meses de invierno" : "solo en el los meses de invierno",
        "solo para profesores" : "solo para profesores",
        "de septiembre a julio" : rf"{format_months_for_regex()}\s*(a|hasta|hasta fin de|a final de)\s*{format_months_for_regex()}", 
        "15 de Septiembre a 30  de Julio" : rf"[0-9]+\s*(|de)\s*{format_months_for_regex()}\s*(|a|al)\s*[0-9]+\s*(|de)\s*{format_months_for_regex()}", 
        "desde septiembre 2024 a junio 2025" : rf"{format_months_for_regex()}\s(|de)*[0-9]{{4}}\s*(a|al|hasta)\s*{format_months_for_regex()}\s*(|de)[0-9]{{4}}",
        "temporada septiembre a enero" : rf"temporada\s*{format_months_for_regex()}\s*a\s*{format_months_for_regex()}",
        "15 septiembre al 15 junio" : rf"[0-9]+\s*{format_months_for_regex()}\s*(a|al)\s*[0-9]+\s*{format_months_for_regex()}",
        "10 de septiembre y el 30 de junio" : rf"{format_months_for_regex()}\s*(al|hasta el)\s*[0-9]+\s*(|de)\s*{format_months_for_regex()}",
        "1 de septiembre de 2024 hasta/hasta el/al/a 30 de junio 2025" : rf"[0-9]+\s*de\s*{format_months_for_regex()}\s*(|de)\s*[0-9]{{4}}\s*(a|hasta|al|hasta el)\s*[0-9]+\s*(|de)\s*{format_months_for_regex()}\s*(|de)\s*[0-9]{{4}}", 
        "1 de septiembre hasta 30 de junio 2025" : rf"{format_months_for_regex()}\s*(|de)\s*(|[0-9]{{4}})\s*(a|hasta|al|hasta el)\s*[0-9]+\s*(|de)\s*{format_months_for_regex()}\s*(|de)\s*[0-9]{{4}}", 
        "5 de septiembre de 2024 hasta finales de junio de 2025" : rf"{format_months_for_regex()}\s*de\s*[0-9]{{4}}\s*(a|hasta)\s*(|finales)\s*(|de)\s*{format_months_for_regex()}\s*de\s*[0-9]{{4}}" 
    }

    return rules


def format_rules_for_web(rules_list):
    """Returns a single string containing al joinned elements of a list, separated by #"""
    
    formatted_values = [f"#{value.upper()} " for value in rules_list]
    key_words = "".join(formatted_values)

    return key_words