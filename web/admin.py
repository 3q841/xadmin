from django.contrib import admin
from .models import post, Token

# Register your models here.
admin.site.register(post)
admin.site.register(Token)