class Flat:

    def __init__(self,origin, name, address, price, phone_number, description, original_link, image_link):
        self.origin = origin
        self.name = name
        self.address = address
        self.price = price
        self.phone_number= phone_number
        self.description = description
        self.original_link= original_link
        self.image_link= image_link

    def format(self):
        if self.origin == "":
            pass

    def __str__(self):
        return (
            f"[ Origin: {self.origin}\n"
            f"Name: {self.name}\n"
            f"Address: {self.address}\n"
            f"Price: {self.price}\n"
            f"Phone number: {self.phone_number}\n"
            f"Description: {self.description}\n"
            f"Link: {self.original_link}\n"
            f"Image: {self.image_link} ]"
        )
        #return f"[Name:{self.name},Address:{self.address}, Price:{self.price}, Phone number:{self.phone_number}, Description:{self.description}, Link:{self.original_link}, Image:{self.image_link}]"
