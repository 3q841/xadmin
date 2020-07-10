from django.urls import path
#from .views import PostListView
from . import views
#from django.conf import settings

urlpatterns = [
    path('blog/exp/', views.sub_qustion, name='user-ans'),
    path('accounts/register/', views.register, name = 'register'),
    path('', views.index , name='index'),
]
"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""