class Flat:

    def __init__(self, name, address, price, phone_number, description, original_link, image_link):
        self.name = name
        self.address = address
        self.price = price
        self.phone_number= phone_number
        self.description = description
        self.original_link= original_link
        self.image_link= image_link

    def __str__(self):
        return f"[Name:{self.name}, Address:{self.address}, Price:{self.price}, Phone number:{self.phone_number}, Description:{self.description}, Link:{self.original_link}, Image:{self.image_link}]"
