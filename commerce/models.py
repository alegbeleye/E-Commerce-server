from django.db import models
from commerce.validators import validate_percentage_cut
from commerce.controllers import upload_image_to_s3
import bcrypt

# Create your models here.

class Product(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    name = models.CharField(max_length=500)
    original_price = models.FloatField(default=0.00)
    current_price = models.FloatField(default = 0.00)
    price_percentage_cut = models.IntegerField(default=0, validators=[validate_percentage_cut])
    product_info = models.CharField(max_length=50000, null=True)
    product_image_url = models.CharField(max_length=10000, null=True)
    amount_available_in_stock = models.IntegerField(default=0)
    rating = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
    def apply_percentage_cut_to_price(self) -> None:
        price_cut_amount:float =  (self.price_percentage_cut/100) * self.original_price
        self.current_price = self.original_price - price_cut_amount
    
    def apply_url_to_image(self, image) -> None:
        url = upload_image_to_s3(image, self.id, self.name)
        self.product_image_url = url
    


class Customer(models.Model):
    id = models.CharField(max_length=2000, primary_key=True)
    email = models.CharField(max_length=500)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    hashed_password = models.CharField(max_length=5000)
    country = models.CharField(max_length=500)
    
    def __str__(self):
        return self.last_name
    
    def hash_password(self, password) -> None:
        bytes:str = password.encode('utf-8')

        #generating a salt
        salt = bcrypt.gensalt()

        #hashing the password
        hash = bcrypt.hashpw(bytes, salt)

        self.hashed_password = hash.decode('utf-8')
    
    def compare_password(self, raw_password: str) -> None:
        raw_password_encoded = raw_password.encode('utf-8')
        hashed_password_encoded = self.hashed_password.encode('utf-8')
        return bcrypt.checkpw(raw_password_encoded, hashed_password_encoded)
    
    