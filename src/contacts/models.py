from django.db import models
from users.models import Profile


class ContactGroup(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64, null=True)
    building_number = models.IntegerField(null=True)
    flat_number = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.city} {self.street} {self.building_number} {self.flat_number}"


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(ContactGroup, null=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PhoneNumber(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=64)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number}"


class Email(models.Model):
    address = models.CharField(max_length=128)
    type = models.CharField(max_length=64)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}"
