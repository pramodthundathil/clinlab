from django.db import models
from django.contrib.auth.models import User
from Clinic.models import TestType, Order
import uuid
from datetime import datetime


class TestPriceSlab(models.Model):
    test = models.ForeignKey(TestType, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return str(str(self.test) + " " + str(self.price))


class Invoce(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    order = models.OneToOneField(Order,on_delete=models.SET_NULL, null=True, blank=True)
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    date_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True, default=0)
    adjustment = models.FloatField(null=True, blank=True, default=0)
    total_payable = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_unique_order_number()
        super(Invoce, self).save(*args, **kwargs)

    def generate_unique_order_number(self):
        current_time = datetime.now()
        serial_number = current_time.strftime("%Y%m%d%H%M%S")
        return serial_number
    
    def __str__(self):
        return str(self.order + self.invoice_number)
    
class InvoiceItems(models.Model):
    TestPrice = models.ForeignKey(TestPriceSlab,on_delete=models.SET_NULL,null=True)
    price = models.FloatField(default=0)
    invoice = models.ForeignKey(Invoce, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

        return str(self.TestPrice + self.invoice )




    