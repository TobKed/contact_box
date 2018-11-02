from django.db import models
from users.models import Profile
from django.urls import reverse


class ContactGroupQuerySet(models.QuerySet):
    def search(self, search=None):
        if search:
            return self.filter(name__contains=search) | self.filter(description__contains=search)
        return self


class ContactGroupManager(models.Manager):
    def get_queryset(self):
        return ContactGroupQuerySet(self.model, using=self._db)

    def search(self, search):
        return self.get_queryset().search(search=search)


class ContactGroup(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    objects = ContactGroupManager()

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("group-detail", kwargs={"pk": self.pk})


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64, null=True, blank=True)
    building_number = models.IntegerField(null=True, blank=True)
    flat_number = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city} {self.street} {self.building_number} {self.flat_number}"

    def get_absolute_url(self):
        return reverse("address-detail", kwargs={"pk": self.pk})


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    address = models.ForeignKey(Address, null=True,blank=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(ContactGroup, null=True, blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("person-detail", kwargs={"pk": self.pk})


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
