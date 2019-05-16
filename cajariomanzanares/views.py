from django.shortcuts import render
from .models import Registros, Caja, Veterinarios
from datetime import datetime, timedelta
from .forms import RegistrosForm
from django.http import HttpResponse
from django.db import connection


# Create your views here.

def index(request):
    return render(request, 'index.html')


def registros(request, idVet):

    if request.method != "POST":
        return render(request, 'cajaRioManazanares.html', {'idVet': idVet})
    else:

        idRegistro = Registros.objects.filter(idRegistro__isnull=False).values_list('idRegistro').last()
        try:
            idRegistro = int(idRegistro[0]) + 1
        except:
            idRegistro = 1
            # raise Http404("No Tienes ningún cliente dado de alta")
        if idRegistro < 10:
            idRegistro = '00000'+(str(idRegistro))

        fechaRegistro = datetime.now()
        fechaRegistro = fechaRegistro.strftime("%Y-%m-%d")

        if request.POST.get('nombreMascota'):
            print("Validamos el formulario")
            form = Registros()
            form.idRegistro = idRegistro
            print("ID VETERINARIO: ", idVet)
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



def opciones(request, idVet):
    print("Entra en Opciones   !!!!!")

    for i in Registros.objects.raw('''SELECT idRegistro as idRegistro, max(fechaRegistro) FROM REGISTROS'''):
        print("RegDiaadfasd: ", i.fechaRegistro)
        ultFecha = i.fechaRegistro

    #if str(ultFecha) < datetime.now().strftime("%Y-%m-%d"):
    #    print("No hay registros aún para el día de hoy: ", datetime.now().strftime("%Y-%m-%d"))
    #    noRegistros = 0
    #else:
    #    noRegistros = 1


    return render(request, 'opciones.html', {'idVet' : idVet} )


def hacerCaja(request, idVet):

    print("Entra en hacerCaja  !!!!!!")

    fechaCaja = datetime.now()
    fechaCaja2 = datetime.now() - timedelta(days=1)
    fechaCaja = fechaCaja.strftime("%Y-%m-%d")
    fechaCaja2 = fechaCaja2.strftime("%Y-%m-%d")

    print("Fecha Caja 2: ", fechaCaja2)
    print("Fecha Caja: ", fechaCaja)

    if request.method != "POST":

        return render(request, 'hacerCaja.html', {'idVet': idVet})

    else:

        cajaDia = Caja.objects.filter(consulta__startswith=request.POST.get('consulta'), periodo__startswith=request.POST.get('periodo'), fechaCaja=fechaCaja).values()

        #for cajaDia in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja From Caja where consulta = %s
        #                                    and periodo = %s and fechaCaja = %s ''', [request.POST.get('consulta'),
        #                                                                             request.POST.get('periodo'),
        #                                                                             fechaCaja2]):
        print(cajaDia)

        if cajaDia:
            print("YA EXISTE LA CAJA")
            existe = 1
            return render(request, 'hacerCaja.html', {'existe': existe, 'idVet': idVet})
        else:
            print("NO EXISTE LA CAJAAAAAA")
            registrosConsulta = Registros.objects.filter(consulta__startswith=request.POST.get('consulta'),
                                          fechaRegistro=fechaCaja).values()
            #for registrosConsulta in Registros.objects.raw('''SELECT idRegistro as idRegistro FROM Registros
            #                                               where consulta = %s and fechaRegistro = %s ''',
            #                                               [request.POST.get('consulta'), fechaCaja]):
            if not registrosConsulta:
                print("NO HAY REGISTROS PARA PODER HACER LA CAJA")
                noReg = 1
                consulta = request.POST.get('consulta')
                return render(request, 'hacerCaja.html', {'noReg': noReg, 'consulta': consulta})
            else:

                sumaCampoDia = 0
                for campoDia in Registros.objects.raw(''' SELECT idRegistro as idRegistro FROM Registros 
                                                             where metodoPago = 'E' and fechaRegistro = %s ''', [fechaCaja]):
                    sumaCampoDia = sumaCampoDia + float(campoDia.importe)

                print("sumaCampoDia: ", sumaCampoDia)

                cajaRealizada = Caja.objects.filter(fechaCaja=fechaCaja2).values()

                #for cajaRealizada in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja FROM Caja
                #                                where fechaCaja = %s ''', [fechaCaja2]):

                print("ENTRA EN EL FOR")

                if cajaRealizada:
                    print("ENTRA EN CAJAREALIZADA.FECHACAJA")

                    #   REALIZAR QUERY PARA EL DÍA ANTERIOR AL QUE ACTUALMENTE SE ESTÁ  #
                    sumaCampoTotal = 0
                    for maxFechaCaja in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja FROM Caja
                                                        where fechaCaja = %s ''', [fechaCaja2]):
                        #ultFechaCaja = Caja.objects.filter(mod_date__gt=('fechaRegistro') - timedelta(days=1))
                        print("MAXFECHA ACTUAL: ", maxFechaCaja.fechaCaja)
                        if maxFechaCaja.fechaCaja is None:
                            print("entra aqui")
                            sumaCampoTotal = 0
                        else:
                            for campoMonedas in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja FROM Caja
                                                                where fechaCaja = %s and consulta = %s ''', [fechaCaja2, request.POST.get('consulta')]):
                                print("Numero de Monedas: ", campoMonedas.impMonedas)
                                sumaCampoTotal = sumaCampoTotal + int(campoMonedas.impMonedas)

                            for campoBilletes in Caja.objects.raw('''SELECT idRegistroCaja as idRegistroCaja FROM Caja
                                                                where fechaCaja = %s and consulta = %s ''', [fechaCaja2, request.POST.get('consulta')]):
                                print("Numero de Billetes: ", campoBilletes.impBilletes)
                                sumaCampoTotal = sumaCampoTotal + int(campoBilletes.impBilletes)


                    print("sumaCampoTotal: ", sumaCampoTotal)
                    sumaCampoTotal = sumaCampoTotal + sumaCampoDia


                    idRegistroCaja = Caja.objects.filter(idRegistroCaja__isnull=False).values_list('idRegistroCaja').last()
                    try:
                        idRegistroCaja = int(idRegistroCaja[0]) + 1
                    except:
                        idRegistroCaja = 1
                        # raise Http404("No Tienes ningún cliente dado de alta")
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
                    print("NO EXISTE LA CAJA DEL DÍA ANTERIOR")
                    noReg2 = 2
                    consulta = request.POST.get('consulta')
                    return render(request, 'hacerCaja.html', {'noReg2': noReg2, 'consulta': consulta})



    return render(request, 'index.html')



def mostrarCaja(request):

    fechaCaja = datetime.now()
    fechaCaja = fechaCaja.strftime("%Y-%m-%d")

    print("Entra en MOSTRARCAJA !!!!")

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

