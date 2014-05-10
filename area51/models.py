from django.db import models

ALIENCATEGORIES = (
    (0, 'UFO'),
    (1, 'Alien in the Flesh'),
    (2, 'Strange Lights'),
    (3, 'Glitch in the Matrix'),
)

class User(models.Model):
    def __str__(self):
        return self.username
    username = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.IntegerField(max_length=10, null=True, blank=True)
    #TODO: password

class Event(models.Model):
    def __str__(self):
        return self.event_desc
    # TODO: geolocation field
    creator = models.ForeignKey(User)
    event_desc = models.TextField()
    category = models.IntegerField(max_length=1, choices=ALIENCATEGORIES, default=0)
    date_of_creation = models.DateField(auto_now=True)
    photo = models.ImageField(upload_to="aliens/", null=True, blank=True)

class Admin(models.Model):
    def __str__(self):
        return self.admin_name
    admin_name = models.ForeignKey(User, primary_key=True)
    cont_events = models.ManyToManyField(Event, through='Contribution')

class Contribution(models.Model):
    def __str__(self):
        return self.comment
    admin_name = models.ForeignKey(Admin)
    event_id = models.ForeignKey(Event)
    date_of_contrib = models.DateField(auto_now=True)
    comment = models.TextField()
