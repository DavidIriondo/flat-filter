from abc import ABC, abstractmethod

class ScrapyBase(ABC):

    @abstractmethod
    def start_scrapy_process(self):
        pass

    @abstractmethod
    def retrieve_elements(self, html_element):
        pass

