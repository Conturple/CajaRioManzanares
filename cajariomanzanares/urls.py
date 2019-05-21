from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),    # Página princial.
    path('registros/<int:idVet>/', views.registros, name="registros"),  # Crear un nuevo Registro

    path('opciones/<int:idVet>/', views.opciones, name="opciones"),     # Muestra el conjunto de opciones de la
                                                                        # aplicación.

    path('hacerCaja/<int:idVet>/', views.hacerCaja, name="hacerCaja"),  # Crea una nueva Caja

    path('mostrarCaja', views.mostrarCaja, name="mostrarCaja"),     # Muestra el conjunto de operaciones de cada una de
                                                                    # las consultas.

]

