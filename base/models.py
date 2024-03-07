from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class Customer(AbstractUser):

    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="default.png")
    description = models.TextField(null=True, blank=True)
    available_quantity = models.IntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.address


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=200, null=True, blank=False, default="Created", choices=[("Created", "Created"), ("Processing", "Processing"), ("Shipped", "Shipped"), ("Delivered", "Delivered"), ("Cancelled", "Cancelled")])
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, null=True)


    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)



    def __str__(self):
        return str(self.id)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total





class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    @property
    def get_total_quantity(self):
        total = self.quantity
        return total
    @property
    def get_total_price(self):
        total = self.product.price
        return total

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)




