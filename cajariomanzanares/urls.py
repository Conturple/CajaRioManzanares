from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('registros/<int:idVet>/', views.registros, name="registros"),

    path('opciones/<int:idVet>/', views.opciones, name="opciones"),
    path('hacerCaja/<int:idVet>/', views.hacerCaja, name="hacerCaja"),


    path('mostrarCaja', views.mostrarCaja, name="mostrarCaja"),

]

