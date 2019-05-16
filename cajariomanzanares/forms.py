from django import forms
from .models import Registros, Caja


class RegistrosForm(forms.ModelForm):

    class Meta:
        model = Registros
        fields = ["idRegistro", "idVet", "consulta", "fechaRegistro", "nombreMascota", "nombreCliente", "operacion",
                  "importe", "metodoPago"]


class CajaForm(forms.ModelForm):

    class Meta:
        model = Caja
        fields = ["idRegistroCaja", "idVet", "periodo", "fechaCaja", "campoDia", "campoTotal", "campoCaja", "impMonedas",
                  "impBilletes"]