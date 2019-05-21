from django.shortcuts import render
from .models import Registros, Caja, Veterinarios
from datetime import datetime, timedelta
from .forms import RegistrosForm
from django.http import HttpResponse
from django.db import connection


# Create your views here.


''' 
Método de inicio para que se muestre la pantalla inicial.
Esta pantalla hace referencia a cada una de las veterinarias que componen la cĺinica
'''
def index(request):
    return render(request, 'index.html')



''' 
Método que en primera instancia muestra el formulario con los campos necesarios para un nuevo REGISTROS
En segunda instancia, valida el formulario con los datos introducidos. En caso de no introducir correctamente los 
valores, se muestra un mensaje de error (form is not validated) en el navegador
'''
def registros(request, idVet):

    if request.method != "POST":
        return render(request, 'cajaRioManazanares.html', {'idVet': idVet})
    else:

        idRegistro = Registros.objects.filter(idRegistro__isnull=False).values_list('idRegistro').last()
        try:
            idRegistro = int(idRegistro[0]) + 1
        except:
            idRegistro = 1
        if idRegistro < 10:
            idRegistro = '00000'+(str(idRegistro))

        fechaRegistro = datetime.now()
        fechaRegistro = fechaRegistro.strftime("%Y-%m-%d")


        # Validación del formulario para poder guardar un nuevo registro introducido.

        if request.POST.get('nombreMascota'):
            form = Registros()
            form.idRegistro = idRegistro
            form.idVet = idVet
            form.consulta = request.POST.get('consulta')
            form.fechaRegistro = fechaRegistro
            form.nombreMascota = request.POST.get('nombreMascota')
            form.nombreCliente = request.POST.get('nombreCliente')
            form.operacion = request.POST.get('operacion')
            form.importe = request.POST.get('importe')
            form.metodoPago = request.POST.get('metodoPago')

            u = form.save()
            registro = Registros.objects.all()
            context = {'registro': registro}
            return render(request, 'index.html', context)
        else:
            return HttpResponse("form is not validated")

    return render(request, 'index.html', {})


'''
Método que muestra las opciones disponible: 
    1. Crear Nuevo Registro.
    2. Hacer Caja.
    3. Mostrar Cajas.
'''
def opciones(request, idVet):

    return render(request, 'opciones.html', {'idVet': idVet})


''' 
Método que en primera instancia muestra el formulario con los campos necesarios para una nueva CAJA.
En segunda instancia, valida el formulario con los datos introducidos. En caso de no introducir correctamente los 
valores, se muestra un mensaje de error (form is not validated) en el navegador
'''
def hacerCaja(request, idVet):

    fechaCaja = datetime.now()
    fechaCaja2 = datetime.now() - timedelta(days=1)
    fechaCaja = fechaCaja.strftime("%Y-%m-%d")
    fechaCaja2 = fechaCaja2.strftime("%Y-%m-%d")

    if request.method != "POST":

        return render(request, 'hacerCaja.html', {'idVet': idVet})

    else:

        cajaDia = Caja.objects.filter(consulta__startswith=request.POST.get('consulta'),
                                      periodo__startswith=request.POST.get('periodo'), fechaCaja=fechaCaja).values()

        if cajaDia:
            existe = 1
            return render(request, 'hacerCaja.html', {'existe': existe, 'idVet': idVet})
        else:
            registrosConsulta = Registros.objects.filter(consulta__startswith=request.POST.get('consulta'),
                                                         fechaRegistro=fechaCaja).values()

            if not registrosConsulta:
                noReg = 1
                consulta = request.POST.get('consulta')
                return render(request, 'hacerCaja.html', {'noReg': noReg, 'consulta': consulta})
            else:
                sumaCampoDia = 0
                for campoDia in Registros.objects.raw(''' SELECT idRegistro as idRegistro FROM Registros 
                                                             where metodoPago = 'E' and fechaRegistro = %s ''',
                                                      [fechaCaja]):

                    sumaCampoDia = sumaCampoDia + float(campoDia.importe)

                cajaRealizada = Caja.objects.filter(fechaCaja=fechaCaja2).values()

                if cajaRealizada:

                    #   REALIZAR QUERY PARA EL DÍA ANTERIOR AL QUE ACTUALMENTE SE ESTÁ  #
                    sumaCampoTotal = 0
                    for maxFechaCaja in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja FROM Caja
                                                        where fechaCaja = %s ''', [fechaCaja2]):
                        #ultFechaCaja = Caja.objects.filter(mod_date__gt=('fechaRegistro') - timedelta(days=1))
                        if maxFechaCaja.fechaCaja is None:
                            sumaCampoTotal = 0
                        else:
                            for campoMonedas in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja FROM Caja
                                                                where fechaCaja = %s and consulta = %s ''', [fechaCaja2, request.POST.get('consulta')]):
                                sumaCampoTotal = sumaCampoTotal + int(campoMonedas.impMonedas)

                            for campoBilletes in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja FROM Caja
                                                                where fechaCaja = %s and consulta = %s ''', [fechaCaja2, request.POST.get('consulta')]):
                                sumaCampoTotal = sumaCampoTotal + int(campoBilletes.impBilletes)


                    sumaCampoTotal = sumaCampoTotal + sumaCampoDia


                    idRegistroCaja = Caja.objects.filter(idRegistroCaja__isnull=False).values_list('idRegistroCaja').last()
                    try:
                        idRegistroCaja = int(idRegistroCaja[0]) + 1
                    except:
                        idRegistroCaja = 1
                    if idRegistroCaja < 10:
                        idRegistroCaja = '00000' + (str(idRegistroCaja))

                    fechaCaja = datetime.now()
                    fechaCaja = fechaCaja.strftime("%Y-%m-%d")

                    if request.POST.get('periodo'):
                        formCaja = Caja()
                        formCaja.idRegistroCaja = idRegistroCaja
                        formCaja.idVet = idVet
                        formCaja.consulta = request.POST.get('consulta')
                        formCaja.periodo = request.POST.get('periodo')
                        formCaja.fechaCaja = fechaCaja
                        formCaja.campoDia = sumaCampoDia
                        formCaja.campoTotal = sumaCampoTotal
                        formCaja.campoCaja = sumaCampoTotal
                        formCaja.impMonedas = request.POST.get('impMonedas')
                        formCaja.impBilletes = request.POST.get('impBilletes')

                        x = formCaja.save()

                        return render(request, 'index.html')
                    else:
                        return HttpResponse("form is not validated")
                else:
                    noReg2 = 2
                    consulta = request.POST.get('consulta')
                    return render(request, 'hacerCaja.html', {'noReg2': noReg2, 'consulta': consulta})



    return render(request, 'index.html')


''' 
Método que visualiza en forma de tabla, el conjunto de operaciones que cada una de las consultas ha realizado hasta
el momento.
'''
def mostrarCaja(request):

    fechaCaja = datetime.now()
    fechaCaja = fechaCaja.strftime("%Y-%m-%d")


    cursorPri = connection.cursor()
    cursorSeg = connection.cursor()
    cursorPri.execute('''SELECT nombreMascota as nombreMascota, nombreCliente as nombreCliente, operacion as operacion, 
                    importe as importe, metodoPago as metodoPago FROM Registros where fechaRegistro = %s 
                    and consulta = 1 ''', [fechaCaja])

    cursorSeg.execute('''SELECT nombreMascota as nombreMascota, nombreCliente as nombreCliente, operacion as operacion, 
                    importe as importe, metodoPago as metodoPago FROM Registros where fechaRegistro = %s 
                    and consulta = 2 ''', [fechaCaja])

    regPrimeraConsulta = cursorPri.fetchall()
    regSegundaConsulta = cursorSeg.fetchall()


    return render(request, 'mostrarCaja.html', {'regPrimeraConsulta': regPrimeraConsulta, 'regSegundaConsulta': regSegundaConsulta})

