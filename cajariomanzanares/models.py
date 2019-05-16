from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

METODOPAGO = (
    ('T', 'Tarjeta'),
    ('E', 'Efectivo'),
)

CONSULTA = (
    ('1', 'Consulta1'),
    ('2', 'Consulta2'),
)

PERIODO = (
    ('M', 'Mañana'),
    ('T', 'Tarde'),
)


class Veterinarios(models.Model):

    idVet = models.CharField(max_length=2, primary_key=True, null=False, verbose_name="Id Veterinario")
    nombreVet = models.CharField(max_length=15, null=False, verbose_name="Nombre Veterinario")
    apellidosVet = models.CharField(max_length=30, null=False, verbose_name="Apellidos Veterinario")


    class Meta:
        db_table = "Veterinarios"

    def __str__(self):
        return self.idVet + ' ' + self.nombreVet + ' ' + self.apellidosVet


class Registros(models.Model):

    idRegistro = models.CharField(max_length=6, primary_key=True, null=False, verbose_name="Id Registro")
    idVet = models.CharField(max_length=2, null=False, verbose_name="Id Veterinario")
    consulta = models.CharField(max_length=1, choices=CONSULTA, null=False, verbose_name="Consulta")
    fechaRegistro = models.DateField(auto_now_add=False, null=False, verbose_name="Fecha Registgro")
    nombreMascota = models.CharField(max_length=30, null=False, verbose_name="Nombre Mascota")
    nombreCliente = models.CharField(max_length=50, null=False, verbose_name="Nombre Cliente")
    operacion = models.CharField(max_length=50, null=False, verbose_name="Descripción Operación")
    importe = models.CharField(max_length=8, null=False, validators=[RegexValidator(r'^\?<=>\d+.\d+|\d+$')], verbose_name="Importe")
    metodoPago = models.CharField(max_length=1, choices=METODOPAGO, null=False, verbose_name="Método Pago")


    class Meta:
        db_table = "Registros"

    def __str__(self):
        return str(self.importe)

class Caja(models.Model):

    idRegistroCaja = models.CharField(max_length=6, primary_key=True, null=False, verbose_name="Id Registro Caja")
    idVet = models.CharField(max_length=2, null=False, verbose_name="Id Veterinario")
    consulta = models.CharField(max_length=1, choices=CONSULTA, null=False, verbose_name="Consulta")
    periodo = models.CharField(max_length=1, choices=PERIODO, null=False, verbose_name="Periodo")
    fechaCaja = models.DateField(auto_now_add=False, null=False, verbose_name="Fecha Caja")
    campoDia = models.CharField(max_length=8, validators=[RegexValidator(r'^\?<=>\d+.\d+|\d+$')], null=False, verbose_name="Caja Dia")
    campoTotal = models.CharField(max_length=8, validators=[RegexValidator(r'^\?<=>\d+.\d+|\d+$')], null=False, verbose_name="Caja Total")
    campoCaja = models.CharField(max_length=8, validators=[RegexValidator(r'^\?<=>\d+.\d+|\d+$')], null=False, verbose_name="Caja")
    impMonedas = models.CharField(max_length=8, validators=[RegexValidator(r'^\?<=>\d+.\d+|\d+$')], null=False, verbose_name="Importe Monedas")
    impBilletes = models.CharField(max_length=8, validators=[RegexValidator(r'^\?<=>\d+.\d+|\d+$')], null=False, verbose_name="Importe Billetes")


    class Meta:
        db_table = "Caja"


    def __str__(self):
        return self.idVet + ' ' + self.periodo + ' ' + str(self.fechaCaja) \
                + ' ' + str(self.campoDia) + ' ' + str(self.campoTotal) + ' ' + str(self.campoCaja) \
                + ' ' + str(self.impMonedas) + ' ' + str(self.impBilletes)

