from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.IntegerField(max_length=10)
    #TODO: password

class Event(models.Model):
    creator = models.ForeignKey(User)
    event_desc = models.TextField()
    #TODO: category enumeration,geolocation
    category = models.CharField(max_length=100)
    date_of_creation = models.DateField(auto_now=True)
#    photo = models.ImageField()

class Admin(models.Model):
    admin_name = models.ForeignKey(User, primary_key=True)
    cont_events = models.ManyToManyField(Event, through='Contribution')

class Contribution(models.Model):
    admin_name = models.ForeignKey(Admin)
    event_id = models.ForeignKey(Event)
    date_of_contrib = models.DateField(auto_now=True)
    comment = models.TextField()
