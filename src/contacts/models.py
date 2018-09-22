from django.db import models


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64, null=True)
    building_number = models.IntegerField(null=True)
    flat_number = models.IntegerField(null=True)


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
