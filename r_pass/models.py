from django.db import models
from fernet_fields import EncryptedTextField, EncryptedCharField
import re


class Host(models.Model):
    cname = models.CharField(max_length=250, unique=True)


class Group(models.Model):
    source_id = models.CharField(max_length=250, unique=True)


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    hosts = models.ManyToManyField(Host)
    groups = models.ManyToManyField(Group)

    def view_url(self):
        url_title = self.title.lower()
        url_title = re.sub(r'[^\w]+', '-', url_title)
        url_title = re.sub(r'-*$', '', url_title)
        return "/r-pass/service/%s/%i" % (url_title, self.pk)

    def edit_url(self):
        return "%s/edit" % self.view_url()

    def __str__(self):
        return "ID: %s, Title: %s" % (self.pk, self.title)


class AccessToken(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    user = EncryptedCharField(max_length=150)
    access_token = EncryptedTextField()
    service = models.ForeignKey(Service)
