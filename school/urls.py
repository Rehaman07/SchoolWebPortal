from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('updates/', views.updates, name='updates'),
    path('admissions/', views.admissions, name='admissions'),
    path('contact/', views.contact, name='contact'),
]
