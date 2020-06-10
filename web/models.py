from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class post(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='xreenshot', default='')
    def __str__(self):
        return self.auther