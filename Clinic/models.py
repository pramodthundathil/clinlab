from django.db import models
from Home.models import Patient
import uuid
from django.contrib.auth.models import User


class TestCategory(models.Model):
    name = models.CharField(max_length=255)
    specimen = models.CharField(max_length=255)
    add_by =models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    
class TestType(models.Model):
    name = models.CharField(max_length=100)
    specimen = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    normal_range = models.CharField(max_length=100, default=" ", blank=True, null=True)
    unit = models.CharField(max_length=50,default=" ", blank=True, null=True)
    test_category = models.ForeignKey(TestCategory, on_delete=models.SET_NULL, null=True, blank=True)
    Interpertaion_description = models.TextField(null=True, default="")

    def __str__(self):
        return self.name
    

class ComprehensiveTest(models.Model):
    category = models.ForeignKey(TestCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=20)
    specimen = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tests = models.ManyToManyField(TestType)
    availability = models.BooleanField(default=True)
    add_by =models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)
    


    def __str__(self):
        return str(self.name)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sample_collected_time = models.DateTimeField(null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    patient_name = models.CharField(max_length=255, null=True, blank=True)
    sample = models.CharField(max_length=10,default=" ")
    doctor = models.CharField(max_length=100, default='Self')
    hospital = models.CharField(max_length=100, default=" ")
    order_number = models.CharField(max_length=10, unique=True, editable=False)
    order_status = models.BooleanField(default=False)
    approvel_status = models.BooleanField(default=False)
    approval_date = models.DateTimeField(auto_now_add=False,null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_unique_order_number()
        super(Order, self).save(*args, **kwargs)

    def generate_unique_order_number(self):
        # Generate a unique order number using UUID
        return str(uuid.uuid4().hex[:5]).upper()

    def __str__(self):
        return self.order_number
    

class TestResult(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    is_comprehensive = models.BooleanField(default=False)
    comprehensive_test = models.ForeignKey(ComprehensiveTest, on_delete=models.SET_NULL, null=True, blank=True)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    test_date = models.DateTimeField(auto_now_add=True)
    result_value = models.CharField(max_length=30, null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='test_results')
    comments = models.TextField(blank=True, null=True)
    validated = models.BooleanField(default=False)
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_results')

    def __str__(self):
        return f"{self.order.patient} - {self.test_type} - {self.test_date.strftime('%Y-%m-%d')}"
