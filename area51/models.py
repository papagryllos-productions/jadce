from django.db import models
from django.forms import ModelForm
from geoposition.fields import GeopositionField
from django.contrib.auth.models import AbstractUser

ALIENCATEGORIES = (
    (0, 'UFO'),
    (1, 'Alien in the Flesh'),
    (2, 'Strange Lights'),
    (3, 'Glitch in the Matrix'),
    (4, 'Gojira Invasion'),
    (5, 'Vortex to Unknown'),
    (6, 'Messiah Returns'),
    (7, 'Man stuck in Astral Projection'),
)

class User(AbstractUser):
    telephone = models.CharField(max_length=13, null=True)

class Event(models.Model):
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return "/event/%i/" % self.id
    position = GeopositionField()
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User)
    description = models.TextField()
    category = models.IntegerField(max_length=1, choices=ALIENCATEGORIES, default=0)
    dealt = models.BooleanField(default=False)
    date_of_creation = models.DateField(auto_now=True)
    photo1 = models.ImageField(upload_to="aliens", null=True, blank=True)
    photo2 = models.ImageField(upload_to="aliens", null=True, blank=True)
    photo3 = models.ImageField(upload_to="aliens", null=True, blank=True)
    photo4 = models.ImageField(upload_to="aliens", null=True, blank=True)

class Contribution(models.Model):
    def __str__(self):
        return self.comment
    admin_name = models.ForeignKey(User)
    event_id = models.ForeignKey(Event)
    date_of_contrib = models.DateField(auto_now=True)
    comment = models.TextField()

class UserForm(ModelForm):
    class Meta:
        model = User
