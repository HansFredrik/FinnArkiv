from django.db import models

class CarClassified(models.Model):
    finnid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=10000, null=True, blank=True)
    sold = models.BooleanField()
    status = models.CharField(max_length=200, null=True, blank=True)
    postalcode = models.IntegerField(null=True, blank=True)
    postalname = models.CharField(max_length=200, null=True, blank=True)
    mileage = models.CharField(max_length=200, null=True, blank=True)
    bodytype = models.CharField(max_length=200, null=True, blank=True)
    carlocation = models.CharField(max_length=200, null=True, blank=True)
    carsalesform = models.CharField(max_length=200, null=True, blank=True)
    warranty = models.CharField(max_length=200, null=True, blank=True)
    yearmodel = models.CharField(max_length=200, null=True, blank=True)
    registrationclass = models.CharField(max_length=200, null=True, blank=True)
    enginevolume = models.CharField(max_length=200, null=True, blank=True)
    engineeffect = models.CharField(max_length=200, null=True, blank=True)
    enginefuel = models.CharField(max_length=200, null=True, blank=True)
    weight = models.CharField(max_length=200, null=True, blank=True)
    transmission = models.CharField(max_length=200, null=True, blank=True)
    wheeldrive = models.CharField(max_length=200, null=True, blank=True)
    exteriourcolourmain = models.CharField(max_length=200, null=True, blank=True)
    exteriourcolour = models.CharField(max_length=200, null=True, blank=True)
    interiourcolour = models.CharField(max_length=200, null=True, blank=True)
    noofseats = models.CharField(max_length=200, null=True, blank=True)
    noofdoors = models.CharField(max_length=200, null=True, blank=True)
    noofowners = models.CharField(max_length=200, null=True, blank=True)
    regno = models.CharField(max_length=200, null=True, blank=True)
    co2 = models.CharField(max_length=200, null=True, blank=True)
    seller = models.CharField(max_length=200, null=True, blank=True)

class Make(models.Model):
    make = models.CharField(max_length=100, primary_key=True)
    count = models.IntegerField()
class Model(models.Model):
    model = models.CharField(max_length=100, primary_key=True)
    make = models.ForeignKey(Make)
    count = models.IntegerField()