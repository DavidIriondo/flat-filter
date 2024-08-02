from services.scrapy_modules.scrapy_base import ScrapyBase

class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ScrapyManager(Singleton):
    def __init__(self, ):
        if not hasattr(self, 'initialized'):
            self.flatList = []
            self.webComponents = []
            self.initialized = True

    #Añadir pisos a la lista de pisos
    def get_flatList(self):
        return self.flatList

    def add_to_flatList(self, element):
        self.flatList.append(element)

    #Añadir componentes para escrapear
    def add_web_component(self, component):
        self.webComponents.append(component)

    def start_process(self, filters, rules):
        print("Iniciando proceso de scrapy...")
        for component in self.webComponents:
            self.flatList.extend(component.start_scrapy_process())