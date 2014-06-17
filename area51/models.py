"""
DB interface in the form of models
"""

from django.db import models
from geoposition.fields import GeopositionField
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# The user model/table. Every row represents a user.
class User(AbstractUser):
    telephone = models.CharField(max_length=13, null=True)

# The event model/table. Every row represents an event.
class Event(models.Model):
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return "/e/%i/" % self.id
    position = GeopositionField()
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User)
    description = models.TextField()
    category = models.CharField(max_length=100)
    dealt = models.BooleanField(default=False)
    date_of_creation = models.DateTimeField('date created', default=datetime.now)
    photo1 = models.ImageField(upload_to="aliens", null=True, blank=True)
    photo2 = models.ImageField(upload_to="aliens", null=True, blank=True)
    photo3 = models.ImageField(upload_to="aliens", null=True, blank=True)
    photo4 = models.ImageField(upload_to="aliens", null=True, blank=True)

# The available categories
class Aliencategories(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

# Connection between events and their checkers/contributors
class Contribution(models.Model):
    def __str__(self):
        return self.comment
    admin_name = models.ForeignKey(User)
    event_id = models.ForeignKey(Event)
    date_of_contrib = models.DateTimeField('date checked', default=datetime.now)
    comment = models.TextField()
