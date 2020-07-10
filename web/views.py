# -*- coding: utf-8 -*-

from json import JSONEncoder
import datetime 
from django.views.generic import ListView
from django.core import serializers
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST
from .models import User, Token, post ,Passwordresetcodes

random_str = lambda N: ''.join(
    random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


@csrf_exempt
def sub_qustion(request):

    """ submit Answare of every Question """
    this_date =request.POST['date'] if 'date' in request.POST else timezone.now()
    token = request.POST['token']
    this_user = User.objects.filter(token__token = token).get()
    input_image = request.FILES['image']
    post.objects.create(author = this_user, date=this_date,
                        text=request.POST['text'],image= input_image )

    return JsonResponse({
        'status' : 'ok'
    }, encoder=JSONEncoder)

def register(request):
    if request.POST.__contains__('requestcode'):  # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message

        if not User.objects.filter(username=request.POST['username']).exists():
            if not User.objects.filter(email=request.POST['email']).exists():
                code = get_random_string(length=32)
                #now = datetime.now()
                email= request.POST['email']
                password = make_password(request.POST['password'])
                username = request.POST['username']
                temporarycode = Passwordresetcodes(
                    email=email, code=code, username=username, password=password)
                temporarycode.save()
                message = ' Wellcome '
                body = " برای فعال کردن اکانت خود روی لینک روبرو کلیک کنید: <a href=\"{}?code={}\">لینک رو به رو</a> ".format(request.build_absolute_uri('/accounts/register/'), code)
                message = message + body
                context = {
                    'message': message }
                return render(request, 'index.html', context)
            else:
                context = {
                    'message': 'متاسفانه این شماره دانشجوی قبلا استفاده شده است. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
                # TODO: keep the form data
                return render(request, 'register.html', context)
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)

    elif request.GET.__contains__('code'):  # user clicked on code
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(
                code=code).exists():  # if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password,
                                          email=new_temp_user.email)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)
            # delete the temporary activation code from db
            Passwordresetcodes.objects.filter(code=code).delete()
            massage = ' .اکانت شما با موفقیت ساخته شد'
            head = ' توکن شماعبارت است از : {}'.format(this_token)
            body = '  آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی'
            massage = massage + head + body 
            context = {
                'message': massage 
            }
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'register.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)

def index(request):
    post_list_l= post.objects.all().order_by('-date')[0:4]
    post_list_m= post.objects.all().order_by('-date')[4:8]
    post_list_r= post.objects.all().order_by('-date')[8:12]
    
    context = {
        'posts_l': post_list_l,
        'posts_m': post_list_m,
        'posts_r': post_list_r,
    }
    return render(request , 'index.html' , context )

#class PostListView(ListView):   
 #   model = post
## template_name = 'index.html'
 #   context_object_name = 'posts'
 #   ordering = ['-date']