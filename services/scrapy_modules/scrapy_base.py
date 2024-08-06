from abc import ABC, abstractmethod

class ScrapyBase(ABC):

    @abstractmethod
    def start_scrapy_process(self, filters, rules):
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

    
    def apply_rules(self, rules):
        """Metodo booleano que filtra los pisos en funcion de si pasan o no las reglas de validacion.
        En este caso las relgas son palabras concretas que los pisos no deben tener para considerarse validos"""

        pass

