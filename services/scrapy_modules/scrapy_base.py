import re
from abc import ABC, abstractmethod

class ScrapyBase(ABC):

    @abstractmethod
    def start_scrapy_process(self, rules, filters):
        pass

    @abstractmethod
    def retrieve_elements(self, html_element):
        pass

    @abstractmethod
    def build_url(self, filters):
        pass
    
    @abstractmethod
    def build_headers(self):
        pass

    
    def apply_rules(self, rules, flat):
        """Metodo booleano que filtra los pisos en funcion de si pasan o no las reglas de validacion.
        En este caso las relgas son palabras concretas que los pisos no deben tener para considerarse validos"""

        text = flat.description.lower()

        for rule in rules:

            if rule.search(text):
                #print("El texto contiene la palabra clave: " + str(r))
                return False
            else:
                pass
                #print("El texto no contiene la palabra clave: " + str(r))

        return True