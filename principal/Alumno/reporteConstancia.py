# -*- encoding: utf-8 -*-
import os
RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
from geraldo import Report, landscape, ReportBand, ObjectValue, SystemField,\
            BAND_WIDTH, Label,Image,Line,ReportGroup,DetailBand
from reportlab.lib.pagesizes import A5,A4,letter
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.colors import navy, yellow, red, purple, orange,\
    green, white, blue

class reporteDeConstancia(Report):
	title = 'Instituto Politécnico Nacional'
	page_size = (letter)
	margin_left = 2*cm
	margin_top = 0.5*cm
	margin_right = 0.5*cm
	margin_bottom = 0.5*cm
    
	class band_detail(DetailBand):
            height=0.5*cm
            elements=[
                ]
    
	class band_begin(ReportBand):
            height = 1*cm
            elements = [
                Label(text='CONSTANCIA DE ESTUDIOS', top=1.5*cm,width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 9, 'alignment': TA_CENTER} ),
            ]
    
	class band_page_footer(ReportBand):
            height = 0.5*cm
            elements = [
					Label(text='Documento sin validez oficial', top=0.1*cm),
                    SystemField(expression=u'Fecha Elaboracion %(now:%Y, %b %d)s', top=0.1*cm,
						width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
					] 
    
	class band_summary(ReportBand):
			height = 1.5*cm
			elements = [
			Label(text='A QUIEN CORRESPONDA:', top=1*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='EL QUE SUSCRIBE HACE CONSTAR', top=1.8*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='QUE EL ALUMNO', top=1.8*cm, left=6.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			ObjectValue(attribute_name='alumno.cve_usuario.get_full_name'
              , top= 2.5*cm,left=7*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':11, 'alignment': TA_CENTER}),
			Label(text='CON NUMERO DE BOLETA', top=3.3*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			ObjectValue(attribute_name='alumno'
			  , top= 3.3*cm,left=3.4*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':8, 'alignment': TA_CENTER}),
			Label(text='ESTÁ INSCRITO EN ESTE PLANTEL', top=3.3*cm, left=6.9*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
		    Label(text='CURSANDO ASIGNATURAS DEL', top=3.3*cm, left=11.8*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='TERCER NIVEL, GRUPO 3CM9 DE LA', top=3.6*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='LICENCIATURA EN ING. EN SIS.', top=3.6*cm, left=6.4*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='COMPUTACIONALES COMO', top=3.6*cm, left=10.8*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='ALUMNO', top=3.6*cm, left=14.7*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='REGULAR EN EL TURNO MATUTINO', top=3.9*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='CUBRIENDO EL 49.71% DE', top=3.9*cm, left=6.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='CRÉDITOS CON UN PROMEDIO DE', top=3.9*cm, left=9.9*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='8.25.', top=3.9*cm, left=14.8*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			
			
			Label(text='OBSERVACIONES:', top=5.2*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='LA LICENCIATURA CONSTA DE 5', top=6*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='NIVELES, CON UN TOTAL DE 239.20', top=6*cm, left=5.8*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='CRÉDITOS.', top=6*cm, left=10.7*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='LA VIGENCIA ES DEL 5 DE AGOSTO', top=6.8*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='DEL 2013 AL 13 DE DICIEMBRE DE', top=6.8*cm, left=6.1*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='2013 SE EXTIENDE LA PRESENTE A', top=6.8*cm, left=10.9*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='PETICIÓN DEL INTERESADO EN LA', top=7.1*cm, left=1.2*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			Label(text='CIUDAD DE MÉXICO, D.F.,', top=7.1*cm, left=6.1*cm, style={'fontName': 'Helvetica', 'fontSize':8}),
			SystemField(expression=u'A LOS %(now: %d)s DÍAS', top=7.1*cm, left=9.7*cm, style={'fontName': 'Helvetica-Bold', 'fontSize':8}),
			SystemField(expression=u'DEL MES DE %(now: %b)s', top=7.1*cm, left=11.8*cm, style={'fontName': 'Helvetica-Bold', 'fontSize':8}),
			SystemField(expression=u'DEL %(now: %Y)s.', top=7.1*cm, left=14.2*cm, style={'fontName': 'Helvetica-Bold', 'fontSize':8}),
			
			Label(text='ATENTAMENTE', top=8.5*cm, left=7*cm, style={'fontName': 'Helvetica-Bold', 'fontSize':9, 'alignment': TA_CENTER}),
			Label(text='"LA TÉCNICA AL SERVICIO DE', top=8.8*cm, left=6*cm, style={'fontName': 'Helvetica-Bold', 'fontSize':9, 'alignment': TA_CENTER}),
			Label(text='LA PATRIA"', top=8.8*cm, left=9.4*cm, style={'fontName': 'Helvetica-Bold', 'fontSize':9, 'alignment': TA_CENTER}),
				]	  
    
	class band_page_header(ReportBand):
            height = 1.5*cm
            elements = [ Image(left=0.4*cm, top=0, width=4*cm, height=5.12*cm,
						filename= os.path.join(RUTA_PROYECTO,'../Alumno/escom.gif')),
                        SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 21, 'alignment': TA_CENTER}),
						Label(text="Escuela Superior de Cómputo", top=0.8*cm, left=0,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 16, 'alignment': TA_CENTER}),
						Label(text="SUBDIRECCIÓN DE SERVICIOS EDUCATIVOS E INTEGRACIÓN SOCIAL DEPARTAMENTO DE GESTIÓN ESCOLAR", top=2.5*cm, left=0,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 8, 'alignment': TA_CENTER}),
                        ]
