from django.db import models

# Create your models here.


class BitlyURL(models.Model):
    unshorted_url = models.URLField(max_length=255,unique=True)
    shortened_url = models.URLField(max_length=30)