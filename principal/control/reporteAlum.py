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


class reporteAlumnos(Report):
    title = 'Instituto Politécnico Nacional'

    #materia_grupo.profesor.cve_usuario
    page_size = (letter)
    margin_left = 2*cm
    margin_top = 0.5*cm
    margin_right = 0.5*cm
    margin_bottom = 0.5*cm

    class band_detail(ReportBand):
        height = 0.5*cm
        bandera=True

        elements=(
            #ObjectValue(attribute_name='nombre',top=5*cm, left=0.5*cm, style={'fontName': 'Helvetica-Bold', 'fontSize':8}),
            
            
            ObjectValue(attribute_name='cve_usuario'
                , top=0*cm,left=6*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':14, 'alignment': TA_CENTER}),
				
			Label(text="Nombre: ", top=2*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),
            
			ObjectValue(attribute_name='cve_usuario.nombre'
                , top=2*cm,left=5*cm ,style={'fontName': 'Helvetica-Bold', 'fontSize':12}),				
                
			Label(text="Apellido Paterno: ", top=3*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.apellidoPaterno'
                , top=3*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),			
			
			Label(text="Apellido Materno: ", top=4*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.apellidoMaterno'
                , top=4*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),			
			
			
			Label(text="Sexo: ", top=5*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.sexo'
                , top=5*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),


			Label(text="Fecha de nacimiento: ", top=6*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.fecha_nac'
                , top=6*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="CURP: ", top=7*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.curp'
                , top=7*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="E-mail: ", top=8*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.email_personal'
                , top=8*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="Seguro médico: ", top=9*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.seguroMedico'
                , top=9*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),				
			
			
			Label(text="Número de SS: ", top=10*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.numero_ss'
                , top=10*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),
				
			Label(text="Tipo: ", top=11*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='tipo'
                , top=11*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="Teléfono: ", top=12*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='cve_usuario.Telefono_Celular'
                , top=12*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),				
			

					
			
				
            
        )

    class band_page_header(ReportBand):
        height = 1.5*cm
        elements = [ Image(left=0.4*cm, top=0, width=4*cm, height=5.12*cm,
                    filename= os.path.join(RUTA_PROYECTO,'../control/escom.gif')),


                    SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 21, 'alignment': TA_CENTER}),
                    Label(text="Escuela Superior de Cómputo", top=0.8*cm, left=0,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 16, 'alignment': TA_CENTER}),

                    SystemField(expression=u'Pagina %(page_number)d de %(page_count)d', top=0.1*cm,
                        width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                    ]
        borders = {'bottom': Line(stroke_width=5)}
    
    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='Documento sin validez oficial', top=0.1*cm),
                SystemField(expression=u'Fecha Elaboración %(now:%Y, %b %d)s', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        borders = {'top': True}

    class band_begin(ReportBand):
        height = 1*cm
        elements = [
            Label(text='Información del alumno ', top=0.5*cm,left=5.8*cm,width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14} ),
				
        ]


        #borders = {'bottom': Line(stroke_width=2)}

#*********************************************************************************************************
