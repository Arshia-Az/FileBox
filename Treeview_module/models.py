from django.db import models

# Create your models here.


class Profile(models.Model):
    avatar = models.ImageField(upload_to = 'images/avatar/')