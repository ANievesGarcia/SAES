# -*- encoding: utf-8 -*-

from django.shortcuts import render 
from django.shortcuts import render_to_response 
from django.shortcuts import redirect 
from django.template import RequestContext 
from django.http import HttpResponseRedirect 
from django.contrib.auth import authenticate 
from django.http import HttpResponse 
from principal.models import * 
import time 
from django.core import serializers
from django.utils import timezone
#APARTE
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from principal.models import *
from datetime import datetime
from geraldo.utils import cm
from geraldo.generators import PDFGenerator
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils.encoding import smart_str, smart_unicode
import random
from reporteAlum import *
from reporteProf import *
from geraldo.generators import PDFGenerator
from datetime import date

from reporteGrupo import*
from reports import reporteMateria

import time
bandera=0
prof=0
nombre=0
tipo=0
def control_main(request):

	bol=request.user
	fechas=calendarios.objects.all()[0]
	finet=fechas.finets
	actual=date.today()
	notif=0
	if(actual>finet):
		notif=1
		print "entra"    	
	#alu=CitaInsc.objects.get(alumno__cve_usuario=bol)
	#cita=alu.cita
	#hora=datetime.now(tz=timezone.get_default_timezone())
	#inscrito=alu.inscrito
	return render(request, 'control/controlinicio.html', locals(), context_instance=RequestContext(request))

#BUSCAR PROFESOR	
#************************************************************************************

def buscarprof(request):
	bol=request.user	
	profesoresList= Profesor.objects.all()	
	profesors= Profesor.objects.all()	
	return render(request,'control/buscarprof.html', locals(), context_instance=RequestContext(request))

#************************************************************************************	
def mostrarprofesores(request):
	global bandera
	bol=request.user
	if request.method=='POST':
		nombre= request.POST.get('prof')
		completo=nombre.split()	
		print len(completo)	
		if(len(completo)==3):
			nombreprofesor=completo[0]
			apellidoPat=completo[1]
			apellidoMat=completo[2]	
			bandera=1
		elif(len(completo)==1):
			clave=completo[0]
			print clave
			bandera=2
		else:
			bandera=3
		
		print "todo va bien"	
		if (bandera==1):	
			#print nombreprofesor,apellidoPaterno,apellidoMaterno
			try:
				profesors = Profesor.objects.filter(cve_usuario__nombre = nombreprofesor,cve_usuario__apellidoPaterno = apellidoPat,cve_usuario__apellidoMaterno = apellidoMat)[0]
				#print profesor
				#notif=1
				return render(request,'control/buscarprof.html', locals(), context_instance=RequestContext(request))
				
			except:
				profesors= Profesor.objects.all()	
				notif=2
				return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))
		elif(bandera==2):
			try:
				print "veamos"
				profesors = Profesor.objects.filter(cve_usuario__clave = clave)[0]	
				print "Entra aca"
				#notif=1							
				return render(request,'control/buscarprof2.html', locals(), context_instance=RequestContext(request))
				
			except:
				try:
					print clave
					print "pasa por aca"
					profesors = Profesor.objects.filter(cve_usuario__nombre = clave)[0]
					print "Entra aqui"	
					return render(request,'control/buscarprof2.html', locals(), context_instance=RequestContext(request))
				except:
					profesors= Profesor.objects.all()	
					notif=2
					return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))
		else:
				profesors= Profesor.objects.all()	
				notif=3
				return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))
#************************************************************************************
def eliminartotalprofesor(request):
	bol=request.user
	global prof
	try:
		profesors = Profesor.objects.filter(cve_usuario__clave=prof)[0]
		#print profesors.cve_usuario.nombre
		profesors.delete()
		profesors = Profesor.objects.all()
		notif=5
		return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))
	except:
		print "Error"
		return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))
				
#************************************************************************************			
def eliminarprofesor(request,dato):
	bol=request.user
	notif=4
	try:
		global prof
		prof=dato		
		profesor2 = Profesor.objects.filter(cve_usuario__clave=dato)[0]
		profesors= Profesor.objects.all()	
		return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))
	except:
		print "muere"
		return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))

#************************************************************************************
#FECHAS
def fechas_inscripciones(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]		
	return render(request, 'control/fechasinscr.html', locals(), context_instance=RequestContext(request))

def periodo_escolar(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	materias=Materia.objects.all()
	for a in materias:
		print smart_str(a.nombre)
	return render(request, 'control/fechasperiodo.html', locals(), context_instance=RequestContext(request))

def modificar_periodo(request):
	bol=request.user
	#fechas=calendarios.objects.all()[0]
	#inicio=str(fechas.inicinscr).split('-')
	#print inicio
	#print inicio[0],inicio[1],inicio[2]	
	return render(request, 'control/periodo.html', locals(), context_instance=RequestContext(request))

def guardar_periodo(request):
	bol=request.user
	if request.method=='POST':
		if(request.POST.get('inic')=="" or request.POST.get('fin')==""):
			notif=3
			return render(request, 'control/periodo.html', locals(), context_instance=RequestContext(request))
		else:
			fechainic= request.POST.get('inic').replace("/","-")
			fechafin= request.POST.get('fin').replace("/","-")
			uno=fechainic.split('-')
			dos=fechafin.split('-')
			if(int(dos[2])-int(uno[2])==0):
				if( int(dos[0])-int(uno[0])==6):					
					fechainic=uno[2]+"-"+uno[0]+"-"+uno[1]
					fechafin=dos[2]+"-"+dos[0]+"-"+dos[1]
					try:
						fechas=calendarios.objects.all()[0]
						print "pasa1"			
						print fechas.clave,fechas.inicinscr
						#date1=date(uno[2],uno[1],uno[1])
						fechas.inicperiodo=fechainic
						print "pasa2"
						fechas.finperiodo=fechafin
						fechas.save()
						print "pasa3"
						notif=1
						fechas=calendarios.objects.all()[0]
						return render(request, 'control/fechasperiodo.html', locals(), context_instance=RequestContext(request))
					except Exception,e: 
						print str(e)
						print "aaaaa no pude"
						return render(request, 'control/periodo.html', locals(), context_instance=RequestContext(request))
				else:
					notif=5
					return render(request, 'control/periodo.html', locals(), context_instance=RequestContext(request))
					
			if(int(dos[2])-int(uno[2])==1):
				if( int(dos[0])+12-int(uno[0])==6):					
					print "entra aqui"
					fechainic=uno[2]+"-"+uno[0]+"-"+uno[1]
					fechafin=dos[2]+"-"+dos[0]+"-"+dos[1]
					try:
						fechas=calendarios.objects.all()[0]
						print "pasa1"			
						print fechas.clave,fechas.inicinscr
						#date1=date(uno[2],uno[1],uno[1])
						fechas.inicperiodo=fechainic
						print "pasa2"
						fechas.finperiodo=fechafin
						fechas.save()
						print "pasa3"
						notif=1
						fechas=calendarios.objects.all()[0]
						return render(request, 'control/fechasperiodo.html', locals(), context_instance=RequestContext(request))
					except Exception,e: 
						print str(e)
						print "aaaaa no pude"
						return render(request, 'control/periodo.html', locals(), context_instance=RequestContext(request))
				else:
					notif=5
					return render(request, 'control/periodo.html', locals(), context_instance=RequestContext(request))
				
			
		
 
#************************************************************************************
def guardar_inscripciones(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]	
	if request.method=='POST':
		if(request.POST.get('inic')=="" or request.POST.get('fin')==""):
			notif=3
			return render(request, 'control/inscripciones.html', locals(), context_instance=RequestContext(request))
		else:
			#VALIDAR FECHA CON PERIODO
			fechain= request.POST.get('inic').replace("/","-")
			fechaf= request.POST.get('fin').replace("/","-")
			uno1=fechain.split('-')
			dos2=fechaf.split('-')
			fechain=uno1[2]+"-"+uno1[0]+"-"+uno1[1]
			fechaf=dos2[2]+"-"+dos2[0]+"-"+dos2[1]
			periodoin=str(fechas.inicperiodo).split('-')			
			periodofn=str(fechas.finperiodo).split('-')		
						
			periodoinano=int(periodoin[0])
			periodoinmes=int(periodoin[1])
			periodoindia=int(periodoin[2])
			
			periodofnano=int(periodofn[0])
			periodofnmes=int(periodofn[1])
			periodofndia=int(periodofn[2])
			
			fechainano=int(uno1[2])
			fechainmes=int(uno1[0])
			fechaindia=int(uno1[1])
			
			fechafnano=int(dos2[2])
			fechafnmes=int(dos2[0])
			fechafndia=int(dos2[1])
			
			if periodofnano-fechafnano==1:
				periodofnmes+=12
			print periodoinano,periodoinmes,periodoindia
			print periodofnano,periodofnmes,periodofndia
			print fechainano,fechainmes,fechaindia
			print fechafnano,fechafnmes,fechafndia
			
			if(periodoinano<=fechainano and periodoinmes<= fechainmes and periodoindia<=fechaindia and periodofnano>=fechafnano and periodofnmes>=fechafnmes): 			
			

				#ASIGNAR CITAS DE INSCRIPCION
				perio=fechas.periodo
				alumnos=Alumno.objects.all()
				ordinarios=[]
				undiatarde=[]
				dosdiatarde=[]	
				for al in alumnos:		
					temporal=kardex.objects.filter(alumno=al,periodo=perio)		
					promedio=0
					rango=0
					arreglo=[]
					for materias in temporal:			
						if(materias.calificacion<6):
							rango+=1
							promedio=promedio+materias.calificacion
						else:
							promedio=promedio+materias.calificacion	
					if(len(temporal)==0):
						promedio=0
					else:
						promedio=promedio/len(temporal)
					arreglo.append(al.cve_usuario.clave)
					arreglo.append(promedio)
					if(rango==0):						
						ordinarios.append(arreglo)
					elif(rango==1):							
						undiatarde.append(arreglo)
					else:	
						dosdiatarde.append(arreglo)
						
				#ORDENAMIENTO DE ALUMNOS
				listaordinarios=sorted(ordinarios,lambda x,y: cmp(x[1],y[1]))
				listaordinarios=listaordinarios[::-1]
				listaundia=sorted(undiatarde,lambda x,y: cmp(x[1],y[1]))
				listaundia=listaundia[::-1]
				listadosdia=sorted(dosdiatarde,lambda x,y: cmp(x[1],y[1]))
				listadosdia=listadosdia[::-1]
				print listaordinarios
				print listaundia
				print listadosdia
				citas=CitaInsc.objects.all()
				#BORRAR LAS CITAS ANTERIORES
				for cita in citas:
					cita.delete()	
				fechainicio=fechas.inicinscr
				fecha=str(fechainicio).split('-')
				horainic=8
				minutoinic=0
				segundos=0	
				#CREAR NUEVAS CITAS
				for i in range (len(listaordinarios)):
					try:
						alum=Alumno.objects.filter(cve_usuario__clave=listaordinarios[i][0])[0]
						now = datetime(int(fecha[0]), int(fecha[1]), int(fecha[2]),horainic, minutoinic,segundos)
						print now
						nuevacita=CitaInsc.objects.create(alumno=alum,cita=now)
						minutoinic+=15
						if(minutoinic>=60):
							horainic+=1
							minutoinic=0
					except Exception,e: 
							print str(e)
				print "pasa"
				for i in range (len(listaundia)):
					try:
						alum=Alumno.objects.filter(cve_usuario__clave=listaundia[i][0])[0]
						now = datetime(int(fecha[0]), int(fecha[1]), int(fecha[2])+1,horainic, minutoinic,segundos)
						print now
						nuevacita=CitaInsc.objects.create(alumno=alum,cita=now)
						minutoinic+=15
						if(minutoinic>=60):
							horainic+=1
							minutoinic=0
					except Exception,e: 
							print str(e)			
				for i in range (len(listadosdia)):
					try:
						alum=Alumno.objects.filter(cve_usuario__clave=listadosdia[i][0])[0]
						now = datetime(int(fecha[0]), int(fecha[1]), int(fecha[2])+1,horainic, minutoinic,segundos)
						print now
						nuevacita=CitaInsc.objects.create(alumno=alum,cita=now)
						minutoinic+=15
						if(minutoinic>=60):
							horainic+=1
							minutoinic=0					
						
					except Exception,e: 
							print str(e)
				
				fechainic= request.POST.get('inic').replace("/","-")
				fechafin= request.POST.get('fin').replace("/","-")
				uno=fechainic.split('-')
				dos=fechafin.split('-')
				fechainic=uno[2]+"-"+uno[0]+"-"+uno[1]
				fechafin=dos[2]+"-"+dos[0]+"-"+dos[1]
				try:
					fechas=calendarios.objects.all()[0]
					print "pasa1"			
					print fechas.clave,fechas.inicinscr
					#date1=date(uno[2],uno[1],uno[1])
					fechas.inicinscr=fechainic
					print "pasa2"
					fechas.fininscr=fechafin
					fechas.periodo=request.POST.get('periodo')
					fechas.save()
					print "pasa3"
					notif=1
					fechas=calendarios.objects.all()[0]				
					return render(request, 'control/fechasinscr.html', locals(), context_instance=RequestContext(request))
				except Exception,e: 
					print str(e)
					print "aaaaa no pude"
					return render(request, 'control/inscripciones.html', locals(), context_instance=RequestContext(request))
			else:
				notif=7
				return render(request, 'control/inscripciones.html', locals(), context_instance=RequestContext(request))
	
#************************************************************************************			
def modificar_inscripciones(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]	
	fechainicio=fechas.inicperiodo
	print "woo",fechainicio
	per=str(fechainicio).split('-')
	ano=int(per[0])
	mes=int(per[1])
	dia=int(per[2])
	request.session['ano'] = ano
	request.session['mes'] = mes
	request.session['dia'] = dia
	
	print per[0],per[1],per[2]	
	return render(request, 'control/inscripciones.html', locals(), context_instance=RequestContext(request))

#************************************************************************************				
def fechas_ordinarias(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	return render(request, 'control/fechasord.html', locals(), context_instance=RequestContext(request))
#************************************************************************************				
def modificar_ordinarias(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	inicio=str(fechas.inicinscr).split('-')
	print inicio
	print inicio[0],inicio[1],inicio[2]
	return render(request, 'control/ordinarias.html', locals(), context_instance=RequestContext(request))
#************************************************************************************		
def guardar_ordinarias(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]	
	if request.method=='POST':
		if(request.POST.get('inic')=="" or request.POST.get('fin')==""):
			notif=3
			return render(request, 'control/ordinarias.html', locals(), context_instance=RequestContext(request))
		else:
			#VALIDAR FECHA CON PERIODO
			fechain= request.POST.get('inic').replace("/","-")
			fechaf= request.POST.get('fin').replace("/","-")
			uno1=fechain.split('-')
			dos2=fechaf.split('-')
			fechain=uno1[2]+"-"+uno1[0]+"-"+uno1[1]
			fechaf=dos2[2]+"-"+dos2[0]+"-"+dos2[1]
			periodoin=str(fechas.inicinscr).split('-')			
			periodofn=str(fechas.fininscr).split('-')		
						
			periodoinano=int(periodoin[0])
			periodoinmes=int(periodoin[1])
			periodoindia=int(periodoin[2])
			
			periodofnano=int(periodofn[0])
			periodofnmes=int(periodofn[1])
			periodofndia=int(periodofn[2])
			
			fechainano=int(uno1[2])
			fechainmes=int(uno1[0])
			fechaindia=int(uno1[1])
			
			fechafnano=int(dos2[2])
			fechafnmes=int(dos2[0])
			fechafndia=int(dos2[1])
			
			if periodofnano-fechafnano==1:
				periodofnmes+=12
			print periodoinano,periodoinmes,periodoindia
			print periodofnano,periodofnmes,periodofndia
			print fechainano,fechainmes,fechaindia
			print fechafnano,fechafnmes,fechafndia
			
			if(periodoinano<=fechainano and periodoinmes<= fechainmes and periodoindia<=fechaindia and periodofnano>=fechafnano and periodofnmes>=fechafnmes): 			
			
				fechainic= request.POST.get('inic').replace("/","-")
				fechafin= request.POST.get('fin').replace("/","-")
				uno=fechainic.split('-')
				dos=fechafin.split('-')
				fechainic=uno[2]+"-"+uno[0]+"-"+uno[1]
				fechafin=dos[2]+"-"+dos[0]+"-"+dos[1]
				try:
					fechas=calendarios.objects.all()[0]
					print "pasa1"			
					print fechas.clave,fechas.inicinscr
					#date1=date(uno[2],uno[1],uno[1])
					fechas.inicord=fechainic
					print "pasa2"
					fechas.finord=fechafin
					fechas.save()
					print "pasa3"
					notif=1
					fechas=calendarios.objects.all()[0]
					return render(request, 'control/fechasord.html', locals(), context_instance=RequestContext(request))
				except Exception,e: 
					print str(e)
					print "aaaaa no pude"
					return render(request, 'control/ordinarias.html', locals(), context_instance=RequestContext(request))
			else:
				notif=7
				return render(request, 'control/ordinarias.html', locals(), context_instance=RequestContext(request))
#************************************************************************************				
def fechas_extra(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	return render(request, 'control/fechasextra.html', locals(), context_instance=RequestContext(request))

#************************************************************************************		
def modificar_extraordinarias(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	return render(request, 'control/extraordinarias.html', locals(), context_instance=RequestContext(request))
#************************************************************************************		
def guardar_extraordinarias(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]	
	if request.method=='POST':
		if(request.POST.get('inic')=="" or request.POST.get('fin')==""):
			notif=3
			return render(request, 'control/extraordinarias.html', locals(), context_instance=RequestContext(request))
		else:
			#VALIDAR FECHA CON PERIODO
			fechain= request.POST.get('inic').replace("/","-")
			fechaf= request.POST.get('fin').replace("/","-")
			uno1=fechain.split('-')
			dos2=fechaf.split('-')
			fechain=uno1[2]+"-"+uno1[0]+"-"+uno1[1]
			fechaf=dos2[2]+"-"+dos2[0]+"-"+dos2[1]
			periodoin=str(fechas.inicord).split('-')			
			periodofn=str(fechas.finord).split('-')		
						
			periodoinano=int(periodoin[0])
			periodoinmes=int(periodoin[1])
			periodoindia=int(periodoin[2])
			
			periodofnano=int(periodofn[0])
			periodofnmes=int(periodofn[1])
			periodofndia=int(periodofn[2])
			
			fechainano=int(uno1[2])
			fechainmes=int(uno1[0])
			fechaindia=int(uno1[1])
			
			fechafnano=int(dos2[2])
			fechafnmes=int(dos2[0])
			fechafndia=int(dos2[1])
			
			if periodofnano-fechafnano==1:
				periodofnmes+=12
			if fechainmes-periodoinmes==1:
				fechaindia+=30
			print periodoinano,periodoinmes,periodoindia
			print periodofnano,periodofnmes,periodofndia
			print fechainano,fechainmes,fechaindia
			print fechafnano,fechafnmes,fechafndia
			
			if(periodoinano<=fechainano and periodoinmes<= fechainmes and periodoindia<=fechaindia): 	
				fechainic= request.POST.get('inic').replace("/","-")
				fechafin= request.POST.get('fin').replace("/","-")
				uno=fechainic.split('-')
				dos=fechafin.split('-')
				fechainic=uno[2]+"-"+uno[0]+"-"+uno[1]
				fechafin=dos[2]+"-"+dos[0]+"-"+dos[1]
				try:
					fechas=calendarios.objects.all()[0]
					print "pasa1"			
					print fechas.clave,fechas.inicinscr
					#date1=date(uno[2],uno[1],uno[1])
					fechas.inicextra=fechainic
					print "pasa2"
					fechas.finextra=fechafin
					fechas.save()
					print "pasa3"
					notif=1
					fechas=calendarios.objects.all()[0]
					return render(request, 'control/fechasextra.html', locals(), context_instance=RequestContext(request))
				except Exception,e: 
					print str(e)
					print "aaaaa no pude"
					return render(request, 'control/extraordinarias.html', locals(), context_instance=RequestContext(request))
			else:
				notif=7
				return render(request, 'control/extraordinarias.html', locals(), context_instance=RequestContext(request))
#************************************************************************************				
def fechas_ets(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	return render(request, 'control/fechasets.html', locals(), context_instance=RequestContext(request))
#************************************************************************************		
def modificar_ets(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	return render(request, 'control/ets.html', locals(), context_instance=RequestContext(request))
	#************************************************************************************		
def guardar_ets(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]	
	if request.method=='POST':
		if(request.POST.get('inic')=="" or request.POST.get('fin')==""):
			notif=3
			return render(request, 'control/ets.html', locals(), context_instance=RequestContext(request))
		else:
			#VALIDAR FECHA CON PERIODO
			fechain= request.POST.get('inic').replace("/","-")
			fechaf= request.POST.get('fin').replace("/","-")
			uno1=fechain.split('-')
			dos2=fechaf.split('-')
			fechain=uno1[2]+"-"+uno1[0]+"-"+uno1[1]
			fechaf=dos2[2]+"-"+dos2[0]+"-"+dos2[1]
			periodoin=str(fechas.finextra).split('-')			
			periodofn=str(fechas.finextra).split('-')		
						
			periodoinano=int(periodoin[0])
			periodoinmes=int(periodoin[1])
			periodoindia=int(periodoin[2])
			
			periodofnano=int(periodofn[0])
			periodofnmes=int(periodofn[1])
			periodofndia=int(periodofn[2])
			
			fechainano=int(uno1[2])
			fechainmes=int(uno1[0])
			fechaindia=int(uno1[1])
			
			fechafnano=int(dos2[2])
			fechafnmes=int(dos2[0])
			fechafndia=int(dos2[1])
			
			if periodofnano-fechafnano==1:
				periodofnmes+=12
			if fechainmes-periodoinmes==1:
				fechaindia+=30
			print periodoinano,periodoinmes,periodoindia
			print periodofnano,periodofnmes,periodofndia
			print fechainano,fechainmes,fechaindia
			print fechafnano,fechafnmes,fechafndia
			
			if(periodoinano<=fechainano and periodoinmes<= fechainmes and periodoindia<=fechaindia): 
				fechainic= request.POST.get('inic').replace("/","-")
				fechafin= request.POST.get('fin').replace("/","-")
				uno=fechainic.split('-')
				dos=fechafin.split('-')
				fechainic=uno[2]+"-"+uno[0]+"-"+uno[1]
				fechafin=dos[2]+"-"+dos[0]+"-"+dos[1]
				try:
					fechas=calendarios.objects.all()[0]
					print "pasa1"			
					print fechas.clave,fechas.inicinscr
					#date1=date(uno[2],uno[1],uno[1])
					fechas.inicetes=fechainic
					print "pasa2"
					fechas.finets=fechafin
					fechas.save()
					print "pasa3"
					notif=1
					fechas=calendarios.objects.all()[0]
					return render(request, 'control/fechasets.html', locals(), context_instance=RequestContext(request))
				except Exception,e: 
					print str(e)
					print "aaaaa no pude"
					return render(request, 'control/ets.html', locals(), context_instance=RequestContext(request))
			else:
				notif=7
				return render(request, 'control/ets.html', locals(), context_instance=RequestContext(request))
#************************************************************************************
def documentos(request):
	bol=request.user
	alumnos=DocSolicitado.objects.all()
	for alumno in alumnos:
		print alumno.alumno		
	return render(request, 'control/documentos.html', locals(), context_instance=RequestContext(request))
#************************************************************************************			
def eliminardocumento(request,dato1):
	bol=request.user
	try:
		global nombre
		global tipo		
		separado=dato1.split('-')
		nombre=separado[0]
		tipo=separado[1]
		print separado
		alumno2 = DocSolicitado.objects.filter(alumno__cve_usuario__clave=separado[0],tipo_doc=separado[1])[0]
		alumnos=DocSolicitado.objects.all()
		notif=4
		return render(request, 'control/documentos.html', locals(), context_instance=RequestContext(request))
	except:
		print "muere"
		return render(request, 'control/documentos.html', locals(), context_instance=RequestContext(request))
		
def eliminartotaldocumento(request):
	bol=request.user
	global nombre
	global tipo
	try:
		alumno2 = DocSolicitado.objects.filter(alumno__cve_usuario__clave=nombre,tipo_doc=tipo)[0]
		#print profesors.cve_usuario.nombre
		alumno2.delete()
		alumnos=DocSolicitado.objects.all()
		notif=5
		return render(request, 'control/documentos.html', locals(), context_instance=RequestContext(request))
	except:
		print "Error"
		return render(request, 'control/documentos.html', locals(), context_instance=RequestContext(request))

	#**********************Inicia Codigos para Materias *************************************************
	
def abreMateria(request):
	bol=request.user	
	deptos=Depto.objects.all()
	materias=Materia.objects.all()

	
	return render(request, 'control/gestionMateria.html', locals(), context_instance=RequestContext(request))


def abreModificaMateria(request):
	bol=request.user	

	if 'modifica_materia' in request.POST:
		try:	
			deptos=Depto.objects.all()
			materias=Materia.objects.all()
			nombre= request.POST.get('materiaElegida')
			#print nombre
			materiaElegida=Materia.objects.filter(nombre=nombre)[0]	
			#print materiaElegida	
			return render(request, 'control/modificarMateria.html', locals(), context_instance=RequestContext(request))	
		
		except:
				return render(request, 'control/buscarMateria.html', locals(), context_instance=RequestContext(request))	
			
	elif 'elimina_materia' in request.POST:
		try:	
			nombre=request.POST.get('materiaElegida')
			materiaElegida=Materia.objects.filter(nombre=nombre)[0]
			print materiaElegida.materia_antecedente
			if ( materiaElegida.materia_antecedente is not None):
				matA=Materia.objects.filter(materia_antecedente__nombre=materiaElegida.nombre)[0]
				print matA
				Materia.objects.filter(cve_materia=matA.cve_materia).update(materia_antecedente=None)
				print 3
			if ( materiaElegida.materia_siguiente is not None):
				matS=Materia.objects.filter(materia_siguiente__nombre=materiaElegida.nombre)[0]
				print matS
				Materia.objects.filter(cve_materia=matS.cve_materia).update(materia_siguiente=None)			
				print 5
			Materia.objects.filter(cve_materia=materiaElegida.cve_materia).update(materia_siguiente=None,materia_antecedente=None)
			print 6	
			materiaElegida.delete()
			notif=10	
			return render(request,'control/buscarMateria.html', locals(), context_instance=RequestContext(request))	
		except:
				return render(request, 'control/buscarMateria.html', locals(), context_instance=RequestContext(request))	

	elif 'reporte_materia' in request.POST:
		try:
			bol=request.user
			nombre=request.POST.get('materiaElegida')
			request.session["nombre"] = nombre
			materiaElegida=Materia.objects.filter(nombre=nombre)
			resp = HttpResponse(mimetype='application/pdf')
			report = reporteMateria(queryset=materiaElegida)
			report.generate_by(PDFGenerator, filename=resp)
			return resp
		except:
			return render(request, 'control/buscarMateria.html', locals(), context_instance=RequestContext(request))	


def abreBuscaMateria(request):
	bol=request.user	
	mat= Materia.objects.all()		
	return render(request, 'control/buscarMateria.html', locals(), context_instance=RequestContext(request))	

	

	
def mostrarMateria(request):
	bol=request.user
	if request.method=='POST':
			nombre= request.POST.get('materia')
			print len(nombre)
		
		#completo=nombre.split()		

			if(len(nombre)==0):
				bandera=3
			
			else:
				bandera=1

		
			
			if (bandera==1):	
				try:
					materias= Materia.objects.filter(nombre = smart_str(nombre))[0]
					print "entra",materias.nombre					
					return render(request,'control/buscarMateria.html', locals(), context_instance=RequestContext(request))
				except:
					materias= Materia.objects.all()	
					print 2
					notif=2
					return render(request, 'control/buscarMateria.html', locals(), context_instance=RequestContext(request))
		
			else:
				materias= Materia.objects.all()	
				notif=3
				return render(request, 'control/buscarMateria.html', locals(), context_instance=RequestContext(request))

	
	
def regMateria(request):
			bol=request.user
			if  request.method=='POST':
				try:	
					cve=request.POST.get('cve_materia')
					nombre=request.POST.get('nombre_materia')
					creditos=request.POST.get('credito_materia')
					plan=request.POST.get('plan_materia')
					clas=request.POST.get('clasif_materia')
					tipo=request.POST.get('tipo_materia')
					nivel=request.POST.get('nivel_materia')
					dep=request.POST.get('dep_materia')
					a=Depto.objects.filter(nombre_depto=dep)[0]
					matA=request.POST.get('matA_materia')
					completo=matA.split()
					matS=request.POST.get('matS_materia')
					completo1=matS.split()
					if (len(matA)!=0 and  len(matS)!=0):
						b=Materia.objects.filter(cve_materia=completo[0])[0]
						c=Materia.objects.filter(cve_materia=completo1[0])[0]
						p=Materia(cve_materia=cve,nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a,materia_antecedente=b,materia_siguiente=c)
						p.save();
						Materia.objects.filter(cve_materia=b.cve_materia).update(materia_siguiente=p)
						Materia.objects.filter(cve_materia=c.cve_materia).update(materia_antecedente=p)
						
						
						
					elif (len(matA)==0 and len(matS)==0):
						p=Materia(cve_materia=cve,nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a)
						p.save();	
					elif(len(matA)!=0 and len(matS)==0):
						b=Materia.objects.filter(cve_materia=completo[0])[0]
						p=Materia(cve_materia=cve,nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a,materia_antecedente=b)
						p.save();
						Materia.objects.filter(cve_materia=b.cve_materia).update(materia_siguiente=p)
						
						
					elif(len(matA)==0 and len(matS)!=0):
						c=Materia.objects.filter(cve_materia=completo1[0])[0]
						p=Materia(cve_materia=cve,nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a,materia_siguiente=c)
						p.save();
						Materia.objects.filter(cve_materia=c.cve_materia).update(materia_antecedente=p)							
					
					notif=1
				except:	
						notif=2
						return render(request,'control/gestionMateria.html', locals(), context_instance=RequestContext(request))
			return render(request,'control/gestionMateria.html', locals(), context_instance=RequestContext(request))		

def modificaMateria(request):
	bol=request.user
	if  request.method=='POST':
		try:	
			cve=request.POST.get('cve_materia')
			nombre=request.POST.get('nombre_materia')
			creditos=request.POST.get('credito_materia')
			plan=request.POST.get('plan_materia')
			clas=request.POST.get('clasif_materia')
			tipo=request.POST.get('tipo_materia')
			nivel=request.POST.get('nivel_materia')
			dep=request.POST.get('dep_materia')
			a=Depto.objects.filter(nombre_depto=dep)[0]
			matA=request.POST.get('matA_materia')
			matS=request.POST.get('matS_materia')
			if (len(matA)!= 4 and  len(matS) != 4):
					#print len(matA)
					#print len(matS)
					completo=matA.split()	
					b=Materia.objects.filter(cve_materia=completo[0])[0]
					completo1=matS.split()		
					c=Materia.objects.filter(cve_materia=completo1[0])[0]
					Materia.objects.filter(cve_materia=cve).update(nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a,materia_antecedente=b,materia_siguiente=c)
					p=Materia.objects.filter(cve_materia=cve)[0]
					Materia.objects.filter(cve_materia=b.cve_materia).update(materia_siguiente=p)
					Materia.objects.filter(cve_materia=c.cve_materia).update(materia_antecedente=p)
			
			elif (len(matA)==4 and len(matS)==4):
					print len(matA)
					print len(matS)
					Materia.objects.filter(cve_materia=cve).update(nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a)
			elif(len(matA)!=4 and len(matS)==4):
				print len(matA)
				print len(matS)
				completo=matA.split()		
				b=Materia.objects.filter(cve_materia=completo[0])[0]
				print b
				Materia.objects.filter(cve_materia=cve).update(nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a,materia_antecedente=b)
				p=Materia.objects.filter(cve_materia=cve)[0]
				Materia.objects.filter(cve_materia=b.cve_materia).update(materia_siguiente=p)
				
				
				
			elif(len(matA)==4 and len(matS)!=4):
				print len(matA)
				print len(matS)			
				completo1=matS.split()		
				c=Materia.objects.filter(cve_materia=completo1[0])[0]
				Materia.objects.filter(cve_materia=cve).update(nombre=nombre,creditos=creditos,plan_estudios=plan,clasificacion=clas,tipo=tipo,nivel=nivel,depto=a,materia_siguiente=c)
				p=Materia.objects.filter(cve_materia=cve)[0]
				Materia.objects.filter(cve_materia=c.cve_materia).update(materia_antecedente=p)	
			notif=1
			return render(request,'control/modificarMateria.html', locals(), context_instance=RequestContext(request))
		except:
				return render(request,'control/buscarMateria.html', locals(), context_instance=RequestContext(request))
			
			
#**********************Termina Codigos para Materias *************************************************

#************************************************************************************
# ENVIAR CORREO A ALUMNO
def alumnoCorreo(request):
	bol=request.user
	return render(request, 'control/alumnoCorreo.html', locals(), context_instance=RequestContext(request))
				
#************************************************************************************
#ENVIO DE CORREO
def enviarAlumnoCorreo(request): 
	bol=request.user
	if request.method=='POST':
		try:
			#destinatarios= request.POST.get('destinatarios')
			#destinatario=destinatarios.split()			
			asunto= request.POST.get('asunto')
			mensaje= request.POST.get('mensaje')
			destinatarios=Alumno.objects.all()
			i=0
			lista=[]
			for alumno in destinatarios:
				lista.insert(i,alumno.cve_usuario.email_institucional)
				i=i+1;
				
				#correo = EmailMessage(asunto, mensaje, to=[destinatario[0],destinatario[1],destinatario[2]])
			#send_mail('asunto', 'mensaje', 'saes.escom@gmail.com',['saes.escom@gmail.com'], fail_silently=False)
			#correo = EmailMessage(asunto, mensaje, to=[alumno.cve_usuario.email_institucional])
			correo = EmailMessage(asunto, mensaje, to=lista)
			correo.send()	
			flag=1
			return render(request, 'control/alumnoCorreo.html', locals(), context_instance=RequestContext(request))
		except:
			flag=2 #Mensaje de error de conexion
			return render(request, 'control/alumnoCorreo.html', locals(), context_instance=RequestContext(request))
	#else:
        #formulario = recuperar_pass()
        #return render_to_response('recuperar_pass.html',{'formulario':formulario}, context_instance=RequestContext(request))


#************************************************************************************
	
def buscarAlum(request):
	bol=request.user	
	return render(request, 'control/buscarAlum.html', locals(), context_instance=RequestContext(request))
def mostrarAlum(request):
	bol=request.user
	fechas=calendarios.objects.all()[0]
	datein=fechas.inicinscr
	datefn=fechas.fininscr
	actual=date.today()
	notifica=0
	if(actual>=datein and actual<=datefn):
		notifica=1
		print "Si entra"
		
	if request.method=='POST':
			boleta= request.POST.get('alumno')
		
		#completo=nombre.split()		

			if(len(boleta)==0):
				bandera=3
				
			else:
				bandera=1

		
			
			if (bandera==1):	
				try:
					usuarios=Usuario.objects.filter(clave = boleta)[0]
				
					alumnos= Alumno.objects.filter(cve_usuario = usuarios)[0]
					notif=15
					return render(request,'control/buscarAlum.html', locals(), context_instance=RequestContext(request))
	
					
				except:
					
					print 2
					notif=2
					return render(request, 'control/buscarAlum.html', locals(), context_instance=RequestContext(request))
		
			else:
				#materias= Materia.objects.all()	
				notif=3
				return render(request, 'control/buscarAlum.html', locals(), context_instance=RequestContext(request))
	
def modificarAlum(request):
	bol=request.user	
	clave= request.POST.get('clave')
	note= request.POST.get('key')
	try:
		usuarios=Usuario.objects.filter(clave = clave)[0]
						
	except:
		print 2
	if note=='si':
		if  request.method=='POST':
			nombre=request.POST.get('nombre_alumno')
			apPat=request.POST.get('apellidoPaterno')
			apMat=request.POST.get('apellidoMaterno')
			boleta=request.POST.get('clave')
			sexo=request.POST.get('sexo')
			fec_nac=request.POST.get('fec_nac')
			
			Usuario.objects.filter(clave=boleta).update(clave=boleta,nombre=nombre,apellidoPaterno=apPat,apellidoMaterno=apMat,sexo=sexo,fecha_nac=fec_nac)
			notif=15
			notif2=1
			try:
				usuarios=Usuario.objects.filter(clave = clave)[0]
				alumnos= Alumno.objects.filter(cve_usuario = usuarios)[0]		
			except:
				print 2
				notif=5
			return render(request, 'control/buscarAlum.html', locals(), context_instance=RequestContext(request))
	return render(request, 'control/modAlumno.html', locals(), context_instance=RequestContext(request))
def reporteAlum(request):
	
	bol=request.user
	clave=request.POST.get('clave1')
	
	a=Usuario.objects.filter(clave=clave)[0]
	alumno=Alumno.objects.filter(cve_usuario=a)
	
	resp = HttpResponse(mimetype='application/pdf')
	 
	report = reporteAlumnos(queryset=alumno)
	report.generate_by(PDFGenerator, filename=resp)
	return resp

def regAlumno(request):
	bol=request.user	
	if  request.method=='POST':
			nombre=request.POST.get('nombre_alumno')
			apPat=request.POST.get('apellidoPaterno')
			apMat=request.POST.get('apellidoMaterno')
			boleta=request.POST.get('boleta')
			sexo=request.POST.get('sexo')
			fec_nac=request.POST.get('fec_nac')
			try:
				one_entry=Usuario.objects.get(clave=boleta)
				notif=2
			except :
				p=Usuario(clave=boleta,nombre=nombre,apellidoPaterno=apPat,apellidoMaterno=apMat,sexo=sexo,fecha_nac=fec_nac,clasificacion='Alumnos')
				p.save();
				cve=apPat.upper();
				usuario=Usuario.objects.get(clave=boleta)
				usuario.set_password(cve)
				usuario.save();
				a=Usuario.objects.filter(clave=boleta)[0]
				q=Alumno(cve_usuario=a,tipo='Nuevo_Ingreso',promedio_escuela_procedencia=0.0)
				q.save();
				b=Alumno.objects.filter(cve_usuario=a)[0]
				r=CitaInsc(alumno=b)
				r.save();
				notif=1
	else:
		i=1
		while (i==1):
			num=random.randrange(1000)
			if(num<100):
				n="0"+str(num)
			else:
				n=str(num)
			d = date.today()
			yr=d.year	
			bolet=""+str(yr)+"630"+n
			print bolet
			try:
				one_entry=Usuario.objects.get(clave=bolet)
			except:
				i=0
	return render(request, 'control/regAlumno.html', locals(), context_instance=RequestContext(request))
#-------- GESTION GRUPOS MODIF ---------------------------------------

def color( materia ):
    if( materia.materia.clasificacion == 'Institucional' ) :
        return 'm1'

    elif( materia.materia.clasificacion == 'Cientifica_basica' ) :
        return 'm4'

    elif( materia.materia.clasificacion == 'Profesional' ) :
        return 'm3'

    elif( materia.materia.clasificacion == 'Terminal_integración' ) :
        return 'm2'
    else :
        return 'm3'

def gestion_grupos( request ):

	clave_empleado					= request.user
	#empleado						= EmpleadoEscolar.objects.get( cve_usuario = clave_empleado )

	lista_grupos					= Grupo.objects.all()
	request.session['lista_grupos'] = lista_grupos

	return render_to_response( 'control/grupos/gestion.html', locals(), context_instance = RequestContext( request ) )


def abrir_grupo( request ):

	clave_empleado						= request.user
	#empleado							= EmpleadoEscolar.objects.get( cve_usuario = clave_empleado )

	salones								= Salon.objects.exclude( bandera = 3 )
	materias							= Materia.objects.all()

	mensaje_abrir						= 0

	request.session['salones']			= salones
	request.session['materias']			= materias
	if 'mensaje_abrir' in request.session:
		mensaje_abrir					= request.session['mensaje_abrir']
	request.session['mensaje_abrir']	= mensaje_abrir

	return render_to_response( 'control/grupos/abrir.html', locals(), context_instance = RequestContext( request ) )


def modificar_grupo( request, clave_grupo ):

	clave_empleado				= request.user
	#empleado					= EmpleadoEscolar.objects.get( cve_usuario = clave_empleado )

	clave_grupo					= clave_grupo
	grupo						= Grupo.objects.get( cve_grupo = clave_grupo )

	salones						= Salon.objects.exclude( bandera = 3 )
	materias					= Materia.objects.all()

	mensaje_modificar			= 0

	materiasig					= MateriaImpartidaEnGrupo.objects.filter( grupo = grupo )

	request.session['grupo']		= clave_grupo
	request.session['materiasig']	= materiasig
	if 'mensaje_modificar' in request.session:
		mensaje_modificar					= request.session['mensaje_modificar']
	request.session['mensaje_modificar']	= mensaje_modificar

	return render_to_response( 'control/grupos/modificar.html', locals(), context_instance = RequestContext( request ) )


def controlador_cerrar_grupo( request, clave_grupo ):

	clave_empleado	= request.user
	#empleado		= EmpleadoEscolar.objects.get( cve_usuario = clave_empleado )

	clave_grupo		= clave_grupo

	grupo			= Grupo.objects.get( cve_grupo = clave_grupo )

	salon			= Salon.objects.get( cve_salon = str( grupo.cve_salon.cve_salon ) )

	if clave_grupo[2] == 'M' :
		salon.bandera = salon.bandera - 1
	else :
		salon.bandera = salon.bandera - 2

	salon.save()
	grupo.delete()

	return HttpResponseRedirect( "../grupos/" )


def controlador_abrir_grupo( request ):

	clave_empleado	= request.user
	#empleado		= EmpleadoEscolar.objects.get( cve_usuario = clave_empleado )

	clave_grupo		= request.POST.get( 'clave_grupo' )
	clave_salon		= int ( request.POST.get( 'clave_salon' ) )

	clave_materia1	= request.POST.get( 'materias1' )
	clave_horario1	= int( request.POST.get( 'horarios1' ) )
	
	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		clave_materia2	= request.POST.get( 'materias2' )
		clave_materia3	= request.POST.get( 'materias3' )
		clave_materia4	= request.POST.get( 'materias4' )
		clave_materia5	= request.POST.get( 'materias5' )
		clave_materia6	= request.POST.get( 'materias6' )
		clave_horario2	= int( request.POST.get( 'horarios2' ) )
		clave_horario3	= int( request.POST.get( 'horarios3' ) )
		clave_horario4	= int( request.POST.get( 'horarios4' ) )
		clave_horario5	= int( request.POST.get( 'horarios5' ) )
		clave_horario6	= int( request.POST.get( 'horarios6' ) )
			
	if ( clave_grupo[0] == '1' ) :
		clave_materia7	= request.POST.get( 'materias7' )
		clave_horario7	= int( request.POST.get( 'horarios7' ) )

	lista_grupos	= Grupo.objects.all()

	for grupo in lista_grupos :
		if ( grupo.cve_grupo == clave_grupo ) :
			request.session['mensaje_abrir'] = 1
			return HttpResponseRedirect( '../abrir_grupo/' )

	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( ( clave_materia1 == clave_materia2 ) or ( clave_materia1 == clave_materia3 ) or ( clave_materia1 == clave_materia4 ) or ( clave_materia1 == clave_materia5 ) or ( clave_materia1 == clave_materia6 ) or ( clave_materia2 == clave_materia3 ) or ( clave_materia2 == clave_materia4 ) or ( clave_materia2 == clave_materia5 ) or ( clave_materia2 == clave_materia6 ) or ( clave_materia3 == clave_materia4 ) or ( clave_materia3 == clave_materia5 ) or ( clave_materia3 == clave_materia6 ) or ( clave_materia4 == clave_materia5 ) or ( clave_materia4 == clave_materia6 ) or ( clave_materia5 == clave_materia6 ) ) :
			request.session['mensaje_abrir'] = 2
			return HttpResponseRedirect( '../abrir_grupo/' )
		if ( ( clave_horario1 == clave_horario2 ) or ( clave_horario1 == clave_horario3 ) or ( clave_horario1 == clave_horario4 ) or ( clave_horario1 == clave_horario5 ) or ( clave_horario1 == clave_horario6 ) or ( clave_horario2 == clave_horario3 ) or ( clave_horario2 == clave_horario4 ) or ( clave_horario2 == clave_horario5 ) or ( clave_horario2 == clave_horario6 ) or ( clave_horario3 == clave_horario4 ) or ( clave_horario3 == clave_horario5 ) or ( clave_horario3 == clave_horario6 ) or ( clave_horario4 == clave_horario5 ) or ( clave_horario4 == clave_horario6 ) or ( clave_horario5 == clave_horario6 ) ) :
			request.session['mensaje_abrir'] = 3
			return HttpResponseRedirect( '../abrir_grupo/' )

	if ( ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( ( clave_materia1 == clave_materia7 ) or ( clave_materia2 == clave_materia7 ) or ( clave_materia3 == clave_materia7 ) or ( clave_materia4 == clave_materia7 ) or ( clave_materia5 == clave_materia7 ) or ( clave_materia6 == clave_materia7 ) ) :
			request.session['mensaje_abrir'] = 2
			return HttpResponseRedirect( '../abrir_grupo/' )
		if ( ( clave_horario1 == clave_horario7 ) or ( clave_horario2 == clave_horario7 ) or ( clave_horario3 == clave_horario7 ) or ( clave_horario4 == clave_horario7 ) or ( clave_horario5 == clave_horario7 ) or ( clave_horario6 == clave_horario7 ) ) :
			request.session['mensaje_abrir'] = 3
			return HttpResponseRedirect( '../abrir_grupo/' )

	if ( not ( clave_materia1[1] == clave_grupo[0] ) ) :
		request.session['mensaje_abrir'] = 5
		return HttpResponseRedirect( '../abrir_grupo/' )

	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( not ( ( clave_materia2[1] == clave_grupo[0] ) and ( clave_materia3[1] == clave_grupo[0] ) and ( clave_materia4[1] == clave_grupo[0] ) and ( clave_materia5[1] == clave_grupo[0] ) and ( clave_materia6[1] == clave_grupo[0] ) ) ) :
			request.session['mensaje_abrir'] = 5
			return HttpResponseRedirect( '../abrir_grupo/' )

	if ( ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( not ( clave_materia7[1] == clave_grupo[0] ) ) :
			request.session['mensaje_abrir'] = 5
			return HttpResponseRedirect( '../abrir_grupo/' )

	salon	= Salon.objects.get( cve_salon = clave_salon )

	if ( clave_grupo[2] == 'M' ) :
		if ( ( salon.bandera == 1 ) or ( salon.bandera == 3 ) ) :
			request.session['mensaje_abrir'] = 4
			return HttpResponseRedirect( '../abrir_grupo/' )
		else :
			salon.bandera	= salon.bandera + 1
			turno			= 'Matutino'

		if ( ( clave_horario1 > 8 ) or ( clave_horario2 > 8 ) or ( clave_horario3 > 8 ) or ( clave_horario4 > 8 ) or ( clave_horario5 > 8 ) or ( clave_horario6 > 8 ) or ( clave_horario7 > 8 ) ) :
			request.session['mensaje_abrir'] = 6
			return HttpResponseRedirect( '../abrir_grupo/' )
	else :
		if ( ( salon.bandera == 2 ) or ( salon.bandera == 3 ) ) :
			request.session['mensaje_abrir'] = 4
			return HttpResponseRedirect( '../abrir_grupo/' )
		else :
			salon.bandera	= salon.bandera + 2
			turno			= 'Vespertino'

		if ( ( clave_horario1 < 8 ) or ( clave_horario2 < 8 ) or ( clave_horario3 < 8 ) or ( clave_horario4 < 8 ) or ( clave_horario5 < 8 ) or ( clave_horario6 < 8 ) or ( clave_horario7 < 8 ) ) :
			request.session['mensaje_abrir'] = 6
			return HttpResponseRedirect( '../abrir_grupo/' )

	profesor	= Profesor.objects.get( cve_usuario__clave = 'XXXX000000' )

	nuevo_grupo	= Grupo( cve_grupo = clave_grupo, cve_salon = salon, turno = turno )

	salon.save()
	nuevo_grupo.save()

	materia1	= Materia.objects.get( cve_materia = clave_materia1 )
	horario1	= Horario.objects.get( cve_horario = clave_horario1 )
	materia_ig1	= MateriaImpartidaEnGrupo( materia = materia1, horario = horario1, grupo = nuevo_grupo, profesor = profesor )
	materia_ig1.save()

	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :	
		materia2	= Materia.objects.get( cve_materia = clave_materia2 )
		materia3	= Materia.objects.get( cve_materia = clave_materia3 )
		materia4	= Materia.objects.get( cve_materia = clave_materia4 )
		materia5	= Materia.objects.get( cve_materia = clave_materia5 )
		materia6	= Materia.objects.get( cve_materia = clave_materia6 )
		horario2	= Horario.objects.get( cve_horario = clave_horario2 )
		horario3	= Horario.objects.get( cve_horario = clave_horario3 )
		horario4	= Horario.objects.get( cve_horario = clave_horario4 )
		horario5	= Horario.objects.get( cve_horario = clave_horario5 )
		horario6	= Horario.objects.get( cve_horario = clave_horario6 )
	
		materia_ig2	= MateriaImpartidaEnGrupo( materia = materia2, horario = horario2, grupo = nuevo_grupo, profesor = profesor )
		materia_ig3	= MateriaImpartidaEnGrupo( materia = materia3, horario = horario3, grupo = nuevo_grupo, profesor = profesor )
		materia_ig4	= MateriaImpartidaEnGrupo( materia = materia4, horario = horario4, grupo = nuevo_grupo, profesor = profesor )
		materia_ig5	= MateriaImpartidaEnGrupo( materia = materia5, horario = horario5, grupo = nuevo_grupo, profesor = profesor )
		materia_ig6	= MateriaImpartidaEnGrupo( materia = materia6, horario = horario6, grupo = nuevo_grupo, profesor = profesor )
		materia_ig2.save()
		materia_ig3.save()
		materia_ig4.save()
		materia_ig5.save()
		materia_ig6.save()

	if ( ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :	
		materia7	= Materia.objects.get( cve_materia = clave_materia7 )
		horario7	= Horario.objects.get( cve_horario = clave_horario7 )
		materia_ig7	= MateriaImpartidaEnGrupo( materia = materia7, horario = horario7, grupo = nuevo_grupo, profesor = profesor )
		materia_ig7.save()

	request.session['mensaje_abrir'] = 0
	return HttpResponseRedirect( '../grupos/' )


def controlador_modificar_grupo( request ):

	clave_empleado	= request.user
	#empleado		= EmpleadoEscolar.objects.get( cve_usuario = clave_empleado )

	clave_grupo		= request.POST.get( 'clave_grupo' )

	grupo			= Grupo.objects.get( cve_grupo = clave_grupo )

	clave_salon_ant	= grupo.cve_salon.cve_salon
	clave_salon_nue	= int ( request.POST.get( 'clave_salon' ) )

	clave_materia1	= request.POST.get( 'materias1' )
	clave_horario1	= int( request.POST.get( 'horarios1' ) )

	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		clave_materia2	= request.POST.get( 'materias2' )
		clave_materia3	= request.POST.get( 'materias3' )
		clave_materia4	= request.POST.get( 'materias4' )
		clave_materia5	= request.POST.get( 'materias5' )
		clave_materia6	= request.POST.get( 'materias6' )
		clave_horario2	= int( request.POST.get( 'horarios2' ) )
		clave_horario3	= int( request.POST.get( 'horarios3' ) )
		clave_horario4	= int( request.POST.get( 'horarios4' ) )
		clave_horario5	= int( request.POST.get( 'horarios5' ) )
		clave_horario6	= int( request.POST.get( 'horarios6' ) )
			
	if ( clave_grupo[0] == '1' ) :
		clave_materia7	= request.POST.get( 'materias7' )
		clave_horario7	= int( request.POST.get( 'horarios7' ) )

	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( ( clave_materia1 == clave_materia2 ) or ( clave_materia1 == clave_materia3 ) or ( clave_materia1 == clave_materia4 ) or ( clave_materia1 == clave_materia5 ) or ( clave_materia1 == clave_materia6 ) or ( clave_materia2 == clave_materia3 ) or ( clave_materia2 == clave_materia4 ) or ( clave_materia2 == clave_materia5 ) or ( clave_materia2 == clave_materia6 ) or ( clave_materia3 == clave_materia4 ) or ( clave_materia3 == clave_materia5 ) or ( clave_materia3 == clave_materia6 ) or ( clave_materia4 == clave_materia5 ) or ( clave_materia4 == clave_materia6 ) or ( clave_materia5 == clave_materia6 ) ) :
			request.session['mensaje_modificar'] = 2
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )
		if ( ( clave_horario1 == clave_horario2 ) or ( clave_horario1 == clave_horario3 ) or ( clave_horario1 == clave_horario4 ) or ( clave_horario1 == clave_horario5 ) or ( clave_horario1 == clave_horario6 ) or ( clave_horario2 == clave_horario3 ) or ( clave_horario2 == clave_horario4 ) or ( clave_horario2 == clave_horario5 ) or ( clave_horario2 == clave_horario6 ) or ( clave_horario3 == clave_horario4 ) or ( clave_horario3 == clave_horario5 ) or ( clave_horario3 == clave_horario6 ) or ( clave_horario4 == clave_horario5 ) or ( clave_horario4 == clave_horario6 ) or ( clave_horario5 == clave_horario6 ) ) :
			request.session['mensaje_modificar'] = 3
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )

	if ( ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( ( clave_materia1 == clave_materia7 ) or ( clave_materia2 == clave_materia7 ) or ( clave_materia3 == clave_materia7 ) or ( clave_materia4 == clave_materia7 ) or ( clave_materia5 == clave_materia7 ) or ( clave_materia6 == clave_materia7 ) ) :
			request.session['mensaje_modificar'] = 2
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )
		if ( ( clave_horario1 == clave_horario7 ) or ( clave_horario2 == clave_horario7 ) or ( clave_horario3 == clave_horario7 ) or ( clave_horario4 == clave_horario7 ) or ( clave_horario5 == clave_horario7 ) or ( clave_horario6 == clave_horario7 ) ) :
			request.session['mensaje_modificar'] = 3
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )

	if ( not ( clave_materia1[1] == clave_grupo[0] ) ) :
		request.session['mensaje_modificar'] = 5
		partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
		return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )

	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( not ( ( clave_materia2[1] == clave_grupo[0] ) and ( clave_materia3[1] == clave_grupo[0] ) and ( clave_materia4[1] == clave_grupo[0] ) and ( clave_materia5[1] == clave_grupo[0] ) and ( clave_materia6[1] == clave_grupo[0] ) ) ) :
			request.session['mensaje_modificar'] = 5
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )

	if ( ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :
		if ( not ( clave_materia7[1] == clave_grupo[0] ) ) :
			request.session['mensaje_modificar'] = 5
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )

	salon_anterior	= Salon.objects.get( cve_salon = clave_salon_ant )
	salon_nuevo		= Salon.objects.get( cve_salon = clave_salon_nue )

	if ( clave_grupo[2] == 'M' ) :
		if ( ( salon_nuevo.bandera == 1 ) or ( salon_nuevo.bandera == 3 ) ) :
			request.session['mensaje_modificar'] = 4
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )
		else :
			salon_nuevo.bandera	= salon_nuevo.bandera + 1
			salon_anterior.bandera	= salon_anterior.bandera - 1

		if ( ( clave_horario1 > 8 ) or ( clave_horario2 > 8 ) or ( clave_horario3 > 8 ) or ( clave_horario4 > 8 ) or ( clave_horario5 > 8 ) or ( clave_horario6 > 8 ) or ( clave_horario7 > 8 ) ) :
			request.session['mensaje_modificar'] = 6
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )
	else :
		if ( ( salon_nuevo.bandera == 2 ) or ( salon_nuevo.bandera == 3 ) ) :
			request.session['mensaje_modificar'] = 4
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )
		else :
			salon_nuevo.bandera	= salon_nuevo.bandera + 2
			salon_anterior.bandera	= salon_anterior.bandera - 2

		if ( ( clave_horario1 < 8 ) or ( clave_horario2 < 8 ) or ( clave_horario3 < 8 ) or ( clave_horario4 < 8 ) or ( clave_horario5 < 8 ) or ( clave_horario6 < 8 ) or ( clave_horario7 < 8 ) ) :
			request.session['mensaje_modificar'] = 6
			partes = ( '../modificar_grupo', str( clave_grupo ), '/' )
			return HttpResponseRedirect( ''.join( str( parte ) for parte in partes if parte is not None ) )

	profesor	= Profesor.objects.get( cve_usuario__clave = 'XXXX000000' )

	MateriaImpartidaEnGrupo.objects.filter( grupo = grupo ).delete()

	salon_anterior.save()
	salon_nuevo.save()
	grupo.cve_salon = salon_nuevo
	grupo.save()

	materia1	= Materia.objects.get( cve_materia = clave_materia1 )
	horario1	= Horario.objects.get( cve_horario = clave_horario1 )
	materia_ig1	= MateriaImpartidaEnGrupo( materia = materia1, horario = horario1, grupo = grupo, profesor = profesor )
	materia_ig1.save()

	if ( ( clave_grupo[0] == '1' ) or ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :	
		materia2	= Materia.objects.get( cve_materia = clave_materia2 )
		materia3	= Materia.objects.get( cve_materia = clave_materia3 )
		materia4	= Materia.objects.get( cve_materia = clave_materia4 )
		materia5	= Materia.objects.get( cve_materia = clave_materia5 )
		materia6	= Materia.objects.get( cve_materia = clave_materia6 )
		horario2	= Horario.objects.get( cve_horario = clave_horario2 )
		horario3	= Horario.objects.get( cve_horario = clave_horario3 )
		horario4	= Horario.objects.get( cve_horario = clave_horario4 )
		horario5	= Horario.objects.get( cve_horario = clave_horario5 )
		horario6	= Horario.objects.get( cve_horario = clave_horario6 )
	
		materia_ig2	= MateriaImpartidaEnGrupo( materia = materia2, horario = horario2, grupo = grupo, profesor = profesor )
		materia_ig3	= MateriaImpartidaEnGrupo( materia = materia3, horario = horario3, grupo = grupo, profesor = profesor )
		materia_ig4	= MateriaImpartidaEnGrupo( materia = materia4, horario = horario4, grupo = grupo, profesor = profesor )
		materia_ig5	= MateriaImpartidaEnGrupo( materia = materia5, horario = horario5, grupo = grupo, profesor = profesor )
		materia_ig6	= MateriaImpartidaEnGrupo( materia = materia6, horario = horario6, grupo = grupo, profesor = profesor )
		materia_ig2.save()
		materia_ig3.save()
		materia_ig4.save()
		materia_ig5.save()
		materia_ig6.save()

	if ( ( clave_grupo[0] == '2' ) or ( clave_grupo[0] == '3' ) or ( clave_grupo[0] == '4' ) ) :	
		materia7	= Materia.objects.get( cve_materia = clave_materia7 )
		horario7	= Horario.objects.get( cve_horario = clave_horario7 )
		materia_ig7	= MateriaImpartidaEnGrupo( materia = materia7, horario = horario7, grupo = grupo, profesor = profesor )
		materia_ig7.save()

	request.session['mensaje_modificar'] = 0
	return HttpResponseRedirect( '../grupos/' )


def controlador_consultar_grupo( request, clave_grupo ):

	clave_empleado				= request.user
	#empleado					= EmpleadoEscolar.objects.get( cve_usuario = clave_empleado )

	clave_grupo					= clave_grupo
	grupo						= Grupo.objects.get( cve_grupo = clave_grupo )

	materiasig					= MateriaImpartidaEnGrupo.objects.filter( grupo = grupo )

	for materia in materiasig :
		
		if ( materia.horario.cve_horario == 1 ) :
			materia1 	= materia.materia.nombre
			m1			= color( materia )
		elif ( materia.horario.cve_horario == 2 ) :
			materia2 	= materia.materia.nombre
			m2			= color( materia )
		elif ( materia.horario.cve_horario == 3 ) :
			materia3 	= materia.materia.nombre
			m3			= color( materia )
		elif ( materia.horario.cve_horario == 4 ) :
			materia4 	= materia.materia.nombre
			m4			= color( materia )
		elif ( materia.horario.cve_horario == 5 ) :
			materia5 	= materia.materia.nombre
			m5			= color( materia )
		elif ( materia.horario.cve_horario == 6 ) :
			materia6 	= materia.materia.nombre
			m6			= color( materia )
		elif ( materia.horario.cve_horario == 7 ) :
			materia7 	= materia.materia.nombre
			m7			= color( materia )
		elif ( materia.horario.cve_horario == 8 ) :
			materia8 	= materia.materia.nombre
			m8			= color( materia )
		elif ( materia.horario.cve_horario == 9 ) :
			materia9 	= materia.materia.nombre
			m9			= color( materia )
		elif ( materia.horario.cve_horario == 10 ) :
			materia10 	= materia.materia.nombre
			m10			= color( materia )
		elif ( materia.horario.cve_horario == 11 ) :
			materia11 	= materia.materia.nombre
			m11			= color( materia )
		elif ( materia.horario.cve_horario == 12 ) :
			materia12 	= materia.materia.nombre
			m12			= color( materia )
		elif ( materia.horario.cve_horario == 13 ) :
			materia13 	= materia.materia.nombre
			m13			= color( materia )
		elif ( materia.horario.cve_horario == 14 ) :
			materia14 	= materia.materia.nombre
			m14			= color( materia )

	request.session['grupo']		= clave_grupo
	request.session['materiasig']	= materiasig

	return render_to_response( 'control/grupos/consultar.html', locals(), context_instance = RequestContext( request ) )

def controlador_reporte_grupo( request, clave_grupo ):
	response	= HttpResponse( mimetype = 'application/pdf' )
	
	clave_grupo	= clave_grupo
	grupo		= Grupo.objects.get( cve_grupo = clave_grupo )

	materiasig	= MateriaImpartidaEnGrupo.objects.filter( grupo = grupo )

	reporte		= reporteDeHorario( queryset = materiasig )
	reporte.generate_by( PDFGenerator, filename = response )
	return response
#************************************************************************************ MIO

def nuevoprof(request):
	bol=request.user
	return render(request, 'control/Agregar_modificar_profesor.html', locals(), context_instance=RequestContext(request))

def agregar_nuevo_prof(request):
	bol=request.user
	if request.method == 'POST': 
		try:
			vera = 1
			if int(request.POST.get('inst_ss')) == 1:
				aux_ssints = 1#'IMSS'
			elif int(request.POST.get('inst_ss')) == 2:
				aux_ssints = 2#'ISSTE'
			elif int(request.POST.get('inst_ss')) == 3:
				aux_ssints = 3#'Seguro Popular'
			else:
				aux_ssints = 0#'No tiene'
			if str(request.POST.get('Sexo')) == 'M':
				aux_sexo = 'M'
			else:
				aux_sexo = 'F'
			if int(request.POST.get('tipo_sangre')) == 1:
				aux_tipo_sangre = 'O+'
			elif int(request.POST.get('tipo_sangre')) == 2:
				aux_tipo_sangre = 'O-'
			elif int(request.POST.get('tipo_sangre')) == 3:
				aux_tipo_sangre = 'A+'
			else:
				aux_tipo_sangre = 'A-'
			aux_cve = request.POST.get('nombre')[:3]
			aux_cve = aux_cve + str(request.POST.get('Apellido_Paterno')[:3])
			aux_cve = aux_cve + str(request.POST.get('Apellido_Materno')[:3])
			aux_cve = aux_cve.upper()
			aux_cve = aux_cve + '0'
			no_existe = 1
			anexo = -1
			while no_existe == 1:
				no_existe = Usuario.objects.filter(clave = aux_cve).count()
				if no_existe > 0:
					anexo = anexo + 1
					aux_cve = str(aux_cve[:-1]) + str(anexo)
					print aux_cve
			aux_password = str(request.POST.get('Apellido_Paterno')[:3])
			print aux_password
			if str(request.POST.get('telefono_Celular')) == '':
				aux_cel = 0
			else:
				aux_cel = request.POST.get('telefono_Celular')
			datos_usuario = Usuario.objects.create(
								#id = aux_id,
								clave = aux_cve,
								nombre = request.POST.get('nombre'),
								apellidoPaterno = request.POST.get('Apellido_Paterno'),
								apellidoMaterno = request.POST.get('Apellido_Materno'),
								curp = request.POST.get('CURP'),
								email_personal = request.POST.get('email_personal'),
								email_institucional = request.POST.get('email_institucional'),
								Telefono_Casa = request.POST.get('telefono_Casa'),
								Telefono_Celular = aux_cel,
								seguroMedico= request.POST.get('SeguroMedico'),
								numero_ss = request.POST.get('numero_ss'),
								seguro_social_institucion = aux_ssints,
								estado = request.POST.get('Estado'),
								municipio_o_delegacion = request.POST.get('municipio_o_delegacion'),
								calle = request.POST.get('calle'),
								colonia = request.POST.get('colonia'),
								lt = request.POST.get('lote'),
								num = request.POST.get('numero'),
								mz = request.POST.get('manzana'),
								cp = request.POST.get('cp'),
								alergias = request.POST.get('alergias'),
								enfermedades= request.POST.get('enfermedades'),
								nacionalidad = request.POST.get('Nacionalidad'),
								sexo = aux_sexo,
								tipo_sangre = aux_tipo_sangre,
								foto = ' ',
								#fecha_nac = datetime.datetime.strptime(request.POST.get('fecha_nac') + " 00:00", '%d/%m/%y %H:%M').strftime('%Y-%m-%d %H:%M').isoformat(),
								#fecha_nac = time.strptime(request.POST.get('fecha_nac') + " 00:00", '%Y-%m-%d %H:%M'),
								fecha_nac = request.POST.get('fecha_nac'),	
								#fecha_alta = datetime.now(),						
								clasificacion = "Profesores"
							)
			datos_usuario.save()
			aux_password = aux_password.upper()
			puf = Usuario.objects.get(clave = aux_cve)
			puf.set_password(aux_password)
			puf.save()
			if int(request.POST.get('Estatus')) == 1:
				aux_status = 'Activo'
			elif int(request.POST.get('Estatus')) == 2:
				aux_status = 'Sabatico'
			elif int(request.POST.get('Estatus')) == 3:
				aux_status = 'Estudiando'
			else:
				aux_status = 'Incapacidad'
			if request.POST.get('tipo') == 1:
				aux_tipo = 'Base'
			else:
				aux_tipo = 'Interino'
			if request.POST.get('horario') == 1:
				aux_hora_entrada = '7:00'
				aux_hora_salida = '15:00'
			else:
				aux_hora_entrada = '15:00'
				aux_hora_salida = '21:00'
			if request.POST.get('grado_estudios') == 1:
				aux_grado_estudios = 'Doctorado'
			elif request.POST.get('grado_estudios') == 2:
				aux_grado_estudios = 'Maestria'
			elif request.POST.get('grado_estudios') == 3:
				aux_grado_estudios = 'Ingenieria'
			else:
				aux_grado_estudios = 'Licenciatura'
			if request.POST.get('laboratorio_cuidar') == 1:
				aux_lab_a_mi_cargo = 1
			elif request.POST.get('laboratorio_cuidar') == 2:
				aux_lab_a_mi_cargo = 2
			elif request.POST.get('laboratorio_cuidar') == 3:
				aux_lab_a_mi_cargo = 3
			elif request.POST.get('laboratorio_cuidar') == 4:
				aux_lab_a_mi_cargo = 4
			elif request.POST.get('laboratorio_cuidar') == 5:
				aux_lab_a_mi_cargo = 5
			elif request.POST.get('laboratorio_cuidar') == 6:
				aux_lab_a_mi_cargo = 6
			elif request.POST.get('laboratorio_cuidar') == 7:
				aux_lab_a_mi_cargo = 7
			elif request.POST.get('laboratorio_cuidar') == 8:
				aux_lab_a_mi_cargo = 8
			else:
				aux_lab_a_mi_cargo = 0
			if request.POST.get('depto') == 1:
				aux_depto = 1
			elif request.POST.get('depto') == 3:
				aux_depto = 3
			elif request.POST.get('depto') == 4:
				aux_depto = 4
			else:
				aux_depto = 5
			datos_profesor = Profesor.objects.create(
								cve_usuario = Usuario.objects.filter(clave=aux_cve)[0],
								tipo = aux_tipo,
								hora_entrada = aux_hora_entrada,
								hora_salida = aux_hora_salida,
								grado_estudios = aux_grado_estudios,
								carrera = request.POST.get('carrera'),
								salario = request.POST.get('salario'),
								rol_academico = 'normal',
								Departamento = Depto.objects.filter(id=aux_depto)[0],
								status = aux_status,
								comentario = ' '
								#grupo_tutorado_id = ''									
							 )
			datos_profesor.save()
			return render(request, 'control/controlinicio.html', locals(), context_instance=RequestContext(request))
		except:  
			vera = 2
			return render(request, 'control/Agregar_modificar_profesor.html', locals(), context_instance=RequestContext(request))

#*************************

def modificarprofesor(request,dato):
	bol=request.user
	id_prof = dato
	datos_profesor = Profesor.objects.filter(cve_usuario__clave=dato)[0]
	datos_usuario = Usuario.objects.filter(clave=dato)[0]
	aux_fechanac = datos_usuario.fecha_nac.isoformat()
	try:
		puf = Usuario.objects.get(clave = dato)
		datos_lab = Laboratorio.objects.filter(encargado_id = puf.id)[0]
		if int(datos_lab.id) == 1:
			aux_lab = 1
		elif int(datos_lab.id) == 2:
			aux_lab = 2
		elif int(datos_lab.id) == 3:
			aux_lab = 3
		elif int(datos_lab.id) == 4:
			aux_lab = 4
		elif int(datos_lab.id) == 5:
			aux_lab = 5
		elif int(datos_lab.id) == 6:
			aux_lab = 6
		elif int(datos_lab.id) == 7:
			aux_lab = 7
		else:
			aux_lab = 8
	except:
			aux_lab = 9		
	if str(datos_profesor.status) == "Activo":
		aux_act = 1
	elif str(datos_profesor.status) == "Sabatino":
		aux_act = 2
	elif str(datos_profesor.status) == "Estudiando":
		aux_act = 3
	else:
		aux_act = 4
	if str(datos_profesor.tipo) == "Base":
		aux_tipo = 1
	else:
		aux_tipo = 2
	if str(datos_profesor.grado_estudios) == "Doctorado":
		aux_grado = 1
	elif str(datos_profesor.grado_estudios) == "Maestria":
		aux_grado = 2
	elif str(datos_profesor.grado_estudios) == "Ingenieria":
		aux_grado = 3
	else:
		aux_grado = 4
	if int(datos_profesor.Departamento_id) == 1:
		aux_depto = 1
	elif int(datos_profesor.Departamento_id) == 3:
		aux_depto = 3
	elif int(datos_profesor.Departamento_id) == 4:
		aux_depto = 4
	else:
		aux_depto = 5

	return render(request, 'control/modificar_profesor.html', locals(), context_instance=RequestContext(request))
	
def modificar_prof(request):
	bol=request.user
	if request.method == 'POST': 
		try:
			raul = 1
			cambios_profesor = Usuario.objects.filter(clave = request.POST.get('id_usuario'))[0]		
			cambios_profesor.nombre = request.POST.get('nombre')
			cambios_profesor.apellidoPaterno = request.POST.get('Apellido_Paterno')
			cambios_profesor.apellidoMaterno = request.POST.get('Apellido_Materno')
			cambios_profesor.curp = request.POST.get('CURP')
			cambios_profesor.email_institucional = request.POST.get('email_institucional')
			cambios_profesor.estado = request.POST.get('Estado')
			cambios_profesor.municipio_o_delegacion = request.POST.get('municipio_o_delegacion')
			cambios_profesor.calle = request.POST.get('calle')
			cambios_profesor.colonia = request.POST.get('colonia')
			cambios_profesor.lt = request.POST.get('lote')
			cambios_profesor.num = request.POST.get('numero')
			cambios_profesor.mz = request.POST.get('manzana')
			cambios_profesor.cp = request.POST.get('cp')
			cambios_profesor.alergias = request.POST.get('alergias')
			cambios_profesor.enfermedades= request.POST.get('enfermedades')
			cambios_profesor.fecha_nac = request.POST.get('fecha_nac')
			cambios_profesor.save()
			cambios_profesor2 = Profesor.objects.filter(cve_usuario__clave = request.POST.get('id_usuario'))[0]	
			if int(request.POST.get('Estatus')) == 1:
				aux_status = 'Activo'
			elif int(request.POST.get('Estatus')) == 2:
				aux_status = 'Sabatico'
			elif int(request.POST.get('Estatus')) == 3:
				aux_status = 'Estudiando'
			else:
				aux_status = 'Incapacidad'
			if int(request.POST.get('tipo')) == 1:
				aux_tipo = 'Base'
			else:
				aux_tipo = 'Interino'
			if int(request.POST.get('grado_estudios')) == 1:
				aux_grado_estudios = 'Doctorado'
			elif int(request.POST.get('grado_estudios')) == 2:
				aux_grado_estudios = 'Maestria'
			elif int(request.POST.get('grado_estudios')) == 3:
				aux_grado_estudios = 'Ingenieria'
			else:
				aux_grado_estudios = 'Licenciatura'
			if int(request.POST.get('laboratorio_cuidar')) == 1:
				aux_lab_a_mi_cargo = 1
			elif int(request.POST.get('laboratorio_cuidar')) == 2:
				aux_lab_a_mi_cargo = 2
			elif int(request.POST.get('laboratorio_cuidar')) == 3:
				aux_lab_a_mi_cargo = 3
			elif int(request.POST.get('laboratorio_cuidar')) == 4:
				aux_lab_a_mi_cargo = 4
			elif int(request.POST.get('laboratorio_cuidar')) == 5:
				aux_lab_a_mi_cargo = 5
			elif int(request.POST.get('laboratorio_cuidar')) == 6:
				aux_lab_a_mi_cargo = 6
			elif int(request.POST.get('laboratorio_cuidar')) == 7:
				aux_lab_a_mi_cargo = 7
			elif int(request.POST.get('laboratorio_cuidar')) == 8:
				aux_lab_a_mi_cargo = 8
			else:
				aux_lab_a_mi_cargo = 0
			if int(request.POST.get('depto')) == 1:
				aux_depto = "Basicas"
			elif int(request.POST.get('depto')) == 3:
				aux_depto = "Ingenieria en Sistemas C"
			elif int(request.POST.get('depto')) == 4:
				aux_depto = "Computacion"
			else:
				aux_depto = "Formacion Integral e Inst"

			cambios_profesor2.tipo = aux_tipo
			cambios_profesor2.grado_estudios = aux_grado_estudios
			cambios_profesor2.carrera = request.POST.get('carrera')
			cambios_profesor2.salario = request.POST.get('salario')
			temporal=Depto.objects.filter(nombre_depto=aux_depto)[0]
			cambios_profesor2.Departamento = temporal
			cambios_profesor2.status = aux_status
			cambios_profesor2.save()
			puf = Usuario.objects.get(clave = request.POST.get('id_usuario'))
			try:
				cambios_profesor_lab2 = Laboratorio.objects.filter(encargado_id = puf.id)[0]
				cambios_profesor_lab2.encargado_id = None
				cambios_profesor_lab2.save()
			except:
				print "nada"
			if aux_lab_a_mi_cargo != 0:
				cambios_profesor_lab = Laboratorio.objects.filter(id = aux_lab_a_mi_cargo)[0]
				cambios_profesor_lab.encargado_id = puf.id
				cambios_profesor_lab.save()
			return render(request, 'control/buscarprof.html', locals(), context_instance=RequestContext(request))
		except:  
			raul = 2
			return render(request, 'control/modificar_profesor.html', locals(), context_instance=RequestContext(request))
			
def reporteProf(request,dato):
	bol = request.user
	a = Usuario.objects.filter(clave = dato)[0]
	profesor = Profesor.objects.filter(cve_usuario__clave = a)
	resp = HttpResponse(mimetype='application/pdf')
	report = reporteProfesor(queryset=profesor)
	report.generate_by(PDFGenerator, filename=resp)
	return resp

def darDeBaja(request):
	bol=request.user
	materia=request.POST.get('materia')
	alum=request.POST.get('clave3')
	l=materia.split()
	mate=l[0]
	print alum
	print mate
	try:
		us=Usuario.objects.filter(clave=alum)[0]
		print 1111
		al=Alumno.objects.filter(cve_usuario=us)[0]
		print 3333
		p=AlumnoTomaClaseEnGrupo.objects.filter(alumno=al)
		print 5555
		for pic in p:
			aux=str(pic.materia_grupo).split()
			if aux[0]==mate:
				q=pic
				print q.materia_grupo
				break
		
		a=AlumnoTomaClaseEnGrupo.objects.filter(alumno=al)
		print 77777
		q.delete();
		notif2=1
		print 8888
		
	except:
		print 22222
	return render(request, 'control/darBajaMaterias.html', locals(), context_instance=RequestContext(request))
def darBajaMat(request):
	bol=request.user
	clave= request.POST.get('clave2')
	try:
		us=Usuario.objects.filter(clave=clave)[0]
		al=Alumno.objects.filter(cve_usuario=us)[0]
		a=AlumnoTomaClaseEnGrupo.objects.filter(alumno=al)
		filas=len(a)
		print len(a)	
	except:
		print 1234
	return render(request, 'control/darBajaMaterias.html', locals(), context_instance=RequestContext(request))

def agregarmateria(request,dato):
	bol=request.user
	clave=dato
	us=Usuario.objects.filter(clave=clave)[0]
	al=Alumno.objects.filter(cve_usuario=us)[0]
	grupos=AlumnoTomaClaseEnGrupo.objects.filter(alumno=al)
	final=[]
	temporal=[]
	tot=0
	if(len(grupos)>0 and len(grupos)<8):
		try:			
			for f in grupos:
				print f.materia_grupo.materia.nombre
			kar=kardex.objects.filter(alumno=al)		
			for g in kar:
				print g.materia.nombre
			materias=Materia.objects.all()
			lista=[]
			listamaterias=[]
			listakardex=[]
			listatomaclases=[]
			for d in materias:
				listamaterias.append(d.nombre)
			for d in grupos:
				listatomaclases.append(d.materia_grupo.materia.nombre)
			for d in kar:
				listakardex.append(d.materia.nombre)
			
			for f in range(len(listamaterias)):
				if(listamaterias[f] not in listatomaclases and listamaterias[f] not in listakardex):
					lista.append(listamaterias[f])									
			#for c in materias:
			#	for d in grupos:
			#		for g in kar:
			#			if(c.nombre!=g.materia.nombre and c.nombre!=d.materia_grupo.materia.nombre):
			#				if c.nombre not in lista:
			#					lista.append(c.nombre)													
										
			for s in range(len(lista)):
				try:
					grupo=MateriaImpartidaEnGrupo.objects.filter(materia__nombre=lista[s])
					for r in range(len(grupo)):
						"""tupla=[]
						print "primero"
						tupla.append(grupo[r].materia.nombre)
						print "5"
						tupla.append(grupo[r].grupo.cve_grupo)
						print "6"
						tupla.append(grupo[r].horario.cve_horario)						
						print "7"
						final.append(tupla)
						print "agregue"""
						if(grupo[r].cupo!=0):
							final.append(grupo[r])
				except:
					print "no entre"
			print "salgo"
			#tot=len(final)
			#for t in range(len(final)):
				#print final[t]		
				
		except:
			print "error"
	return render(request, 'control/modificarhorario.html', locals(), context_instance=RequestContext(request))

def agregarhorario(request,dato):
	bol=request.user
	print dato
	datos=dato.split('-')
	grupo=MateriaImpartidaEnGrupo.objects.filter(materia__nombre=datos[0],grupo__cve_grupo=datos[1])[0]
	us=Usuario.objects.filter(clave=datos[2])[0]
	al=Alumno.objects.filter(cve_usuario=us)[0]
	grupos=AlumnoTomaClaseEnGrupo.objects.filter(alumno=al)
	notif=0
	final=[]
	for a in grupos:
		if(a.materia_grupo.horario.cve_horario==grupo.horario.cve_horario):
			notif=1
	if(notif==1):
		print "Ya esta el horario"
		tot=0			
		for f in grupos:
			print f.materia_grupo.materia.nombre
		kar=kardex.objects.filter(alumno=al)		
		for g in kar:
			print g.materia.nombre
		materias=Materia.objects.all()
		lista=[]
		for c in materias:
			for d in grupos:
				for g in kar:
					if(c.nombre!=g.materia.nombre and c.nombre!=d.materia_grupo.materia.nombre):
						if c.nombre not in lista:
							lista.append(c.nombre)	
		for s in range(len(lista)):
			try:
				grupo=MateriaImpartidaEnGrupo.objects.filter(materia__nombre=lista[s])
				for r in range(len(grupo)):
					if(grupo[r].cupo!=0):
						final.append(grupo[r])
				notif=3				
			except:
				print "algo mal"		
		return render(request, 'control/modificarhorario.html', locals(), context_instance=RequestContext(request))
	else:		
		nuevamat=AlumnoTomaClaseEnGrupo.objects.create(alumno=al,materia_grupo=grupo)
		grupo.cupo-=1
		grupo.save()
		notif=2
		
	print grupo.materia.nombre
	#print datos[0],datos[1]
	return render(request, 'control/buscarAlum.html', locals(), context_instance=RequestContext(request))

def alumnoKardex(request):
	bol=request.user
	hoy=datetime.today()
	fechaFinal=datetime.strptime("19/11/13","%d/%m/%y")
	alumnos=AlumnoTomaClaseEnGrupo.objects.all()
	f=calendarios.objects.all()
	for i in f:
		fecha=i.finets
		print i.finets
		print hoy
	print fecha	
	
	
	if(hoy > fechaFinal):
		
		for al in alumnos:
			print al.alumno.cve_usuario
			print al.materia_grupo
			print al.materia_grupo.materia.cve_materia
			print al.calificacion
				
			if(al.calificacion is not None):

				a=Alumno.objects.filter(cve_usuario=al.alumno.cve_usuario)[0]
				b=Materia.objects.filter(cve_materia=al.materia_grupo.materia.cve_materia)[0]
				try:
						p=kardex(alumno=a,materia=b,calificacion=al.calificacion,periodo=al.periodo,evaluacion="ORD")
						p.save()
						print "CREE ORD"
				except:	
						kardex.objects.filter(alumno=a,materia=b).update(calificacion=al.calificacion,periodo=al.periodo,evaluacion="ORD")
						print "ACT ORD"
					
			if(al.calificacionExtra is not None and al.calificacionExtra>al.calificacion): 	
				a=Alumno.objects.filter(cve_usuario=al.alumno.cve_usuario)[0]
				b=Materia.objects.filter(cve_materia=al.materia_grupo.materia.cve_materia)[0]
				try:
						p=kardex(alumno=a,materia=b,calificacion=al.calificacionExtra,periodo=al.periodo,evaluacion="EXT")
						p.save()
						print "CREE EXT"
				except:	
						kardex.objects.filter(alumno=a,materia=b).update(calificacion=al.calificacionExtra,periodo=al.periodo,evaluacion="EXT")
						print "MOD EXT"
						

			if(al.calificacion < 6 and al.calificacionExtra < 6):
				try:	
					ae=AlumnoTomaEts.objects.filter(alumno=al.alumno.cve_usuario)[0]
					b=Materia.objects.filter(cve_materia=al.materia_grupo.materia.cve_materia)[0]
					kardex.objects.filter(alumno=ae.alumno.cve_usuario,materia=b ).update(calificacion=ae.calificacion,periodo=al.periodo,evaluacion="ETS")
				except:
						print "Hola"
			
	return render(request, 'control/controlinicio.html', locals(), context_instance=RequestContext(request))


