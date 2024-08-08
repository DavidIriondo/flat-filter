class Flat:
    origin = ''
    address = ''
    rooms = ''
    price = ''
    description = ''
    original_link= ''
    image_link= ''

    def format(self):
        
        if self.origin == "":
            pass

    def __str__(self):
        return (
            f"[ Origin: {self.origin}\n"
            f"Address: {self.address}\n"
            f"Price: {self.price}\n"
            f"Description: {self.description}\n"
            f"Link: {self.original_link}\n"
            f"Image: {self.image_link} ]"
        )
        #return f"[Name:{self.name},Address:{self.address}, Price:{self.price}, Phone number:{self.phone_number}, Description:{self.description}, Link:{self.original_link}, Image:{self.image_link}]"
