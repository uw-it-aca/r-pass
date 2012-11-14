from django.db import models
from django_fields.fields import EncryptedTextField, EncryptedCharField

class Host(models.Model):
    cname = models.CharField(max_length=250, unique=True)

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    hosts = models.ManyToManyField(Host)

class AccessToken(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    user = EncryptedCharField(max_length=150)
    access_token = EncryptedTextField()
    service = models.ForeignKey(Service)

