# Create your views here.
# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from principal.models import *
import time
from django.utils import timezone
  
from reporteHorario import *
from reporteKardex import *
from reporteBoleta import *
from reporteConstancia import *
from reporteETS import *
from geraldo.generators import PDFGenerator
# Create your views here.
def alumnoInicio(request):

	bol=request.user
	hora=datetime.now(tz=timezone.get_default_timezone())
	try:
		alu=CitaInsc.objects.get(alumno__cve_usuario=bol)
		cita=alu.cita
		inscrito=alu.inscrito
	except:
		cita=0
		inscrito=0
		return render(request, 'Alumno/Alinicio.html', locals(), context_instance=RequestContext(request))
	return render(request, 'Alumno/Alinicio.html', locals(), context_instance=RequestContext(request))

def alumnoDatosGen(request):
	
	bol=request.user
	nombreCompleto=Usuario.get_full_name(bol)
	if bol.sexo=='M':
		sexo="Masculino"
	else:
		sexo="Femenino"
	bol2=Alumno.objects.get(cve_usuario=bol)
	aux=0

	if request.method=='POST':
		if 'mod_datgen' in request.POST:
			aux=1
			#print "datos generales"
			return render(request, 'Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))
					

		elif 'mod_nac' in request.POST:
			aux=2
			print "nacimiento"
			return render(request, 'Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))

		elif 'mod_dir' in request.POST:
			aux=3
			print "direccion"
			return render(request, 'Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))

		elif 'mod_tutor' in request.POST:
			aux=5
			print "tutor"
			return render(request, 'Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))

	return render(request, 'Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))

def datgenRedirect(request):
	return HttpResponseRedirect('../alumnoDatosGen/')


def actualizarInfo(request):
	bol=request.user
	if 'fin_datgen' in request.POST:
		bol=request.user
		curp=request.POST.get('al_curp')
		Usuario.objects.filter(clave=bol).update(curp=curp)
		aux=0
		notif=1
		return render_to_response('Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))
		#return HttpResponseRedirect('../alumnoDatosGen/')

	elif 'fin_nac' in request.POST:		
		nac=request.POST.get('al_fnac')
		nacionalidad=request.POST.get('al_nacionalidad')
		Usuario.objects.filter(clave=bol).update(nacionalidad=nacionalidad)
		aux=0
		notif=1
		return render_to_response('Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))
		#return HttpResponseRedirect('../alumnoDatosGen/')

	elif 'fin_dir' in request.POST:
		calle=request.POST.get('al_calle')
		#num=request.POST.get('al_numint')
		num1=request.POST.get('al_numint')
		if num1=="":
			num=None
		else:
			num=num1
		colonia=request.POST.get('al_colonia')
		cp1=request.POST.get('al_cp')
		if cp1=="":
			cp=None
		else:
			cp=cp1
		edo=request.POST.get('al_estado')
		delmun=request.POST.get('al_delmun')
		tel=request.POST.get('al_tel')
		movil1=request.POST.get('al_movil')
		if movil1=="":
			movil=None
		else:
			movil=movil1
		email=request.POST.get('al_email')
		Usuario.objects.filter(clave=bol).update(calle=calle, num=num, colonia=colonia, cp=cp, estado=edo, municipio_o_delegacion=delmun, Telefono_Casa=tel, Telefono_Celular=movil, email_institucional=email)
		aux=0
		notif=1
		return render_to_response('Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))
		#return HttpResponseRedirect('../alumnoDatosGen/')

	elif 'fin_tutor' in request.POST:
		bol=request.user
		tutor=request.POST.get('al_tutor')
		Alumno.objects.filter(cve_usuario=bol).update(tutor_legal=tutor)
		aux=0
		notif=1
		return render_to_response('Alumno/Aldatosgenerales.html', locals(), context_instance=RequestContext(request))
		#return HttpResponseRedirect('../alumnoDatosGen/')


def alumnoKardex(request):
	bol=request.user
	return render(request, 'Alumno/Alkardex.html', locals(), context_instance=RequestContext(request))

def kardexframe(request):
	bol=request.user
	cals=[]

	nivel1=kardex.objects.filter(alumno__cve_usuario=bol, materia__nivel=1)
	nivel2=kardex.objects.filter(alumno__cve_usuario=bol, materia__nivel=2)
	nivel3=kardex.objects.filter(alumno__cve_usuario=bol, materia__nivel=3)
	nivel4=kardex.objects.filter(alumno__cve_usuario=bol, materia__nivel=4)
	nivel5=kardex.objects.filter(alumno__cve_usuario=bol, materia__nivel=5)

	len1=len(nivel1)
	len2=len(nivel2)
	len3=len(nivel3)
	len4=len(nivel4)
	len5=len(nivel5)

	if len1!=0 or len2!=0 or len3!=0 or len4!=0 or len5!=0:		

		for alumno in nivel1:
			cals.append(alumno.calificacion)

		for alumno in nivel2:
			cals.append(alumno.calificacion)

		for alumno in nivel3:
			cals.append(alumno.calificacion)

		for alumno in nivel4:
			cals.append(alumno.calificacion)

		for alumno in nivel5:
			cals.append(alumno.calificacion)

		promedio=sum(cals)/len(cals)

	

	return render(request, 'Alumno/Alkardex-frame.html', locals(), context_instance=RequestContext(request))

def alumnoHorario(request):
	bol=request.user
	return render(request, 'Alumno/Alhorario.html', locals(), context_instance=RequestContext(request))

def color(materia):
    if(materia.clasificacion=='Institucional'):
        return 'm1'

    elif(materia.clasificacion=='Cientifica_basica'):
        return 'm4'

    elif(materia.clasificacion=='Profesional'):
        return 'm3'

    elif(materia.clasificacion=='Terminal_integracion'):
        return 'm2'
    else:
        return 'm3'

def nombreCompleto(cve_usuario):
	nom = cve_usuario.nombre
	ap = cve_usuario.apellidoPaterno
	am = cve_usuario.apellidoMaterno
	nc = ap + ' ' + am + ' ' + nom
	return nc

def horarioframe(request):
	bol=request.user
	Grupos=AlumnoTomaClaseEnGrupo.objects.filter(alumno__cve_usuario__clave=bol)
	for alumno in Grupos:

		if(alumno.materia_grupo.horario.cve_horario==1):
			materia1=alumno.materia_grupo.materia.nombre
			m1=color(alumno.materia_grupo.materia)
			grupo1=alumno.materia_grupo.grupo
			prof1=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==2):
			materia2=alumno.materia_grupo.materia.nombre
			m2=color(alumno.materia_grupo.materia)
			grupo2=alumno.materia_grupo.grupo
			prof2=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==3):
			materia3=alumno.materia_grupo.materia.nombre
			m3=color(alumno.materia_grupo.materia)
			grupo3=alumno.materia_grupo.grupo
			prof3=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==4):
			materia4=alumno.materia_grupo.materia.nombre
			m4=color(alumno.materia_grupo.materia)
			grupo4=alumno.materia_grupo.grupo
			prof4=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==5):
			materia5=alumno.materia_grupo.materia.nombre
			m5=color(alumno.materia_grupo.materia)
			grupo5=alumno.materia_grupo.grupo
			prof5=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==6):
			materia6=alumno.materia_grupo.materia.nombre
			m6=color(alumno.materia_grupo.materia)
			grupo6=alumno.materia_grupo.grupo
			prof6=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==7):
			materia7=alumno.materia_grupo.materia.nombre
			m7=color(alumno.materia_grupo.materia)
			grupo7=alumno.materia_grupo.grupo
			prof7=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==8):
			materia8=alumno.materia_grupo.materia.nombre
			m8=color(alumno.materia_grupo.materia)
			grupo8=alumno.materia_grupo.grupo
			prof8=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)

		if(alumno.materia_grupo.horario.cve_horario==9):
			materia9=alumno.materia_grupo.materia.nombre
			m9=color(alumno.materia_grupo.materia)
			grupo9=alumno.materia_grupo.grupo
			prof9=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==10):
			materia10=alumno.materia_grupo.materia.nombre
			m10=color(alumno.materia_grupo.materia)
			grupo10=alumno.materia_grupo.grupo
			prof10=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==11):
			materia11=alumno.materia_grupo.materia.nombre
			m11=color(alumno.materia_grupo.materia)
			grupo11=alumno.materia_grupo.grupo
			prof11=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==12):
			materia12=alumno.materia_grupo.materia.nombre
			m12=color(alumno.materia_grupo.materia)
			grupo12=alumno.materia_grupo.grupo
			prof12=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==13):
			materia13=alumno.materia_grupo.materia.nombre
			m13=color(alumno.materia_grupo.materia)
			grupo13=alumno.materia_grupo.grupo
			prof13=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==14):
			materia14=alumno.materia_grupo.materia.nombre
			m14=color(alumno.materia_grupo.materia)
			grupo14=alumno.materia_grupo.grupo
			prof14=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)
		elif(alumno.materia_grupo.horario.cve_horario==15):
			materia15=alumno.materia_grupo.materia.nombre
			m15=color(alumno.materia_grupo.materia)
			grupo15=alumno.materia_grupo.grupo
			prof15=nombreCompleto(alumno.materia_grupo.profesor.cve_usuario)

	return render(request, 'Alumno/Alhorario-frame.html', locals(), context_instance=RequestContext(request))


def alumnoCalifsemestre(request):
	bol=request.user
	return render(request, 'Alumno/Alcalsemestre.html', locals(), context_instance=RequestContext(request))


def califsemestreframe(request):
	bol=request.user
	Califs=AlumnoTomaClaseEnGrupo.objects.filter(alumno__cve_usuario__clave=bol)	
	return render(request, 'Alumno/Alcalsemestre-frame.html', locals(), context_instance=RequestContext(request))

def alumnoCalifets(request):
	bol=request.user
	return render(request, 'Alumno/Alcalets.html', locals(), context_instance=RequestContext(request))

def califetsframe(request):
	bol=request.user
	calets=AlumnoTomaEts.objects.filter(alumno__cve_usuario__clave=bol)	
	return render(request, 'Alumno/Alcalets-frame.html', locals(), context_instance=RequestContext(request))

def alumnoCalifsaberes(request):
	bol=request.user
	return render(request, 'Alumno/Alcalsaberes.html', locals(), context_instance=RequestContext(request))

def califsaberesframe(request):
	bol=request.user
	calspa=SaberesPrevios.objects.filter(Alumno__cve_usuario__clave=bol)
	regcalspa=len(calspa)
	return render(request, 'Alumno/Alcalsaberes-frame.html', locals(), context_instance=RequestContext(request))

def alumnoInscEts(request):
	bol=request.user
	return render(request, 'Alumno/Alinscribirets.html', locals(), context_instance=RequestContext(request))

def inscetsframe(request):
	bol=request.user
	rep=[]
	materiasCursadas=AlumnoTomaClaseEnGrupo.objects.filter(alumno__cve_usuario__clave=bol)

	for alumno in materiasCursadas:
		if alumno.calificacion<6:
			if alumno.calificacionExtra<6:
				rep.append(alumno)


	hayreprobadas=len(rep)

	if hayreprobadas!=0:
		matrep=AlumnoTomaEts.objects.filter(alumno__cve_usuario=bol)

	#for alumno in rep:
	#	cvemat=alumno.materia_grupo.materia.cve_materia
	#	al=AlumnoTomaEts(alumno=bol,ets=cvemat)
	#	al.save()

	return render(request, 'Alumno/Alinscribirets-frame.html', locals(), context_instance=RequestContext(request))

def alumnoInscSaberes(request):
	bol=request.user

	return render(request, 'Alumno/Alinscribirsaberes.html', locals(), context_instance=RequestContext(request))

def inscsaberesframe(request):
	bol=request.user
	mat_disponibles=[]
	materias=Materia.objects.all().order_by('nivel')
	registrospa=SaberesPrevios.objects.filter(Alumno__cve_usuario__clave=bol)
	regs=len(registrospa)

	for nombre in materias:
		cvemat=nombre.cve_materia
		if (ya_cursada(bol, cvemat)):
			print "mat cursada: "+nombre.nombre
		elif nombre.tipo != "Optativa":
			mat_disponibles.append(nombre)
		else:
			print "es Optativa"
			
	return render(request, 'Alumno/Alinscribirsaberes-frame.html', locals(), context_instance=RequestContext(request))

def ya_cursada(bol, cvemat):
	alkardex=kardex.objects.filter(alumno__cve_usuario__clave=bol)
	check=0
	for alumno in alkardex:
		if alumno.materia.cve_materia==cvemat:
			check=1

	if check==1:
		return True
	else:
		return False


def procesarSpa(request):
	bol=request.user

	al=Alumno.objects.get(cve_usuario__clave=bol)

	if 'fin_spa' in request.POST:

		eleccion=request.POST.getlist('spa')		

		if len(eleccion) > 3:
			flagspa=3
			return render(request, 'Alumno/Alinscribirsaberes-frame.html', locals(), context_instance=RequestContext(request))
		else:
			for x in eleccion:
				mat=Materia.objects.get(cve_materia=x)
				reg=SaberesPrevios(Alumno=al, Materia=mat)
				reg.save()
			flagspa=1

			return render(request, 'Alumno/Alinscribirsaberes-frame.html', locals(), context_instance=RequestContext(request))
		print eleccion


def alumnoTutor(request):
	bol=request.user
	try:
		dat=Alumno.objects.get(cve_usuario=bol)
		aux=dat.tutor_escolar.cve_usuario
		nomcomprof=Usuario.get_full_name(aux)
		print dat.tutor_escolar.hora_entrada
		print dat.tutor_escolar.hora_salida
	except:
		sintutor=1
		print "sin tutor"
	
	return render(request, 'Alumno/Altutor.html', locals(), context_instance=RequestContext(request))

def alumnoEvaluarprofs(request):
	bol=request.user
	return render(request, 'Alumno/Alevaluarprofs.html', locals(), context_instance=RequestContext(request))

def evaluarprofsframe1(request):
	bol=request.user
	inscrito=AlumnoTomaClaseEnGrupo.objects.filter(alumno__cve_usuario__clave=bol)
	#evaluados=EvaluacionProfesor.objects.filter(alumno__cve_usuario__clave=bol)
	#print len(evaluados)

	lista_profs=[]
	
	for alumno in inscrito:
		cvemateria=alumno.materia_grupo.materia.cve_materia
		cveprof=alumno.materia_grupo.profesor.cve_usuario.clave
		if(esta_evaluado(bol, cvemateria, cveprof)):
			print "profesar evaluado"
		else:
			lista_profs.append(alumno)

	#print lista_profs
	no_evaluados=len(lista_profs)


	return render(request, 'Alumno/Alevaluarprofs-frame.html', locals(), context_instance=RequestContext(request))

def esta_evaluado(bol, cvemat, cveprof):
	check=0
	profev=EvaluacionProfesor.objects.filter(alumno__cve_usuario__clave=bol)
	
	for alumno in profev:
		if alumno.profesor.cve_usuario.clave==cveprof and alumno.materia.cve_materia==cvemat:
			check=1

	if check == 1:
		return True
	else:
		return False



def evaluarprofsframe2(request,idmat):
	bol=request.user

	print bol
	print idmat
	datosprof=AlumnoTomaClaseEnGrupo.objects.get(alumno__cve_usuario__clave=bol, materia_grupo__materia__cve_materia=idmat)

	name=nombreCompleto(datosprof.materia_grupo.profesor.cve_usuario)
	group=datosprof.materia_grupo.grupo
	nameMat=datosprof.materia_grupo.materia.nombre

	return render(request, 'Alumno/Alevaluarprofs-frame2.html', locals(), context_instance=RequestContext(request))


def realizarEvaluacion(request,idmat):
	bol=request.user
	datosprof=AlumnoTomaClaseEnGrupo.objects.get(alumno__cve_usuario__clave=bol, materia_grupo__materia__cve_materia=idmat)
	idprof=datosprof.materia_grupo.profesor.cve_usuario.clave

	al=Alumno.objects.get(cve_usuario__clave=bol)
	profe=Profesor.objects.get(cve_usuario__clave=idprof)
	mat=Materia.objects.get(cve_materia=idmat)

	if 'fin_ev' in request.GET:
		#print "entraste a realizarEvaluacion"
		flagep=1
		p1=request.GET['preg1']
		p2=request.GET['preg2']
		p3=request.GET['preg3']
		p4=request.GET['preg4']
		p5=request.GET['preg5']

		reg=EvaluacionProfesor(alumno=al,profesor=profe,materia=mat,pregunta1=p1,pregunta2=p2,pregunta3=p3,pregunta4=p4,pregunta5=p5)
		reg.save()

	return render(request, 'Alumno/Alevaluarprofs-frame2.html', locals(), context_instance=RequestContext(request))




def alumnoHorariolabs(request):
	bol=request.user
	return render(request, 'Alumno/Alhorariolabs.html', locals(), context_instance=RequestContext(request))

def horariolabsframe(request):
	labs=MateriaImpartidaEnLab.objects.all()
	for cve_materia_grupo in labs:
		print cve_materia_grupo

	fil=MateriaImpartidaEnLab.objects.filter(nombre_lab__nombre="LS1")
	for cve_materia_grupo in fil:
		print cve_materia_grupo.cve_materia_grupo.horario
		print cve_materia_grupo.dia
	return render(request, 'Alumno/Alhorariolabs-frame.html', locals(), context_instance=RequestContext(request))

def alumnoCambiarpass(request):
	bol=request.user
	return render(request, 'Alumno/Alcambiarpass.html', locals(), context_instance=RequestContext(request))

def cambiarPass(request):
	bol=request.user
	if request.method=='POST':
		passact=request.POST.get('passact')
		passnuevo=request.POST.get('passnuevo')
		conpassnuevo=request.POST.get('con-passnuevo')
		if passact=="" or passnuevo=="" or conpassnuevo=="":
			print "vacios"
			notif=4
			return render(request, 'Alumno/Alcambiarpass.html', locals(), context_instance=RequestContext(request))

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
					return render(request, 'Alumno/Alcambiarpass.html', locals(), context_instance=RequestContext(request))
				else:
					print "pass nuevo no coinciden"
					notif=3
					return render(request, 'Alumno/Alcambiarpass.html', locals(), context_instance=RequestContext(request))
				
				print "passnuevo: "+passnuevo
				print "confir passnuevo: "+conpassnuevo
				
	    	if acceso is None:
	    		notif=2
	    		print "contrasena incorrecta"
	    		return render(request, 'Alumno/Alcambiarpass.html', locals(), context_instance=RequestContext(request))	
	

def alumnoinscsem(request):
	bol=request.user
	request.session['cred']=0
	matInfo=Materia.objects.all()
	return render(request,'Alumno/AlInscribir.html',locals(),context_instance=RequestContext(request))
	
def getMateria(request):
	metod=request.GET['metod']
	niv=request.GET['nivel']
	response=HttpResponse()
	response.write("<select id='selector' onChange='getInfo(this.value)'>")
	if metod==str(1):
		matInfo=Materia.objects.filter(nivel=niv)
		for materia in matInfo:
			response.write("<option value='"+materia.cve_materia+"'>"+materia.nombre+"</option>")
	else:
		grupInfo=Grupo.objects.all()
		for grupo in grupInfo:
			if grupo.cve_grupo[0]==niv:
				response.write("<option value='"+grupo.cve_grupo+"'>"+grupo.cve_grupo+"</option>")
	response.write("</select>")
	if request.is_ajax():
		return response
		
def getResult(request):
	clave=request.GET['clave']
	metod=request.GET['metod']
	response=HttpResponse()
	response.write("<table id='hor-minimalist-a'><thead>")
	if metod==str(1):
		matInfo=Materia.objects.get(cve_materia=clave)
		matgrupInfo=MateriaImpartidaEnGrupo.objects.filter(materia=matInfo)
		response.write("<tr><th scope='col'>Grupo</th><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMateria&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspProfesor&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbspLunes&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbsp&nbspMartes&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbspMiercoles&nbsp</th><th scope='col'>&nbsp&nbsp&nbspJueves&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbspViernes&nbsp&nbsp&nbsp</th><th>Cupo</th><th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th></tr></thead><tbody>")
		for mat in matgrupInfo:
			inscritos=AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=mat).count()
			if inscritos!=30:
				response.write("<tr><td>"+mat.grupo.cve_grupo+"</td><td>"+mat.materia.nombre+"</td><td>"+mat.profesor.cve_usuario.nombre+" "+mat.profesor.cve_usuario.apellidoPaterno+" "+mat.profesor.cve_usuario.apellidoMaterno+"</td>")
				if mat.horario.cve_horario==1:
					response.write("<td>7:00-8:30</td><td></td><td></td><td>7:00-8:30</td><td>8:30-10:00</td>")
				if mat.horario.cve_horario==2:
					response.write("<td></td><td>7:00-8:30</td><td>7:00-8:30</td><td></td><td>7:00-8:30</td>")
				if mat.horario.cve_horario==3:
					response.write("<td>8:30-10:30</td><td></td><td>8:30-10:30</td><td>8:30-10:30</td><td></td>")
				if mat.horario.cve_horario==4:
					response.write("<td>10:30-12:00</td><td>8:30-10:30</td><td></td><td>10:30-12:00</td><td></td>")
				if mat.horario.cve_horario==5:
					response.write("<td></td><td>10:30-12:00</td><td>10:30-12:00</td><td></td><td>10:30-12:00</td>")
				if mat.horario.cve_horario==6:
					response.write("<td>12:00-13:30</td><td></td><td>12:00-13:30</td><td>12:00-13:30</td><td></td>")
				if mat.horario.cve_horario==7:
					response.write("<td></td><td>12:00-13:30</td><td>13:30-15:00</td><td></td><td>12:00-13:30</td>")
				if mat.horario.cve_horario==8:
					response.write("<td>13:30-15:00</td><td>13:30-15:00</td><td></td><td>13:30-15:00</td><td></td>")
				if mat.horario.cve_horario==9:
					response.write("<td>15:00-16:30</td><td></td><td></td><td>15:00-16:30</td><td>16:30-18:00</td>")
				if mat.horario.cve_horario==10:
					response.write("<td></td><td>15:00-16:30</td><td>15:00-16:30</td><td></td><td>15:00-16:30</td>")
				if mat.horario.cve_horario==11:
					response.write("<td>16:30-18:00</td><td></td><td>16:30-18:00</td><td>16:30-18:00</td><td></td>")
				if mat.horario.cve_horario==12:
					response.write("<td>18:30-20:00</td><td>16:30-18:00</td><td></td><td>18:30-20:00</td><td></td>")
				if mat.horario.cve_horario==13:
					response.write("<td></td><td>18:30-20:00</td><td>18:30-20:00</td><td></td><td>18:30-20:00</td>")
				if mat.horario.cve_horario==14:
					response.write("<td>20:00-21:30</td><td></td><td>20:00-21:30</td><td></td><td>20:00-21:30</td>")
				response.write("<td>"+str(mat.cupo-inscritos)+"</td><td><img src='../static/img/add.gif' onClick=\"updateAct();anadir('"+mat.grupo.cve_grupo+"','"+mat.materia.cve_materia+"')\" /> Agregar</td></tr>")
	else:
		grupInfo=Grupo.objects.get(cve_grupo=clave)
		grupoInfo=MateriaImpartidaEnGrupo.objects.filter(grupo=grupInfo)
		response.write("<tr><th scope='col'>Grupo</th><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMateria&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspProfesor&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbspLunes&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbsp&nbspMartes&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbspMiercoles&nbsp</th><th scope='col'>&nbsp&nbsp&nbspJueves&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbspViernes&nbsp&nbsp&nbsp</th><th>Cupo</th><th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th></tr></thead><tbody>")
		for mat in grupoInfo:
			inscritos=AlumnoTomaClaseEnGrupo.objects.filter(materia_grupo=mat).count()
			response.write("<tr><td>"+mat.grupo.cve_grupo+"</td><td>"+mat.materia.nombre+"</td><td>"+mat.profesor.cve_usuario.nombre+" "+mat.profesor.cve_usuario.apellidoPaterno+" "+mat.profesor.cve_usuario.apellidoMaterno+"</td>")
			if mat.horario.cve_horario==1:
				response.write("<td>7:00-8:30</td><td></td><td></td><td>7:00-8:30</td><td>8:30-10:00</td>")
			if mat.horario.cve_horario==2:
				response.write("<td></td><td>7:00-8:30</td><td>7:00-8:30</td><td></td><td>7:00-8:30</td>")
			if mat.horario.cve_horario==3:
				response.write("<td>8:30-10:30</td><td></td><td>8:30-10:30</td><td>8:30-10:30</td><td></td>")
			if mat.horario.cve_horario==4:
				response.write("<td>10:30-12:00</td><td>8:30-10:30</td><td></td><td>10:30-12:00</td><td></td>")
			if mat.horario.cve_horario==5:
				response.write("<td></td><td>10:30-12:00</td><td>10:30-12:00</td><td></td><td>10:30-12:00</td>")
			if mat.horario.cve_horario==6:
				response.write("<td>12:00-13:30</td><td></td><td>12:00-13:30</td><td>12:00-13:30</td><td></td>")
			if mat.horario.cve_horario==7:
				response.write("<td></td><td>12:00-13:30</td><td>13:30-15:00</td><td></td><td>12:00-13:30</td>")
			if mat.horario.cve_horario==8:
				response.write("<td>13:30-15:00</td><td>13:30-15:00</td><td></td><td>13:30-15:00</td><td></td>")
			if mat.horario.cve_horario==9:
				response.write("<td>15:00-16:30</td><td></td><td></td><td>15:00-16:30</td><td>16:30-18:00</td>")
			if mat.horario.cve_horario==10:
				response.write("<td></td><td>15:00-16:30</td><td>15:00-16:30</td><td></td><td>15:00-16:30</td>")
			if mat.horario.cve_horario==11:
				response.write("<td>16:30-18:00</td><td></td><td>16:30-18:00</td><td>16:30-18:00</td><td></td>")
			if mat.horario.cve_horario==12:
				response.write("<td>18:30-20:00</td><td>16:30-18:00</td><td></td><td>18:30-20:00</td><td></td>")
			if mat.horario.cve_horario==13:
				response.write("<td></td><td>18:30-20:00</td><td>18:30-20:00</td><td></td><td>18:30-20:00</td>")
			if mat.horario.cve_horario==14:
				response.write("<td>20:00-21:30</td><td></td><td>20:00-21:30</td><td></td><td>20:00-21:30</td>")
			response.write("<td>"+str(mat.cupo-inscritos)+"</td><td><img src='../static/img/add.gif' onClick=\"updateAct();anadir('"+mat.grupo.cve_grupo+"','"+mat.materia.cve_materia+"')\" /> Agregar</td></tr>")
	response.write("</tbody></table>")
	if request.is_ajax():
		return response
def insertData(request):
	bol=request.GET['bol']
	grupo=request.GET['grupo']
	materia=request.GET['materia']
	response=HttpResponse()
	grupInfo=Grupo.objects.get(cve_grupo=grupo)
	matInfo=Materia.objects.get(cve_materia=materia)
	materInfo=MateriaImpartidaEnGrupo.objects.get(grupo=grupInfo,materia=matInfo)
	materiaInfo=MateriaImpartidaEnGrupo.objects.filter(materia=matInfo).all()
	if materInfo.cupo==0:
		response.write("No hay cupo disponible para "+ materInfo.materia.nombre+" en el grupo "+materInfo.grupo.cve_grupo+"")
		return response
	al=Usuario.objects.get(clave=bol)
	alu=Alumno.objects.get(cve_usuario=al)
	inscrito=AlumnoTomaClaseEnGrupo.objects.filter(alumno=alu)
	materias=AlumnoTomaClaseEnGrupo.objects.filter(alumno=alu)
	try:
		pinsc=AlumnoTomaClaseEnGrupo.objects.get(alumno=alu,materia_grupo=materInfo)
	except:
		p=AlumnoTomaClaseEnGrupo(alumno=alu,materia_grupo=materInfo,calificacion=0,calificacionExtra=0)
		try:
			repeat=AlumnoTomaClaseEnGrupo.objects.get(materia_grupo__horario=p.materia_grupo.horario,alumno=alu)
		except:
			try:
				repeat_materia=AlumnoTomaClaseEnGrupo.objects.get(alumno=alu,materia_grupo__materia=matInfo)
			except:
				p.save()
				request.session['cred']=request.session['cred']+matInfo.creditos
				response.write("La materia "+p.materia_grupo.materia.nombre+" se ha agregado correctamente")
				if request.is_ajax():
					return response
			response.write("Ya has inscrito la materia "+repeat_materia.materia_grupo.materia.nombre+" en el grupo "+repeat_materia.materia_grupo.grupo.cve_grupo);
			return response
		response.write("La materia "+matInfo.nombre+" se traslapa con "+repeat.materia_grupo.materia.nombre+"  que ya inscribiste en el grupo "+repeat.materia_grupo.grupo.cve_grupo+"");
		return response
	response.write("Ya has inscrito "+pinsc.materia_grupo.materia.nombre+" en el grupo "+pinsc.materia_grupo.grupo.cve_grupo+"")
	if request.is_ajax():
			return response
def delData(request):
	bol=request.GET['bol']
	grupo=request.GET['grupo']
	materia=request.GET['materia']
	response=HttpResponse()
	grupInfo=Grupo.objects.get(cve_grupo=grupo)
	matInfo=Materia.objects.get(cve_materia=materia)
	request.session['cred']=request.session['cred']-matInfo.creditos
	materInfo=MateriaImpartidaEnGrupo.objects.get(grupo=grupInfo,materia=matInfo)
	materiaInfo=MateriaImpartidaEnGrupo.objects.filter(materia=matInfo).all()
	al=Usuario.objects.get(clave=bol)
	alu=Alumno.objects.get(cve_usuario=al)
	materias=AlumnoTomaClaseEnGrupo.objects.filter(alumno=alu)
	p=AlumnoTomaClaseEnGrupo.objects.get(alumno=alu,materia_grupo=materInfo)
	p.delete()
	if request.is_ajax():
		return response

def delallData(request):
	bol=request.GET['bol']
	request.session['cred']=0
	response=HttpResponse()
	al=Usuario.objects.get(clave=bol)
	alu=Alumno.objects.get(cve_usuario=al)
	p=AlumnoTomaClaseEnGrupo.objects.filter(alumno=alu)
	response.write("<table id='hor-minimalist-a'><thead>")
	response.write("<tr><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMateria&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>Grupo</th><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspProfesor&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbspLunes&nbsp&nbsp</th><th scope='col'>&nbsp&nbspMartes&nbsp&nbsp</th><th scope='col'>&nbspMiercoles&nbsp</th><th scope='col'>&nbsp&nbspJueves&nbsp&nbsp</th><th scope='col'>&nbsp&nbspViernes&nbsp&nbsp</th></tr></thead><tbody></tbody></table>")
	for inscrito in p:
		inscrito.delete()
	if request.is_ajax():
		return response
def updateAct(request):
	bol=request.GET['bol']
	time.sleep(.1)
	response=HttpResponse()
	al=Usuario.objects.get(clave=bol)
	alu=Alumno.objects.get(cve_usuario=al)
	materias=AlumnoTomaClaseEnGrupo.objects.filter(alumno=alu)
	response.write("<table id='hor-minimalist-a'><thead>")
	response.write("<tr><th scope='col'>Grupo</th><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMateria&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspProfesor&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbspLunes&nbsp&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbsp&nbspMartes&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbspMiercoles&nbsp</th><th scope='col'>&nbsp&nbsp&nbspJueves&nbsp&nbsp&nbsp&nbsp</th><th scope='col'>&nbsp&nbsp&nbspViernes&nbsp&nbsp&nbsp</th><th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th></tr></thead><tbody>")
	for mat in materias:
		response.write("<tr><td>"+mat.materia_grupo.grupo.cve_grupo+"</td><td>"+mat.materia_grupo.materia.nombre+"</td><td>"+mat.materia_grupo.profesor.cve_usuario.nombre+" "+mat.materia_grupo.profesor.cve_usuario.apellidoPaterno+" "+mat.materia_grupo.profesor.cve_usuario.apellidoMaterno+"</td>")
		if mat.materia_grupo.horario.cve_horario==1:
			response.write("<td>7:00-8:30</td><td></td><td></td><td>7:00-8:30</td><td>8:30-10:00</td>")
		if mat.materia_grupo.horario.cve_horario==2:
			response.write("<td></td><td>7:00-8:30</td><td>7:00-8:30</td><td></td><td>7:00-8:30</td>")
		if mat.materia_grupo.horario.cve_horario==3:
			response.write("<td>8:30-10:30</td><td></td><td>8:30-10:30</td><td>8:30-10:30</td><td></td>")
		if mat.materia_grupo.horario.cve_horario==4:
			response.write("<td>10:30-12:00</td><td>8:30-10:30</td><td></td><td>10:30-12:00</td><td></td>")
		if mat.materia_grupo.horario.cve_horario==5:
			response.write("<td></td><td>10:30-12:00</td><td>10:30-12:00</td><td></td><td>10:30-12:00</td>")
		if mat.materia_grupo.horario.cve_horario==6:
			response.write("<td>12:00-13:30</td><td></td><td>12:00-13:30</td><td>12:00-13:30</td><td></td>")
		if mat.materia_grupo.horario.cve_horario==7:
			response.write("<td></td><td>12:00-13:30</td><td>13:30-15:00</td><td></td><td>12:00-13:30</td>")
		if mat.materia_grupo.horario.cve_horario==8:
			response.write("<td>13:30-15:00</td><td>13:30-15:00</td><td></td><td>13:30-15:00</td><td></td>")
		if mat.materia_grupo.horario.cve_horario==9:
			response.write("<td>15:00-16:30</td><td></td><td></td><td>15:00-16:30</td><td>16:30-18:00</td>")
		if mat.materia_grupo.horario.cve_horario==10:
			response.write("<td></td><td>15:00-16:30</td><td>15:00-16:30</td><td></td><td>15:00-16:30</td>")
		if mat.materia_grupo.horario.cve_horario==11:
			response.write("<td>16:30-18:00</td><td></td><td>16:30-18:00</td><td>16:30-18:00</td><td></td>")
		if mat.materia_grupo.horario.cve_horario==12:
			response.write("<td>18:30-20:00</td><td>16:30-18:00</td><td></td><td>18:30-20:00</td><td></td>")
		if mat.materia_grupo.horario.cve_horario==13:
			response.write("<td></td><td>18:30-20:00</td><td>18:30-20:00</td><td></td><td>18:30-20:00</td>")
		if mat.materia_grupo.horario.cve_horario==14:
				response.write("<td>20:00-21:30</td><td></td><td>20:00-21:30</td><td></td><td>20:00-21:30</td>")
		response.write("<td><img src='../static/img/delete.gif' onClick=\"updateAct();eliminar('"+mat.materia_grupo.grupo.cve_grupo+"','"+mat.materia_grupo.materia.cve_materia+"')\"/> Eliminar</td></tr>")
	response.write("</table><label style='position: fixed; bottom: 150px; right: 0px'>Creditos:<br> Usados: "+str(request.session['cred'])+"<br>Displonibles: "+str(60-request.session['cred'])+"</label>")
	if request.is_ajax():
		return response
def addAll(request):
	bol=request.GET['bol']
	grupo=request.GET['grup']
	response=HttpResponse()
	grupInfo=Grupo.objects.get(cve_grupo=grupo)
	materInfo=MateriaImpartidaEnGrupo.objects.filter(grupo=grupInfo)
	al=Usuario.objects.get(clave=bol)
	alu=Alumno.objects.get(cve_usuario=al)
	for materia in materInfo:
		if materia.cupo==0:
			response.write("No hay cupo disponible para " +materia.materia.nombre+".<br>")
		else:
			request.session['cred']=request.session['cred']+materia.materia.creditos
			p=AlumnoTomaClaseEnGrupo(alumno=alu,materia_grupo=materia,calificacion=0,calificacionExtra=0)
			try:
				p.save()
			except:
				response.write("Ya has inscrito la materia "+materia.materia.nombre+" en el grupo "+grupo+"<br>")
	if request.is_ajax():
		response.write("El grupo "+grupo+" se ha agregado correctamente a tu horario")
		return response
#
def final(request):
	bol=request.GET['bol']
	creditos=request.session['cred']
	response=HttpResponse()
	alu=Alumno.objects.get(cve_usuario__clave=bol)
	if alu.tipo=='Regular':
		maxcred=60
	else:
		maxcred=30
	if creditos>maxcred:
		response.write("Has excedido los creditos permitidos")
	if creditos<15:
		response.write("No has inscrito los creditos minimos necesarios")
	if creditos>15 and creditos<maxcred:
		CitaInsc.objects.filter(alumno=alu).update(inscrito=1)
		response.write("OK")
	if request.is_ajax():
		return response

def cita(request):
	bol=request.user
	alu=CitaInsc.objects.get(alumno__cve_usuario=bol)
	insc=alu.cita
	return render(request, 'Alumno/Alcita.html', locals(), context_instance=RequestContext(request))

def reporteHorario(request):
	if request.method=='POST':
		bol=request.user
		response = HttpResponse(mimetype='application/pdf')
		objects_list =AlumnoTomaClaseEnGrupo.objects.filter(alumno__cve_usuario__clave=bol) # If you are using Django
    	report = reporteDeHorario(queryset=objects_list)
    	report.generate_by(PDFGenerator, filename=response)
    	return response
		
def reporteKardex(request):
	if request.method=='POST':
		bol=request.user
		response = HttpResponse(mimetype='application/pdf')
		objects_list =kardex.objects.filter(alumno__cve_usuario__clave=bol)
    	report = reporteDeKardex(queryset=objects_list)
    	report.generate_by(PDFGenerator, filename=response)
    	return response
		
def reporteBoleta(request):
	if request.method=='POST':
		bol=request.user
		response = HttpResponse(mimetype='application/pdf')
		objects_list =kardex.objects.filter(alumno__cve_usuario__clave=bol)
    	report = reporteDeBoleta(queryset=objects_list)
    	report.generate_by(PDFGenerator, filename=response)
    	return response
		
def alumnoSolicitardocs(request):
	bol=request.user
	return render(request, 'Alumno/Alsolicitardocs.html', locals(), context_instance=RequestContext(request))
		
def reporteConstancia(request):
	bol=request.user
	if request.method=='GET':
		tipo=request.GET['tipo']
		categoria=request.GET['categoria']
		objects_list =kardex.objects.filter(alumno__cve_usuario__clave=bol)
		al=Alumno.objects.get(cve_usuario__clave=bol)
		response = HttpResponse(mimetype='application/pdf')
		if tipo=='const' and categoria=='no':
			report = reporteDeConstancia(queryset=objects_list)
		
		elif tipo=='bol' and categoria=='no':
			report= reporteDeBoleta(queryset=objects_list)
			
		elif tipo=='const' and categoria=='of':
			cont=request.GET['pass']
			acceso=authenticate(username=str(bol),password=str(cont))
			cuenta=DocSolicitado.objects.filter(tipo_doc="Constancia",alumno__cve_usuario__clave=bol)
			maximo=len(cuenta)
			print len(cuenta)
			
			if maximo==3:
				msj=5
				print "No puedes tramitar mas constancias oficiales"
				return render(request, 'Alumno/Alsolicitardocs-frame.html', locals(), context_instance=RequestContext(request))
			
			else:
				if acceso is not None:
					msj=2
					print "Contrasena correcta"
					print "Constancia oficial"
					reg=DocSolicitado(alumno=al,tipo_doc="Constancia",solicitudes_hechas=1)
					reg.save()
					controlCons=DocSolicitado.objects.filter(tipo_doc="Constancia",alumno__cve_usuario__clave=bol)
					restantesCons=3-len(controlCons)
					print restantesCons
					return render(request, 'Alumno/Alsolicitardocs-frame.html', locals(), context_instance=RequestContext(request))
			
				elif acceso is None:
					msj=1
					print "Contrasena incorrecta"
					cuenta=DocSolicitado.objects.filter(tipo_doc="Constancia",alumno__cve_usuario__clave=bol)
					return render(request, 'Alumno/Alsolicitardocs-frame.html', locals(), context_instance=RequestContext(request))
			
		elif tipo=='bol' and categoria=='of':
			cont=request.GET['pass']
			acceso=authenticate(username=str(bol),password=str(cont))
			cuenta=DocSolicitado.objects.filter(tipo_doc="Boleta",alumno__cve_usuario__clave=bol)
			maximo=len(cuenta)
			print len(cuenta)
			
			if maximo==3:
				msj=4
				print "No puedes tramitar mas boletas oficiales"
				return render(request, 'Alumno/Alsolicitardocs-frame.html', locals(), context_instance=RequestContext(request))
			
			else:
				if acceso is not None:
					msj=3
					print "Contrasena correcta"
					print "Boleta oficial"
					reg=DocSolicitado(alumno=al,tipo_doc="Boleta",solicitudes_hechas=1)
					reg.save()
					controlBol=DocSolicitado.objects.filter(tipo_doc="Boleta",alumno__cve_usuario__clave=bol)
					restantesBol=3-len(controlBol)
					print restantesBol
					return render(request, 'Alumno/Alsolicitardocs-frame.html', locals(), context_instance=RequestContext(request))
			
				elif acceso is None:
					msj=1
					print "Contrasena incorrecta"
					cuenta=DocSolicitado.objects.filter(tipo_doc="Boleta",alumno__cve_usuario__clave=bol)
					return render(request, 'Alumno/Alsolicitardocs-frame.html', locals(), context_instance=RequestContext(request))
				
		else:
			return HttpResponseRedirect('../solicitardocsframe/')
		report.generate_by(PDFGenerator, filename=response)
		return response
	
def solicitardocsframe(request):
	bol=request.user
	return render(request,'Alumno/Alsolicitardocs-frame.html',locals(), context_instance=RequestContext(request))
		
def reporteETS(request):
	if request.method=='POST':
		bol=request.user
		response = HttpResponse(mimetype='application/pdf')
		objects_list =AlumnoTomaEts.objects.filter(alumno__cve_usuario__clave=bol)
    	report = reporteDeETS(queryset=objects_list)
    	report.generate_by(PDFGenerator, filename=response)
    	return response
