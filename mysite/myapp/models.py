from django.db import models

# Create your models here.


class Location(models.Model):
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    pincode = models.CharField(max_length=10)
    timeslot = models.CharField(max_length=50)

    def __str__(self):
        return self.address


class Database(models.Model):
    no = models.IntegerField()
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    pincode = models.IntegerField()
    timeslot = models.CharField(max_length=50, default='9:00am - 5:00pm')

    def __str__(self):
        return f"Database entry {self.no}: {self.address}, {self.pincode}"


class Random(models.Model):
    order_no = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=100, decimal_places=50)
    longitude = models.DecimalField(max_digits=100, decimal_places=50)
    pincode = models.IntegerField()
    timeslot = models.CharField(max_length=50)

    def __str__(self):
        return self.order_no


class Shipment(models.Model):
    order_no = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pincode = models.CharField(max_length=10)
    timeslot = models.CharField(max_length=50)


class Neworder_database(models.Model):
    pincode = models.CharField(max_length=100)
    timeslot = models.CharField(max_length=100)
    trip_capacity = models.CharField(max_length=50)
    radius = models.DecimalField(max_digits=9, decimal_places=6 , default=0)
    trip_score = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    #newcode
    num = models.IntegerField(default=0)
    count = models.IntegerField(default=1,blank=True)
    locations = models.CharField(max_length=500,default=0)
    
class Trip(models.Model):
    order_no = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    # latitude = models.FloatField(default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True)
    # longitude = models.FloatField(default=0.0)
    pincode = models.CharField(max_length=10)
    timeslot = models.CharField(max_length=50)


    def __str__(self):
        return f"Trip {self.id}"

