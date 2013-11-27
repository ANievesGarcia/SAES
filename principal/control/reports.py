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


class reporteMateria(Report):
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
            
            
            ObjectValue(attribute_name='nombre'
                , top=0*cm,left=6*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':14, 'alignment': TA_CENTER}),
				
			Label(text="Clave de materia: ", top=2*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),
            
			ObjectValue(attribute_name='cve_materia'
                , top=2*cm,left=5*cm ,style={'fontName': 'Helvetica-Bold', 'fontSize':12}),				
                
			Label(text="Nombre de materia: ", top=3*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='nombre'
                , top=3*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),			
			
			Label(text="Creditos: ", top=4*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='creditos'
                , top=4*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),			
			
			
			Label(text="Plan de estudios: ", top=5*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='plan_estudios'
                , top=5*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),


			Label(text="Clasificacion: ", top=6*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='clasificacion'
                , top=6*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="Tipo: ", top=7*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='tipo'
                , top=7*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="Nivel: ", top=8*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='nivel'
                , top=8*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="Coordinador: ", top=9*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='coordinador'
                , top=9*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),				
			
			
			Label(text="Departamento: ", top=10*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='depto.nombre_depto'
                , top=10*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),
				
			Label(text="Materia antecedente: ", top=11*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='materia_antecedente'
                , top=11*cm,left=5*cm,style={'fontName': 'Helvetica-Bold', 'fontSize':12, 'alignment': TA_LEFT}),

			Label(text="Materia siguiente: ", top=12*cm, left=0*cm,width=BAND_WIDTH,
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12}),            
			
			ObjectValue(attribute_name='materia_siguiente'
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
            Label(text='Informacion de la materia ', top=0.5*cm,left=5.8*cm,width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14} ),
				
        ]


        #borders = {'bottom': Line(stroke_width=2)}

#*********************************************************************************************************
