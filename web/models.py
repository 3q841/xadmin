from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
# Create your models here.
from django.contrib.auth.models import User

## image compression method

def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io , 'JPEG' , Quality=60)
    new_image = File(im_io, name=image.name)
    return new_image 

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)

class post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.CharField(max_length=255, null=True , blank=True)
    image = models.ImageField(upload_to='screen', blank=True)

    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}-{}".format(self.date, self.author)

class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=52)
    username = models.CharField(max_length=36)
    password = models.CharField(max_length=8)
"""
class Account(AbstractBaseUser):
    number=models.BigInteger()
    username= models.CharField()
    date_joined=models.DateTimeField(verbose_name'date joined')
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = [ 'username', 'number' ]

    def __str__(self):
        return self.number
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_Label):
        return True

"""