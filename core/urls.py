from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('prediction/', views.prediction, name='prediction'),

    path('weather/', views.weather, name='weather'),

    

    path('manual-soil/', views.manual_soil, name='manual_soil'),

    path('soil-scan/', views.soil_scan, name='soil_scan'),

    

    path('reports/', views.reports, name='reports'),
    path('about/', views.about, name='about'),
    path('irrigation/', views.irrigation, name='irrigation'),
]