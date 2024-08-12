from services.scrapy_modules.scrapy_base import ScrapyBase

class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ScrapyManager(Singleton):

    #Valores del filtro por defecto se usa cuando se llama a la pagina sin usar el metodo POST
    DEFAULT_FORM = {
        "province": "malaga",
        "municipality": "fuengirola",
        "min_price": "100",
        "max_price": "900",
        "room_numbers": "2"
        }
    
    def __init__(self, ):
        if not hasattr(self, 'initialized'):
            self.flatList = []
            self.webComponents = []
            self.initialized = True

    #Añadir pisos a la lista de pisos
    def get_flatList(self):
        return self.flatList
    
    #Eliminar los datos de la lista
    def clear_flatList(self):
        return self.flatList.clear()

    #Añadir componentes scrapy
    def add_to_flatList(self, element):
        self.flatList.append(element)

    #Añadir componentes para escrapear
    def add_web_component(self, component):
        self.webComponents.append(component)

    def start_process(self, rules = [], filters = DEFAULT_FORM):
        """Si no se pasan los filtros se crea un filtro por defecto"""

        self.clear_flatList()

        for component in self.webComponents:
            self.flatList.extend(component.start_scrapy_process(rules, filters))

