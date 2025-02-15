from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weapon_name = models.CharField(max_length=100)
    weapon_image = models.URLField()
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.weapon_name} - {self.user.username}"


from django.db import models
from django.contrib.auth.models import User
from .models import Order

class OrderedOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weapon_name = models.CharField(max_length=100)
    weapon_image = models.URLField()
    quantity = models.IntegerField()
    order_date = models.DateTimeField()
    confirmed_date = models.DateTimeField(auto_now_add=True)  # Date when the order was confirmed

    def __str__(self):
        return f"{self.weapon_name} - {self.user.username} (Confirmed)"

    class Meta:
        verbose_name = "Ordered Order"
        verbose_name_plural = "Ordered Orders"
