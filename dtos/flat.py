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
