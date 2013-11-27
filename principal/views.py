# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from forms import *
from models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import date

import json


from geraldo import Report, ReportBand, DetailBand, SystemField, Label, ObjectValue
from geraldo.utils import cm
from geraldo.generators import PDFGenerator

from django.http import HttpResponse    
from reports import lista_alumnos,lista_evaluaciones
from geraldo.generators import PDFGenerator

from django.shortcuts import redirect

from django.core.mail import EmailMessage


def inicio(request):

    usuario = request.user
    formulario = InicioForm()
    error = []
    if not request.user.is_anonymous():

        if usuario.clasificacion ==  'Alumnos':
            return HttpResponseRedirect("alumno/alumnoInicio")
        elif usuario.clasificacion ==  'Profesores':
            return HttpResponseRedirect("profesor_main/")
        elif usuario.clasificacion ==  'Empleado_escolar':
            return HttpResponseRedirect("control/control_main")

    if request.method == "POST":
        formulario = InicioForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.cleaned_data["usuario"]
            password = formulario.cleaned_data["password"]
            acceso = authenticate(username=str(usuario), password=str(password))
            if acceso is not None:          
                if acceso.is_active:
                    login(request, acceso)
                    usuario = request.user
                    return HttpResponseRedirect(reverse('inicio'))
                else:
                    error.append("Tu usuario esta desactivado")     
            else:
                error.append('Usuario o contraseña incorrecta')
        else:
            error.append('Usuario o contraseña incorrecta')
    return render(request, 'login.html',locals())

@login_required(login_url='/inicio')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

def pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def color(materia):
    if(materia.materia.clasificacion=='Institucional'):
        return 'm1'

    elif(materia.materia.clasificacion=='Cientifica_basica'):
        return 'm4'

    elif(materia.materia.clasificacion=='Profesional'):
        return 'm3'

    elif(materia.materia.clasificacion=='Terminal_integración'):
        return 'm2'
    else:
        return 'm3'

@login_required(login_url='/inicio')
def profesor_main(request):
    try:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        Materias=MateriaImpartidaEnGrupo.objects.filter(profesor__cve_usuario=profesor)
        for materia in Materias:

            if(materia.horario.cve_horario==1):
                materia1=materia.materia.nombre
                m1=color(materia)
                grupo1=materia.grupo
            elif(materia.horario.cve_horario==2):
                materia2=materia.materia.nombre
                m2=color(materia)
                grupo2=materia.grupo
            elif(materia.horario.cve_horario==3):
                materia3=materia.materia.nombre
                m3=color(materia)
                grupo3=materia.grupo
            elif(materia.horario.cve_horario==4):
                materia4=materia.materia.nombre
                m4=color(materia)
                grupo4=materia.grupo
            elif(materia.horario.cve_horario==5):
                materia5=materia.materia.nombre
                m5=color(materia)
                grupo5=materia.grupo
            elif(materia.horario.cve_horario==6):
                materia6=materia.materia.nombre
                m6=color(materia)
                grupo6=materia.grupo
            elif(materia.horario.cve_horario==7):
                materia7=materia.materia.nombre
                m7=color(materia)
                grupo7=materia.grupo
            elif(materia.horario.cve_horario==8):
                materia8=materia.materia.nombre
                m8=color(materia)
                grupo8=materia.grupo
            
            if(materia.horario.cve_horario==9):
                materia9=materia.materia.nombre
                m9=color(materia)
                grupo9=materia.grupo
            elif(materia.horario.cve_horario==10):
                materia10=materia.materia.nombre
                m10=color(materia)
                grupo10=materia.grupo
            elif(materia.horario.cve_horario==11):
                materia11=materia.materia.nombre
                m11=color(materia)
                grupo11=materia.grupo
            elif(materia.horario.cve_horario==12):
                materia12=materia.materia.nombre
                m12=color(materia)
                grupo12=materia.grupo
            elif(materia.horario.cve_horario==13):
                materia13=materia.materia.nombre
                m13=color(materia)
                grupo13=materia.grupo
            elif(materia.horario.cve_horario==14):
                materia14=materia.materia.nombre
                m14=color(materia)
                grupo14=materia.grupo
            elif(materia.horario.cve_horario==15):
                materia15=materia.materia.nombre
                m15=color(materia)
                grupo15=materia.grupo

        es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
        es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
        es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
        hoy=date.today()
        f=calendarios.objects.all()
        for i in f:
            inicio_ets=i.inicetes
            fin_ets=i.finets 
            inicio_extra=i.inicextra
            fin_extra=i.finextra
            inicio_ordinario=i.inicord
            fin_ordinario=i.finord
            inicio_saberes=i.inicperiodo

        if(hoy >= inicio_ets and hoy <= fin_ets):
            #fechas de ets
            ets=1;
        else:
            ets=0;


        if(hoy >= inicio_extra and hoy <= fin_extra):
            #fechas de extra
            extra=1;
        else:
            extra=0;

        if(hoy >= inicio_ordinario and hoy <= fin_ordinario):
            #fechas de ordinario
            ordinaria=1;
        else:
            ordinaria=0;

        if(hoy >= inicio_saberes and hoy <= inicio_ordinario):
            #fechas de saberes previos
            saberes=1;
        else:
            saberes=0;

        print "FEchas---------------"
        print ets
        print extra
        print ordinaria



        return render(request, 'profesor/main.html',locals(),context_instance=RequestContext(request))
    except:
        mensaje=1
        return render(request, 'profesor/main.html',locals(),context_instance=RequestContext(request))

@login_required(login_url='/inicio')    
def profesor_miperfil(request):
    try:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        materias_coordina=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario)
        profesor2=Profesor.objects.get(cve_usuario=profesor)
        materias=MateriaImpartidaEnGrupo.objects.filter(profesor=profesor2)
        tutorados=Alumno.objects.filter(tutor_escolar=profesor2)
        es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
        es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
        es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
        foto=profesor2.cve_usuario.foto
        num=0
        for alumno in tutorados:
            num+=1
        num=8-num
        return render_to_response('profesor/mi-perfil.html',locals(),context_instance=RequestContext(request))
    except:
        mensaje=1
        return render_to_response('profesor/mi-perfil.html',locals(),context_instance=RequestContext(request))

def guarda_miperfil(request):
    try:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        grupos=MateriaImpartidaEnGrupo.objects.filter(profesor=profesor)
        profesor2=Profesor.objects.get(cve_usuario=profesor)
        es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
        es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
        es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
        
        correo=request.GET['email']
        telefono=request.GET['telefono']
        hentrada=request.GET['entrada']
        hsalida=request.GET['salida']
        try:
            foto="fotos/"+request.GET['imagen']
        except:
            foto=profesor2.cve_usuario.foto
        usuario=Usuario.objects.filter(clave=profesor).update(email_personal=correo,Telefono_Casa=telefono, foto=foto)
        p=Profesor.objects.filter(cve_usuario=profesor).update(hora_entrada=hentrada,hora_salida=hsalida)

        profesor2=Profesor.objects.get(cve_usuario=profesor)
        materias=MateriaImpartidaEnGrupo.objects.filter(profesor=profesor2)
        tutorados=Alumno.objects.filter(tutor_escolar=profesor2)
        foto=profesor2.cve_usuario.foto
        num=0
        for alumno in tutorados:
            num+=1
        num=8-num
        mensaje=1
        return render_to_response('profesor/mi-perfil2.html',locals(),context_instance=RequestContext(request))
    except:
        mensaje=2
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        profesor2=Profesor.objects.get(cve_usuario=profesor)
        materias=MateriaImpartidaEnGrupo.objects.filter(profesor=profesor2)
        tutorados=Alumno.objects.filter(tutor_escolar=profesor2)
        foto=profesor2.cve_usuario.foto
        num=0
        for alumno in tutorados:
            num+=1
        num=8-num
        return render_to_response('profesor/mi-perfil2.html',locals(),context_instance=RequestContext(request))


def profesor_miperfil2(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    profesor2=Profesor.objects.get(cve_usuario=profesor)
    grupos=MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    return render_to_response('profesor/mi-perfil2.html',locals(),context_instance=RequestContext(request))


def profesor_preferencias(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    prof=Profesor.objects.get(cve_usuario=profesor)
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    return render_to_response('profesor/preferencias.html',locals(),context_instance=RequestContext(request))


def guardar_preferencias(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    comentario=request.GET['preferencias']
    p=Profesor.objects.filter(cve_usuario=profesor).update(comentario=comentario)
    prof=Profesor.objects.get(cve_usuario=profesor)
    mensaje=1
    return render_to_response('profesor/preferencias.html',locals(),context_instance=RequestContext(request))

def profesor_logout(request):
    return render_to_response('profesor/logout.html',locals(),context_instance=RequestContext(request))

def profesor_mis_grupos(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()

    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    return render_to_response('profesor/mis-grupos.html',locals(),context_instance=RequestContext(request))

def profesor_registrar_calificaciones(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.get(cve_usuario = profesor)
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    grupolist = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    return render_to_response('profesor/registrar-calificaciones.html',locals(),context_instance=RequestContext(request))

def profesor_registrar_calificaciones_extra(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    grupolist = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    return render_to_response('profesor/registrar-calificacionesExtra.html',locals(),context_instance=RequestContext(request))

def profesor_registrar_calificaciones_ets(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materias_ets=Ets.objects.filter(cve_materia__coordinador__cve_usuario=atributos_profesor.cve_usuario)
    return render_to_response('profesor/registrar-calificacionesETS.html',locals(),context_instance=RequestContext(request))




def directorio(request):
    profesoresList= Profesor.objects.all()
    materiasList= Materia.objects.all()
    gruposList= Grupo.objects.all()
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    return render_to_response('directorio.html',locals(),context_instance=RequestContext(request))

def profesor_reportes_PRUI08_1(request):
  
    profesor=request.user
    atributos_profesor = Profesor.objects.get(cve_usuario = profesor)
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    grupolist = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    return render_to_response('profesor/reportes/PRUI08.1.html',locals(),context_instance=RequestContext(request))

def profesor_reportes_PRUI08_2(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.get(cve_usuario = profesor)
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    grupolist = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    return render_to_response('profesor/reportes/PRUI08.2.html',locals(),context_instance=RequestContext(request))

def profesor_calendario(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    return render_to_response('profesor/calendario.html',locals(),context_instance=RequestContext(request))

def profesor_tutorias(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    Tutorado=Alumno.objects.filter(tutor_escolar=atributos_profesor)
    return render_to_response('profesor/tutorias.html',locals(),context_instance=RequestContext(request))

def profesor_ingresa_calificacion(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materia=request.GET['materia']
    materiaGrupo = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    materiaGrupo = materiaGrupo.filter(id=materia)[0]
    request.session["materiaGrupo"] = materiaGrupo
    request.session["materia"] = materia
    alumnos = AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=materiaGrupo)
    #print alumnos.values()
    return render_to_response('profesor/IngresaCalificacion.html',locals(),context_instance=RequestContext(request))

def profesor_ingresa_calificacion_extra(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materia=request.GET['materia']
    materiaGrupo1 = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    materiaGrupo = materiaGrupo1.filter(id=materia)
    request.session["materiaGrupo"] = materiaGrupo
    request.session["materia"] = materia
    print materia
    print materiaGrupo
    alumnos = AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=materiaGrupo)

    return render_to_response('profesor/IngresaCalificacionExtra.html',locals(),context_instance=RequestContext(request))

def profesor_ingresa_calificacion_ets(request):
    profesor=request.user
    calificaciones=request.GET
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materia=request.GET['materia']
    ets = Ets.objects.filter(id=int(materia))[0]
    request.session["ets_aplicado"] = ets
    alumnos = AlumnoTomaEts.objects.filter(ets__id=int(materia))
    return render_to_response('profesor/IngresaCalificacionETS.html',locals(),context_instance=RequestContext(request))

def profesor_guarda_calificacion(request):
    calificaciones=request.GET
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    grupolist = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    
    materiaGrupo = request.session["materiaGrupo"]
    materia = request.session["materia"]
    alumnos = AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=materiaGrupo)
    for alumno in calificaciones:
        p=alumnos.filter(alumno_id=alumno).update(calificacion=calificaciones.get(alumno))
    mensaje=1
    return render_to_response('profesor/IngresaCalificacion.html',locals(),context_instance=RequestContext(request))



def profesor_guarda_calificacionExtra(request):
    calificaciones=request.GET
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    grupolist = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor)
    materiaGrupo = request.session["materiaGrupo"]
    alumnos = AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=materiaGrupo)
    for alumno in calificaciones:
        p=alumnos.filter(alumno_id=alumno).update(calificacionExtra=calificaciones.get(alumno))
    mensaje=1
    return render_to_response('profesor/IngresaCalificacionExtra.html',locals(),context_instance=RequestContext(request))

def profesor_guarda_calificacionETS(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    calificaciones=request.GET
    ets = request.session["ets_aplicado"]
    for alumno in calificaciones:
        p=AlumnoTomaEts.objects.filter(ets__id=ets.id,alumno_id=alumno).update(calificacion=calificaciones.get(alumno))
    mensaje=1
    alumnos = AlumnoTomaEts.objects.filter(ets__id=ets.id)
    return render_to_response('profesor/IngresaCalificacionETS.html',locals(),context_instance=RequestContext(request))

def perfiles_profesor(request):
        try:
            profesor=request.user
            atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
            cvep=request.GET['prof']
            es_coordinador=Materia.objects.filter(coordinador__cve_usuario__clave=cvep).count()
            es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
            es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
            profesor2=Profesor.objects.get(cve_usuario__clave=cvep)
            materias_coordina=Materia.objects.filter(coordinador__cve_usuario__clave=cvep)
            materias=MateriaImpartidaEnGrupo.objects.filter(profesor=profesor2)
            tutorados=Alumno.objects.filter(tutor_escolar=profesor2)
            num=0
            for alumno in tutorados:
                num+=1
            num=8-num
            return render_to_response('perfiles/maldonadoCastilloIdalia.html',locals(),context_instance=RequestContext(request))
        except:
            profesoresList= Profesor.objects.all()
            materiasList= Materia.objects.all()
            gruposList= Grupo.objects.all()
            profesor=request.user
            atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
            mensaje=1
            return render_to_response('directorio.html',locals(),context_instance=RequestContext(request))
            

def perfiles_materia(request):
    try:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        infmat=request.GET['mat']
        es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
        es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
        es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
        materia2=Materia.objects.get(nombre=infmat)
        materias=MateriaImpartidaEnGrupo.objects.filter(materia=materia2)

        return render_to_response('perfiles/ingenieria-de-software.html',locals(),context_instance=RequestContext(request))

    except:
        profesoresList= Profesor.objects.all()
        materiasList= Materia.objects.all()
        gruposList= Grupo.objects.all()
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        mensaje=1
        return render_to_response('directorio.html',locals(),context_instance=RequestContext(request))

def perfiles_grupo(request):
    try:
        idg=request.GET['grup']
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
        es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()        
        es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
        materias=MateriaImpartidaEnGrupo.objects.filter(grupo__cve_grupo=idg)
        grupo=Grupo.objects.get(cve_grupo=idg)
        turno=grupo.turno
        print turno
        for materia in materias:
            if(turno=='Matutino'):
                print materia.horario.cve_horario
                if(materia.horario.cve_horario==1):
                    materia1=materia.materia.nombre
                    m1=color(materia)
                    prof1=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==2):
                    materia2=materia.materia.nombre
                    m2=color(materia)
                    prof2=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==3):
                    materia3=materia.materia.nombre
                    m3=color(materia)
                    prof3=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==4):
                    materia4=materia.materia.nombre
                    m4=color(materia)
                    prof4=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==5):
                    materia5=materia.materia.nombre
                    m5=color(materia)
                    prof5=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==6):
                    materia6=materia.materia.nombre
                    m6=color(materia)
                    prof6=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==7):
                    materia7=materia.materia.nombre
                    m7=color(materia)
                    prof7=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==8):
                    materia8=materia.materia.nombre
                    m8=color(materia)
                    prof8=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
            else:
                if(materia.horario.cve_horario==9):
                    materia9=materia.materia.nombre
                    m9=color(materia)
                    prof9=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==10):
                    materia10=materia.materia.nombre
                    m10=color(materia)
                    prof10=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==11):
                    materia11=materia.materia.nombre
                    m11=color(materia)
                    prof11=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==12):
                    materia12=materia.materia.nombre
                    m12=color(materia)
                    prof12=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==13):
                    materia13=materia.materia.nombre
                    m13=color(materia)
                    prof13=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==14):
                    materia14=materia.materia.nombre
                    m14=color(materia)
                    prof14=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                elif(materia.horario.cve_horario==15):
                    materia15=materia.materia.nombre
                    m15=color(materia)
                    prof15=materia.profesor.cve_usuario.nombre+" "+materia.profesor.cve_usuario.apellidoPaterno+" "+materia.profesor.cve_usuario.apellidoMaterno
                
        return render_to_response('perfiles/3CM5.html',locals(),context_instance=RequestContext(request)) 
    except:
            profesoresList= Profesor.objects.all()
            materiasList= Materia.objects.all()
            gruposList= Grupo.objects.all()
            profesor=request.user
            atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
            mensaje=1
            return render_to_response('directorio.html',locals(),context_instance=RequestContext(request))

def profesor_tutorias_comentar(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    cont =0
    Tutorado=ComentarioTutorado.objects.filter(profesor=atributos_profesor)
    return render_to_response('profesor/comentar-tutoria.html',locals(),context_instance=RequestContext(request))

def guardar_comentarios(request):
    try:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
        es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
        es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
        cont =0
        usuario = request.user
        Tutorado=ComentarioTutorado.objects.filter(profesor=atributos_profesor)
        comentarios=request.GET
        for alumno in comentarios:
            p=Tutorado.filter(alumno_id=alumno).update(comentario=comentarios.get(alumno))
        mensaje=1
        return render_to_response('profesor/comentar-tutoria.html',locals(),context_instance=RequestContext(request))
    except:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        cont =0
        usuario = request.user
        Tutorado=ComentarioTutorado.objects.filter(profesor=atributos_profesor)
        mensaje=2
        return render_to_response('profesor/comentar-tutoria.html',locals(),context_instance=RequestContext(request))

def profesor_agregar_tutorado(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    return render_to_response('profesor/agregar-tutorado.html',locals(),context_instance=RequestContext(request))

def profesor_tutorias_add(request):
    try:
        profesor=request.user
        aprofesor = Profesor.objects.get(cve_usuario = profesor)
        boleta = request.GET['boleta']
        alumno=Alumno.objects.get(cve_usuario__clave=boleta)
        if alumno.tipo == 'Historico':
            mensaje = 5
            return render_to_response('profesor/agregar-tutorado.html',locals(),context_instance=RequestContext(request))
        elif alumno.tutor_escolar == None:
            alumno.tutor_escolar=aprofesor
            alumno.save()
        else:
            mensaje=4
            return render_to_response('profesor/agregar-tutorado.html',locals(),context_instance=RequestContext(request))
        p = ComentarioTutorado(profesor=aprofesor, alumno=alumno, comentario="")
        p.save()
        mensaje=1
        return render_to_response('profesor/agregar-tutorado.html',locals(),context_instance=RequestContext(request))
    except:
        mensaje=2
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]

        return render_to_response('profesor/agregar-tutorado.html',locals(),context_instance=RequestContext(request))


def reporte_lista(request):
    try:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        materia=request.GET['materia'] 
        materiaGrupo = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor,id=materia)[0]
        request.session["materiaGrupo"] = materiaGrupo
        request.session["materia"] = materia
        alumnos = AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=materiaGrupo)
        resp = HttpResponse(mimetype='application/pdf')
        report = lista_alumnos(queryset=alumnos)
        report.generate_by(PDFGenerator, filename=resp)
        return resp
    except:
            mensaje=1
            return redirect('/profesor_reportes_PRUI08_1')


def reporte_evaluaciones(request):
    try:
        profesor=request.user
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        materia=request.GET['materia'] 
        materiaGrupo = MateriaImpartidaEnGrupo.objects.filter(profesor=atributos_profesor,id=materia)[0]
        request.session["materiaGrupo"] = materiaGrupo
        request.session["materia"] = materia
        alumnos = AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=materiaGrupo)
        resp = HttpResponse(mimetype='application/pdf')
        report = lista_evaluaciones(queryset=alumnos)
        report.generate_by(PDFGenerator, filename=resp)
        return resp
    except:
        mensaje=1
        return redirect('/profesor_reportes_PRUI08_2')



def recuperar_contrasena(request):
    if request.method=='POST':
        formulario = recuperar_pass(request.POST)
        try:    
            if formulario.is_valid():
                titulo = 'Recuperar contraseña SAES'
                clave_usuario = formulario.cleaned_data['clave_usuario']
                try:
                    usuario=Usuario.objects.get(clave=clave_usuario)
                except:
                    mensaje=1 #Mensaje de usuario no encontrado
                    return render_to_response('recuperar_pass.html',locals(), context_instance=RequestContext(request))
                email=usuario.email_institucional
                contrasena_temporal=usuario.clave
                usuario.set_password(contrasena_temporal)
                usuario.save()
                contenido = formulario.cleaned_data['clave_usuario']+' Su contrasena temporal es:' + contrasena_temporal
                print "************1"
                correo = EmailMessage(titulo, contenido, to=[email])
                print "************2"
                correo.send()   
                print "************3"
                mensaje=3 #Mensaje enviado
                return render_to_response('recuperar_pass.html',locals(), context_instance=RequestContext(request))
            else:
                mensaje=4 #Mensaje de error de formulario
                return render_to_response('recuperar_pass.html',locals(), context_instance=RequestContext(request))

        except:
                mensaje=2 #Mensaje de error de conexion
                return render_to_response('recuperar_pass.html',locals(), context_instance=RequestContext(request))
                
    else:
        formulario = recuperar_pass()
        return render_to_response('recuperar_pass.html',{'formulario':formulario}, context_instance=RequestContext(request))



def jefe_depto_horarios(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefe=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario)[0]
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materias=MateriaImpartidaEnGrupo.objects.filter(materia__depto__id=es_jefe.cve_depto.id)
    profesores=Profesor.objects.filter(Departamento__id=es_jefe.cve_depto.id)
    comentarios=[]
    for come in profesores:
        comentarios.append(come.comentario)

    json_list = simplejson.dumps(comentarios)
    return render_to_response('profesor/gestionarHorarios.html',locals(),context_instance=RequestContext(request))



def jefe_depto_guarda_horarios(request):

    materias=request.GET
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefe=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario)[0]
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materias_impartidas=MateriaImpartidaEnGrupo.objects.filter(materia__depto__id=es_jefe.cve_depto.id)
    try:
        for materia in materias:
            if materias.get(materia) =="sinAsignar":
                print "sin asignar"
                p=materias_impartidas.filter(id=materia).update(profesor="")
            else:
                p=materias_impartidas.filter(id=materia).update(profesor=materias.get(materia))
                mensaje=1;

    except:
        mensaje=2;
    materias=MateriaImpartidaEnGrupo.objects.filter(materia__depto__id=es_jefe.cve_depto.id)
    profesores=Profesor.objects.filter(Departamento__id=es_jefe.cve_depto.id)
    comentarios=[]
    for come in profesores:
        comentarios.append(come.comentario)

    json_list = simplejson.dumps(comentarios)
    return render_to_response('profesor/gestionarHorarios.html',locals(),context_instance=RequestContext(request))

def jefe_depto_guarda_coordinacion(request):
    materia_get=request.GET
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefe=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario)[0]
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materias=Materia.objects.filter(depto__id=es_jefe.cve_depto.id)
    profesores=Profesor.objects.filter(Departamento__id=es_jefe.cve_depto.id)

    try:
        for materia in materia_get:
            if materia_get.get(materia) =="sinAsignar":
                p=materias.filter(id=materia).update(coordinador="")
            else:
                p=materias.filter(id=materia).update(coordinador=materia_get.get(materia))
                mensaje=1;

    except:
        mensaje=2;
    
    return render_to_response('profesor/gestionarCoordinaciones.html',locals(),context_instance=RequestContext(request))

def jefe_depto_coordinacion(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefe=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario)[0]
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materias=Materia.objects.filter(depto__id=es_jefe.cve_depto.id)
    profesores=Profesor.objects.filter(Departamento__id=es_jefe.cve_depto.id)

    return render_to_response('profesor/gestionarCoordinaciones.html',locals(),context_instance=RequestContext(request))



def profesor_registrar_calificaciones_saberes(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materias=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario)
    return render_to_response('profesor/registrar-calificacionesSaberes.html',locals(),context_instance=RequestContext(request))

def profesor_ingresa_calificacion_saberes(request):
    profesor=request.user
    calificaciones=request.GET
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    materia=request.GET['materia']
    request.session["materiaSaberes"] = materia
    materia_saber = Materia.objects.filter(id=int(materia))[0]
    saberes = SaberesPrevios.objects.filter(Materia__id=int(materia)).order_by('Alumno')
    return render_to_response('profesor/IngresaCalificacionSaberes.html',locals(),context_instance=RequestContext(request))


def profesor_guarda_calificacionSaberes(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()

    saberes=request.GET
    for saber in saberes:
        p=SaberesPrevios.objects.filter(id=saber).update(Calificacion=saberes.get(saber))
    mensaje=1
    materia = request.session["materiaSaberes"]
    materia_saber = Materia.objects.filter(id=int(materia))[0]
    saberes = SaberesPrevios.objects.filter(Materia__id=int(materia)).order_by('Alumno')
    return render_to_response('profesor/IngresaCalificacionSaberes.html',locals(),context_instance=RequestContext(request))


def equipoLaboratorio(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefe=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario)[0]
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario)[0]
    equipos=Equipos.objects.filter(laboratorio__id=es_laboratorista.id)
    return render_to_response('profesor/gestionarEquipo.html',locals(),context_instance=RequestContext(request))

def modificarEquipo(request):
    observaciones=request.GET
    
    agregar=0
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefe=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario)[0]
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario)[0]
    
    equipos=Equipos.objects.filter(laboratorio__id=es_laboratorista.id)
    for equip in equipos:
        print observaciones.get(equip.numero_serie+equip.nombreEquipo)
        agregar=1
        for eq in observaciones:
            if(equip.numero_serie!=eq):
                agregar=agregar
            else:
                agregar=0
        if agregar==1:
            print equip.numero_serie
            p=Equipos.objects.get(numero_serie=equip.numero_serie).delete()
            agregar=0
        else:
            p=equipos.filter(numero_serie=equip.numero_serie).update(observaciones=observaciones.get(equip.numero_serie),status=observaciones.get(equip.numero_serie+equip.nombreEquipo))

    equipos=Equipos.objects.filter(laboratorio__id=es_laboratorista.id)
    

    mensaje=1
    return render_to_response('profesor/gestionarEquipo.html',locals(),context_instance=RequestContext(request))



def profesor_agregar_equipo(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    
    return render_to_response('profesor/agregar-equipo.html',locals(),context_instance=RequestContext(request))
def profesor_equipo2(request):
    try:
        profesor=request.user
        nombre=request.GET['nombre']
        serie=request.GET['serie']
        desc=request.GET['desc']
        status=request.GET['status']
        obs=request.GET['obs']
        atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
        es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
        es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
        es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
        
        p=Equipos(nombreEquipo=nombre,numero_serie=serie,
                        descripcionEquipo=desc,
                        status=status,observaciones=obs,
                        laboratorio=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario)[0])
        p.save()
        menseje=1
    except:
        mensaje=2
    return render_to_response('profesor/agregar-equipo.html',locals(),context_instance=RequestContext(request))

def cambiar_contrasena(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()
    bol=request.user
    return render(request, 'profesor/Pr_cambiarpass.html', locals(), context_instance=RequestContext(request))

def cambiarPass(request):
    profesor=request.user
    atributos_profesor = Profesor.objects.filter(cve_usuario = profesor)[0]
    es_coordinador=Materia.objects.filter(coordinador__cve_usuario=atributos_profesor.cve_usuario).count()
    es_jefeDepto=JefeDepartamento.objects.filter(cve_prof__cve_usuario=atributos_profesor.cve_usuario).count()
    es_laboratorista=Laboratorio.objects.filter(encargado__cve_usuario=atributos_profesor.cve_usuario).count()


    bol=request.user
    if request.method=='POST':
        passact=request.POST.get('passact')
        passnuevo=request.POST.get('passnuevo')
        conpassnuevo=request.POST.get('con-passnuevo')
        if passact=="" or passnuevo=="" or conpassnuevo=="":
            print "vacios"
            notif=4
            return render(request, 'profesor/Pr_cambiarpass.html', locals(), context_instance=RequestContext(request))

        else:
            acceso = authenticate(username=str(bol), password=str(passact))
            usuario=Usuario.objects.get(clave=bol)
            
            if acceso is not None:
                print "contrasena correcta"
                if passnuevo==conpassnuevo:
                    print "pass nuevo coinciden"                    
                    usuario.set_password(passnuevo)
                    usuario.save()
                    notif=1
                    return render(request, 'profesor/Pr_cambiarpass.html', locals(), context_instance=RequestContext(request))
                else:
                    print "pass nuevo no coinciden"
                    notif=3
                    return render(request, 'profesor/Pr_cambiarpass.html', locals(), context_instance=RequestContext(request))
                
                print "passnuevo: "+passnuevo
                print "confir passnuevo: "+conpassnuevo
                
            if acceso is None:
                notif=2
                print "contrasena incorrecta"
                return render(request, 'profesor/Pr_cambiarpass.html', locals(), context_instance=RequestContext(request)) 