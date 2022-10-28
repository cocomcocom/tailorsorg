from django.db import models

# Create your models here.

class HomeDetails(models.Model):


    Email = models.EmailField()

    Address = models.TextField()


class DressSample(models.Model):

    Dressid = models.CharField(max_length=100)

    Url = models.TextField()

class Queue(models.Model):

    Username = models.CharField(max_length=100)

    Email = models.EmailField(max_length=100, default=None)

    Userpreferrence = models.CharField(max_length=100)

    Priority = models.DateField()

class Pending(models.Model):

    Username = models.CharField(max_length=100)

    Email = models.EmailField(max_length=100, default=None)

    Userpreferrence = models.CharField(max_length=100, default=None)

    Priority = models.DateField()

class Served(models.Model):

    Username = models.CharField(max_length=100)

    Email = models.EmailField(max_length=100, default=None)


class Bprotect(models.Model):

    counter = models.IntegerField()

    
    
