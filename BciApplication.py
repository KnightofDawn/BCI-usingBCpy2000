
import numpy
import VisionEgg
import random
import pygame
import re
import autocompletar
from autocompletar import formarFrase, iniciar

from VisionEgg.Core import *
from VisionEgg.FlowControl import Presentation
from VisionEgg.FlowControl import Controller
from VisionEgg.FlowControl import ConstantController
from VisionEgg.FlowControl import EvalStringController
from VisionEgg.Gratings import *
from VisionEgg.TCPController import *
from pygame.locals import *
from VisionEgg.Textures import *

from AppTools.Displays import fullscreen
from TryATrie import  *


	
#################################################################
#################################################################

class BciApplication(BciGenericApplication):


	
	#############################################################
	
	def Description(self):
		return "Algoritmo de prueba - Baldezzari, Lucas Matias"
		
	#############################################################
	
	def Construct(self):
		
		params = [      
						#Defino primero los parametros del Filter Module
						# "Filtering:P3TemporalFilter int EpochLength= 500ms 500ms 0 %",
						# "Filtering:P3TemporalFilter int EpochsToAverage= 1 1 0 %",
						"Filtering:Visualize int VisualizeP3TemporalFiltering= 1 1 0 1 ",
						"Filtergin:Visualize int TargetERPChannel= 1 1 0 128 ",
						#A continuación defino parametros para el Aplicattion Module
						"PythonApp:Sequencing int PreRunDuration= 3 3 0 % //Tiempo antes de comenzar corrida (seg)",
						"PythonApp:Sequencing int PostRunDuration= 1 1 0 % //(seg)",
						"PythonApp:Sequencing int PreSequenceDuration= 2 2 0s % //(seg)",
						"PythonApp:Sequencing float PostSequenceDuration= 2 2 0 % //(seg)",
						"PythonApp:Sequencing float ISIDuration= 62.5 62.5 62.5 % //Intervalo maximo entre estímulos (ms)",
						"PythonApp:Sequencing int StimulusDuration= 62.5 62.5 62.5 % //Maxima duracion de estimulo iluminado (ms)",
						"PythonApp:Sequencing int NumberOfSequences= 1 1 1 % //Cantidad de veces que se iluminaran las regiones o caracteres",
						#Declaración de estímulos
					    "PythonApp:Stimuli stringlist self.params.estimulos[0]= {A B C D E F} A B C D E F",
						"PythonApp:Stimuli stringlist self.params.estimulos[1]= {G H I J K L} G H I J K L",
						"PythonApp:Stimuli stringlist self.params.estimulos[2]= {M N O P Q R} M N O P Q R",
						"PythonApp:Stimuli stringlist self.params.estimulos[3]= {S T U V W X} S T U V W X",
						"PythonApp:Stimuli stringlist self.params.estimulos[4]= {Y Z 0 1 2 3} Y Z 0 1 2 3",
						"PythonApp:Stimuli stringlist self.params.estimulos[5]= {4 5 6 7 8 9} 4 5 6 7 8 9",
						"PythonApp:Stimuli stringlist self.params.estimulos[6]= {CH LL RR ESP . ,} CH LL RR ESP . ,",
						"PythonApp:Stimuli stringlist self.params.estimulos[7]= {QUE COMO DONDE QUIEN PORQUE CUANDO} QUE COMO DONDE QUIEN POR%QUE CUANDO",
						"PythonApp:Stimuli stringlist self.params.estimulos[8]= {SI NO CUANTO QUIENES INCOMODO MEPICA} SI CUANTO NO QUIENES INCOMODO ME%PICA",
						"PythonApp:Stimuli stringlist self.params.estimulos[9]= {BINARI1 BINARI2 BINARI3 BINARI4 BINARI5 BINARI6} % % % % % %",
						"PythonApp:Stimuli matrix estimulos= {fila1 fila2 fila3 fila4 fila5 fila6 fila7 fila8 fila9 fila10} {columna1 columna2 columna3 columna4 columna5 columna6}"
						"A B C D E F %" 
						"G H I J K L %"
						"M N O P Q R %"
						"S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 CH LL RR ESP . , QUE COMO DONDE QUIEN POR%QUE CUANDO SI CUANTO NO QUIENES INCOMODO ME%PICA BINARIO1 BINARIO2 BINARIO3 BINARIO4 BINARIO5 BINARIO6 %",
						"PythonApp:Stimuli intlist estSinArbol= {1 2 3 4 5 6 7 8 9} 1 2 3 4 5 6 7 8 9",
						"PythonApp:Stimuli intlist estConArbol= {1 2 3 4 5 6 7 8 9 10} 1 2 3 4 5 6 7 8 9 10",
						"PythonApp:Stimuli intlist estItems= {1 2 3 4 5 6} 1 2 3 4 5 6",
						"PythonApp:Stimuli stringlist items= {1 2 3 4 5 6} item1 item2 item3 item4 item5 item6 ",
						"PythonApp:Stimuli string resultadoDeletro= % % % % // resultado obtenido con el uso de la BCI",
						"PythonApp:Stimuli string palabra= % % % % //palabra obtenida por el sistema",
						"PythonApp:Stimuli stringlist keyBinarios= {BINARIO1 BINARIO2 BINARIO3 BINARIO4 BINARIO5 BINARIO6} BINARIO1 BINARIO2 BINARIO3 BINARIO4 BINARIO5 BINARIO6",
						"PythonApp:Stimuli str palabraPrevia= % % % %",
						"PythonApp:Stimuli str palabraActual= % % % %",
						"PythonApp:Stimuli strlist listaPropuesta= {0 1 2 3 4 5} palabra1 palabra2 palabra3 palabra4 palabra5 palabra6",
						"PythonApp:Stimuli intlist valoresTypeCode= {nivel1 nivel2} 0 0",
						"PythonApp:Stimuli float estimuloProbable= 0.0 0.0 0.0 0.0 //variable para almacenar datos del P3LinearFilter",
						"PythonApp:Speller int InterpretMode= 3 1 1 3 //modo del experimento 1:online free mode 2:copy mode 3:none (enumeration)",
						"PythonApp:Speller string textToSpell= % % % % //palabra para deletrear en CopyMode",
						"PythonApp:Speller int selecKey= 0 0 0 1 //Seleccionar blanco con el teclado: 0 no, 1 yes (boolean)",
						"PythonApp:Speller int selecAutomatica= 0 0 0 1 //Automatic selection for CopyMode: 0 no, 1 yes (boolean)",						
				]
				
		states = [
			"StimulusCode 16 0 0 0",  
			"StimulusType 3 0 0 17",
			# "StimulusBegin 1 0 0 0", 
			"PhaseInSequence 2 0 0 0", # 1: pre-sequence, 2: during sequence, 3: post-sequence
			"limiteEstSinArbol 9 0 1 0", #Cantidad de estimulos sin arbol binario
			"limiteEstConArbol 10 0 1 10", #Cantidad de estimulos con arbol binario 
			"limiteEstItems 6 0 1 20",
			"regionSeleccionada 10 0 2 10", #variable de estado para determinar la region seleccionada
			"SelectedTarget 6 0 2 11", #variable de estado para almacenar el caracter/palabra/frase seleecionada
			"propuestaPalabras 1 0 3 1", #si es 1 es que la región 10 contiene palabras para proponer y se debe iluminar
			"grupoActual 10 0 3 2",
			"itemActual 6 0 3 13",
			"nivelActual 2 1 3 20",
			"ultimoBlock 1 0 4 0",
			"focusOn 10 0 4 1",
			"estadoInterprete 2 1 4 12",
			"siguienteBlock 2 0 0 2",
			"StimulusTypeNivel1 4 0 0 10",
			"StimulusTypeNivel2 8 0 0 11",
			"StimulusCodeResAnterior 16 0 0 0",
			"Contador 16 0 0 0",
        ]
		
		return params,states
		
	#############################################################
	
	def Preflight(self, sigprops):
		# Here is where you would set VisionEgg.config parameters,
		# either using self.screen.setup(), or (for more advanced
		# options) directly like, e.g. this to make the window draggable:
		VisionEgg.config.VISIONEGG_FRAMELESS_WINDOW = 0# gives the window a title bar
		fullscreen(scale=0.92, id=0)
		# Reinicio la semlla de numeros aleatorios
		random.seed()
		iniciar()
		
		SamplingRate = float(((1.0/float(self.params.SamplingRate)*float(self.params.SampleBlockSize)))*1000)
		relacion_StimulusDuration = int(float(self.params.StimulusDuration)/SamplingRate)
		relacion_ISIDuration = int(float(self.params.ISIDuration)/SamplingRate)
		if float(self.params.StimulusDuration) > relacion_StimulusDuration*SamplingRate:
			self.params['StimulusDuration'] = str((SamplingRate)*relacion_StimulusDuration)
			if float(self.params['StimulusDuration']) == 0:
				self.params['StimulusDuration'] = str(SamplingRate)
			print "ADVERTENCIA: Debido a que el SamplingRate es de " + str(SamplingRate)+", la nueva duración será de StimulusDuration será de " + str(self.params['StimulusDuration'])

		if float(self.params.ISIDuration) > relacion_ISIDuration*SamplingRate:
			self.params['ISIDuration'] = str((SamplingRate)*relacion_ISIDuration)
			if float(self.params['ISIDuration']) == 0:
				self.params['ISIDuration'] = str(SamplingRate)
			print "ADVERTENCIA: Debido a que el SamplingRate es de " + str(SamplingRate)+", la nueva duración será del ISIDuration será de " + str(self.params['ISIDuration'])
			
		if self.params['InterpretMode'].val == 1:
			print "ADVERTENCIA: Ya que el modo interprete es 'online free mode', las variables selecAutomatica y selecKey se ponen en cero."
			self.params.selecAutomatica = 0
			self.params.selecKey = 0

	#############################################################
	
	def Initialize(self, indim, outdim):
		# Set up stimuli. Visual stimuli use calls to
		# self.stimulus(). Attach whatever you like as attributes
		# of self, for easy access later on. Don't overwrite existing
		# attributes, however:  using names that start with a capital
		# letter is a good insurance against this.
		# let's have a black background
		self.screen.color = (0,0,0)		
		ancho,alto = self.screen.size	
		dimensiones = (ancho,alto)
		self.states.nivelActual = 1
		
		##INICIO VARIABLES DE ESTAD0
		self.states.limiteEstConArbol = 0
		self.states.limiteEstSinArbol = 0
		self.states.regionSeleccionada = 0
		self.states.SelectedTarget = 0
		self.states.StimulusCodeResAnterior = 0
		self.states.Contador = 0
		# self.states.propuestaPalabras = 1
		# self.params.palabra = 'ca'
		# self.params.SignalSourceFilterChain
		# self.params.SignalSourceFilterChain.matrixlabels()
		# self.params.SignalSourceFilterChain[:, 'Filter Name']
		# print self.params.SignalSourceFilterChain[:, 'Filter Name']
		
		# ch_ind = map(int, self.params['SampleBlockSize'])
		# print ch_ind
		# ChannelNames = map(str, self.params['ChannelNames'])
		# print "Nombre de Canales: " 
		# print ChannelNames	
	# **************** ESTIMULOS GRUPO 1 *********************************
	# **************** ESTIMULOS GRUPO 1 *********************************

		# estimulos = self.screen.SetDefaultFont('impact', 50)
		
		estimulos = self.screen.SetDefaultFont('impact', 45)
		
		self.stimulus(self.params.estimulos[0][0], VisionEgg.Text.Text, text=self.params.estimulos[0][0],
		                                               position=(ancho*0.10,alto*0.93), #A
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[0][1], VisionEgg.Text.Text, text=self.params.estimulos[0][1],
		                                               position=(ancho*0.15,alto*1),   #B
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[0][2], VisionEgg.Text.Text, text=self.params.estimulos[0][2],
		                                               position=(ancho*0.20,alto*0.93),#C
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[0][3], VisionEgg.Text.Text, text=self.params.estimulos[0][3],
		                                               position=(ancho*0.20,alto*0.86),#D
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[0][4], VisionEgg.Text.Text, text=self.params.estimulos[0][4],
		                                               position=(ancho*0.15,alto*0.81),#E
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[0][5], VisionEgg.Text.Text, text=self.params.estimulos[0][5],
		                                               position=(ancho*0.10,alto*0.86),#F
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		
	#**************** ESTIMULOS GRUPO 2 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[1][0], VisionEgg.Text.Text, text=self.params.estimulos[1][0],
		                                               position=(ancho*0.43,alto*0.93),#G
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[1][1], VisionEgg.Text.Text, text=self.params.estimulos[1][1],
		                                               position=(ancho*0.48,alto*1),#H
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[1][2], VisionEgg.Text.Text, text=self.params.estimulos[1][2],
		                                               position=(ancho*0.53,alto*0.93),#I
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[1][3], VisionEgg.Text.Text, text=self.params.estimulos[1][3],
		                                               position=(ancho*0.53,alto*0.86),#J
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[1][4], VisionEgg.Text.Text, text=self.params.estimulos[1][4],
		                                               position=(ancho*0.48,alto*0.81),#K
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[1][5], VisionEgg.Text.Text, text=self.params.estimulos[1][5],
		                                               position=(ancho*0.43,alto*0.86),#L
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		
	#**************** ESTIMULOS GRUPO 3 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[2][0], VisionEgg.Text.Text, text=self.params.estimulos[2][0],
		                                               position=(ancho*0.76,alto*0.93),#M
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[2][1], VisionEgg.Text.Text, text=self.params.estimulos[2][1],
		                                               position=(ancho*0.81,alto*1),#N
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[2][2], VisionEgg.Text.Text, text=self.params.estimulos[2][2],
		                                               position=(ancho*0.86,alto*0.93),#O
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[2][3], VisionEgg.Text.Text, text=self.params.estimulos[2][3],
		                                               position=(ancho*0.86,alto*0.86),#P
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[2][4], VisionEgg.Text.Text, text=self.params.estimulos[2][4],
		                                               position=(ancho*0.81,alto*0.81),#Q
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[2][5], VisionEgg.Text.Text, text=self.params.estimulos[2][5],
		                                               position=(ancho*0.76,alto*0.86),#R
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
	#**************** ESTIMULOS GRUPO 4 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[3][0], VisionEgg.Text.Text, text=self.params.estimulos[3][0],
		                                               position=(ancho*0.10,alto*0.68),#S
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[3][1], VisionEgg.Text.Text, text=self.params.estimulos[3][1],
		                                               position=(ancho*0.15,alto*0.72),#T
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[3][2], VisionEgg.Text.Text, text=self.params.estimulos[3][2],
		                                               position=(ancho*0.20,alto*0.68),#U
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[3][3], VisionEgg.Text.Text, text=self.params.estimulos[3][3],
		                                               position=(ancho*0.20,alto*0.59),#V
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[3][4], VisionEgg.Text.Text, text=self.params.estimulos[3][4],
		                                               position=(ancho*0.15,alto*0.56),#W
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[3][5], VisionEgg.Text.Text, text=self.params.estimulos[3][5],
		                                               position=(ancho*0.10,alto*0.61),#X
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		
	#**************** ESTIMULOS GRUPO 5 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[4][0], VisionEgg.Text.Text, text=self.params.estimulos[4][0],
		                                               position=(ancho*0.43,alto*0.68),#Y
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[4][1], VisionEgg.Text.Text, text=self.params.estimulos[4][1],
		                                               position=(ancho*0.48,alto*0.72),#Z
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[4][2], VisionEgg.Text.Text, text=self.params.estimulos[4][2],
		                                               position=(ancho*0.53,alto*0.68),#0
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[4][3], VisionEgg.Text.Text, text=self.params.estimulos[4][3],
		                                               position=(ancho*0.53,alto*0.59),#1
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[4][4], VisionEgg.Text.Text, text=self.params.estimulos[4][4],
		                                               position=(ancho*0.48,alto*0.56),#2
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[4][5], VisionEgg.Text.Text, text=self.params.estimulos[4][5],
		                                               position=(ancho*0.43,alto*0.61),#3
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		
	#**************** ESTIMULOS GRUPO 6 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[5][0], VisionEgg.Text.Text, text=self.params.estimulos[5][0],
		                                               position=(ancho*0.76,alto*0.68),#4
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[5][1], VisionEgg.Text.Text, text=self.params.estimulos[5][1],
		                                               position=(ancho*0.81,alto*0.72),#5
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[5][2], VisionEgg.Text.Text, text=self.params.estimulos[5][2],
		                                               position=(ancho*0.86,alto*0.68),#6
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[5][3], VisionEgg.Text.Text, text=self.params.estimulos[5][3],
		                                               position=(ancho*0.86,alto*0.59),#7
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[5][4], VisionEgg.Text.Text, text=self.params.estimulos[5][4],
		                                               position=(ancho*0.81,alto*0.56),#8
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[5][5], VisionEgg.Text.Text, text=self.params.estimulos[5][5],
		                                               position=(ancho*0.76,alto*0.61),#9
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.color = numpy.array([0.5, 0.5,0.5])
		
	#**************** ESTIMULOS GRUPO 7 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[6][0], VisionEgg.Text.Text, text=self.params.estimulos[6][0],
		                                               position=(ancho*0.10,alto*0.40),#CH
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[6][1], VisionEgg.Text.Text, text=self.params.estimulos[6][1],
		                                               position=(ancho*0.15,alto*0.47),#LL
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[6][2], VisionEgg.Text.Text, text=self.params.estimulos[6][2],
		                                               position=(ancho*0.20,alto*0.40),#RR
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[6][3], VisionEgg.Text.Text, text=self.params.estimulos[6][3],
		                                               position=(ancho*0.20,alto*0.33),#' ' 
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[6][4], VisionEgg.Text.Text, text=self.params.estimulos[6][4],
		                                               position=(ancho*0.15,alto*0.27),#.
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[6][5], VisionEgg.Text.Text, text=self.params.estimulos[6][5],
		                                               position=(ancho*0.10,alto*0.33),#,
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
													   
	#**************** ESTIMULOS GRUPO 8 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[7][0], VisionEgg.Text.Text, text= 'QUE',
		                                               position=(ancho*0.41,alto*0.40),#QUE
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[7][1], VisionEgg.Text.Text, text= 'COMO',
		                                               position=(ancho*0.48,alto*0.47),#COMO
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[7][2], VisionEgg.Text.Text, text= 'DONDE',
		                                               position=(ancho*0.55,alto*0.40),#DONDE
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[7][3], VisionEgg.Text.Text, text= 'QUIEN',
		                                               position=(ancho*0.55,alto*0.33),#QUIEN
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[7][4], VisionEgg.Text.Text, text= 'POR QUE',
		                                               position=(ancho*0.48,alto*0.27),#POR QUE
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[7][5], VisionEgg.Text.Text, text= 'CUANDO',
		                                               position=(ancho*0.41,alto*0.33),#CUANDO
		                                               anchor='top',
													   color = (0.3,0.3,0.3))

	#**************** ESTIMULOS GRUPO 9 *********************************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[8][0], VisionEgg.Text.Text, text= 'SI',
		                                               position=(ancho*0.76,alto*0.40),#SI
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[8][1], VisionEgg.Text.Text, text= 'NO',
		                                               position=(ancho*0.81,alto*0.47),#NO
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[8][2], VisionEgg.Text.Text, text= 'CUANTO',
		                                               position=(ancho*0.86,alto*0.40),#CUANTO
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[8][3], VisionEgg.Text.Text, text= 'QUIENES',
		                                               position=(ancho*0.90,alto*0.33),#QUIENES
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[8][4], VisionEgg.Text.Text, text= 'INCOMOD@',
		                                               position=(ancho*0.81,alto*0.25),#INCOMOD@
		                                               anchor='top',
													   color = (0.3,0.3,0.3))
		self.stimulus(self.params.estimulos[8][5], VisionEgg.Text.Text, text= 'ME PICA' ,
		                                               position=(ancho*0.72,alto*0.33),#ME PICA
		                                               anchor='top',
													   color = (0.3,0.3,0.3))

	#****** ESTIMULOS CORRESPONDIENTES A LOS OBTENIDOS POR EL ARBOL BINARIO******************
		estimulos = self.screen.SetDefaultFont('impact', 45)
		self.stimulus(self.params.estimulos[9][0], VisionEgg.Text.Text, text= 'YO',
		                                               position=(ancho*0.1,alto*0.15),
		                                               anchor='top',
													   color = (0.3,0.3,0.3),
													   on = True)
		self.stimulus(self.params.estimulos[9][1], VisionEgg.Text.Text, text= 'TU',
		                                               position=(ancho*0.25,alto*0.15),
		                                               anchor='top',
													   color = (0.3,0.3,0.3),
													   on = True)
		self.stimulus(self.params.estimulos[9][2], VisionEgg.Text.Text, text= 'EL',
		                                               position=(ancho*0.40,alto*0.15),
		                                               anchor='top',
													   color = (0.3,0.3,0.3),
													   on = True)
		self.stimulus(self.params.estimulos[9][3], VisionEgg.Text.Text, text= 'ELLA',
		                                               position=(ancho*0.55,alto*0.15),
		                                               anchor='top',
													   color = (0.3,0.3,0.3),
													   on = True)
		self.stimulus(self.params.estimulos[9][4], VisionEgg.Text.Text, text= 'NOSOTROS',
		                                               position=(ancho*0.70,alto*0.15),
		                                               anchor='top',
													   color = (0.3,0.3,0.3),
													   on = True)
		self.stimulus(self.params.estimulos[9][5], VisionEgg.Text.Text, text= 'ELLOS',
		                                               position=(ancho*0.85,alto*0.15),
		                                               anchor='top',
													   color = (0.3,0.3,0.3),
													   on = True)
		
		#***** ESTIMULOS QUE SERÁN USADOS LUEGO DE SELECCIONADA UNA REGIÓN **************
		self.stimulus(self.params['items'][0],VisionEgg.Text.Text, text = '',
														color = (0.3,0.3,0.3),
														position = (ancho*0.16,alto*0.9),
														anchor = 'top',
														font_size = 90,
														on = False)
		self.stimulus(self.params['items'][1],VisionEgg.Text.Text, text ='',
														color = (0.3,0.3,0.3),
														position = (ancho*0.493,alto*0.9),
														anchor = 'top',
														font_size = 90,
														on = False)
		self.stimulus(self.params['items'][2],VisionEgg.Text.Text, text = '',
														color = (0.3,0.3,0.3),
														position = (ancho*0.813,alto*0.9),
														anchor = 'top',
														font_size = 90,
														on = False)
		self.stimulus(self.params['items'][3],VisionEgg.Text.Text, text = '',
														color = (0.3,0.3,0.3),
														position = (ancho*0.16,alto*0.45),
														anchor = 'top',
														font_size = 90,
														on = False)
		self.stimulus(self.params['items'][4],VisionEgg.Text.Text, text = '',
														color = (0.3,0.3,0.3),
														position = (ancho*0.493,alto*0.45),
														anchor = 'top',
														font_size = 90,
														on = False)
		self.stimulus(self.params['items'][5],VisionEgg.Text.Text, text = '',
														color = (0.3,0.3,0.3),
														position = (ancho*0.813,alto*0.45),
														anchor = 'top',
														font_size = 90,
														on = False)

																													
		# ***** OBJETOS DEL TIPO TEXT Y RECTANGULO PARA LA FASE PRE RUN *****************											   
		##Genero un RectanguloInicio que contendra el mensaje PreRun o pre inicio
		self.stimulus('RectanguloInicio',VisionEgg.MoreStimuli.Target2D,position=(ancho*0.5,alto*0.5), 
														color = (1.0,1.0,1.0),
														size = (ancho*0.5,alto*0.3))
		self.stimulus('TextoInicio', VisionEgg.Text.Text, text = 'Para iniciar, click en START',
														position = (ancho*0.5,alto*0.55),
														color = (0.0,0.0,0.0),
														anchor = 'top')
		self.screen.SetDefaultFont('impact', 100)
		self.stimulus('PreRunDuration', VisionEgg.Text.Text, text = str(self.params.PreRunDuration),
														position = (ancho*0.5,alto*0.55),
														color = (1.0,1.0,1.0),
														anchor = 'top',
														on = False)
		self.screen.SetDefaultFont('impact', 150)
		self.stimulus('finSesion', VisionEgg.Text.Text, text = 'Final del JUEGO',
														position = (ancho*0.5,alto*0.55),
														color = (1.0,0.0,0.0),
														anchor = 'top',
														on = False)
														
		#Genero el texto donde se mostrara el texto a enfocar para COPYMODE
		self.screen.SetDefaultFont('impact', 50)
		self.stimulus('textoFocusOn',VisionEgg.Text.Text, text = 'Por favor, enfocarse en: ',
														position = (ancho*0.5,alto*0.55),
														color = (1.0,1.0,1.0),
														anchor = 'top',
														on = False)
		self.stimulus('focusOn',VisionEgg.Text.Text, text = '',
														position = (ancho*0.5,alto*0.45),
														color = (1.0,1.0,1.0),
														anchor = 'top',
														font_size = 40,
														on = False)
														
		#************ Rectangulo donde se muestran las palabras deletreadas **************************************
		self.stimulus('zonaDeletreo', VisionEgg.MoreStimuli.Target2D,position = (0,0), #Recuadro donde se muestran las letras/palabras deletreadas
														color = (1.0,1.0,1.0),
														size = (ancho*2,alto*0.1),
														on = True)
		self.screen.SetDefaultFont('impact', 20)
		self.stimulus('resultado', VisionEgg.Text.Text, text = 'Resultado: ',
														position = (ancho*0.01,alto*0.01),
														color = (1.0,0.0,0.0),
														on = True)
		self.stimulus('resultadoDeletro', VisionEgg.Text.Text, text = '',
														position = (ancho*0.068,alto*0.01),
														color = (0.0,0.0,0.0),
														font_size = 20,
														on = True)
		for i in range(6):
			self.params.listaPropuesta[i] = (self.stimuli[self.params['estimulos'][9][i]].text)
		# filename = os.path.join('E:\Documentos\Facultad\BCI2000\BCI2000\python',"imagenes","Plancha.jpg")												
		# texture = Texture(filename)
		# self.stimulus('Imagen',VisionEgg.Textures.TextureStimulus,texture=texture, shrink_texture_ok=1,
                    # anchor='center',
                    # position=(ancho*0.9,alto*0.6),
					# on = True,
					# size = (250,250)
                    # )
		
	#############################################################
	
	def StartRun(self):
		self.params.NumberOfSequences = int(self.params.NumberOfSequences)
		if int(self.params.InterpretMode) == 1 or int(self.params.InterpretMode) == 3:
			# self.params.BlocksPerRun = int(self.params.BlocksPerRun) * 2 + 1
			self.params.BlocksPerRun = 3
		if int(self.params.InterpretMode ) == 2:
			# self.params.BlocksPerRun = int(len(self.params.textToSpell))*2+1
			self.params.BlocksPerRun = 3
		self.states.focusOn = 0
		self.states.siguienteBlock = 1
		self.stimuli['resultadoDeletro'].text = ''
		# pass
		
	#############################################################
	
	def Phases(self):

		self.phase(name='PreRun', next='PreRunDurationInicial', duration = float(self.params['StimulusDuration'])*2, id = 1)
		self.phase(name='PreRunDurationInicial', next = 'Descuento', duration = 1000, id = 2)
		self.phase(name='Descuento', next = 'PreRunDurationInicial' if self.params.PreRunDuration > 1 
											else 'Limpiar', duration = float(self.params['StimulusDuration'])*2, id = 3)
		self.phase(name='Limpiar', next = 'ActualizarPantalla', duration = float(self.params['StimulusDuration'])*2, id = 4)
		
		self.phase(name='on', duration= float(self.params['StimulusDuration']), next='interTrial', id = 5)
		self.phase(name='off', duration= float(self.params['ISIDuration']), next='on', id = 6)
		
		self.phase(name='InterBlock', next = 'procesarFrase', duration = int(self.params.PostSequenceDuration)*1000 if int(self.params.PostSequenceDuration)*1000 > 0
																									else  1000, id = 7)
		self.phase(name='procesarFrase', next = 'ActualizarPantalla', duration = float(self.params['StimulusDuration'])*2, id = 8)
		self.phase(name='ActualizarPantalla', next = 'mostrarPantalla', duration = 3000, id = 9)#el tiempo entre una nueva presentación, esta dado por el timing de ésta fase
		self.phase(name = 'interTrial', duration = 31.25, next = 'off',id = 12)
		self.phase(name='mostrarPantalla', next = 'on', duration = 31.25*100, id = 10)
		self.phase(name='finalSesion', next = 'finalSesion', duration = float(self.params['StimulusDuration']), id = 11)
		self.design(start = 'PreRun', new_trial ='on', interblock = 'InterBlock', end = 'finalSesion')

		
	#############################################################

	def Transition(self, phase):
	
		if self.states.propuestaPalabras == 0 and self.states.nivelActual == 1:
			self.params.TrialsPerBlock = int(self.params.NumberOfSequences)*10 
		elif self.states.nivelActual == 2:
			self.params.TrialsPerBlock = int(self.params.NumberOfSequences) *6 #aca debo iluminar 6 estímulos
		if self.states.ultimoBlock == 1:
			self.params.TrialsPerBlock = -1
		# present stimuli and update states to record what is going on
		
		if (phase == 'PreRun'):
			self.stimuli['TextoInicio'].on = False
			self.stimuli['PreRunDuration'].on = True
			self.params.PreRunDuration = int(self.params.PreRunDuration)
		
		elif phase == 'PreRunDurationInicial':
			self.stimuli['PreRunDuration'].text = str(self.params.PreRunDuration)
		
		elif phase == 'Descuento':
			self.params.PreRunDuration = self.params.PreRunDuration - 1
				
		elif phase == 'Limpiar':
			self.states.PhaseInSequence = 1
			self.stimuli['RectanguloInicio'].color = (1.0,1.0,1.0)
			self.stimuli['RectanguloInicio'].on = False
			self.stimuli['PreRunDuration'].on = False
			random.shuffle(self.params.estSinArbol)
			random.shuffle(self.params.estConArbol)
			random.shuffle(self.params.estItems)				

		elif phase == 'InterBlock':
			if  int(self.params.InterpretMode) == 1 or int(self.params.InterpretMode) == 3:
				if self.states.CurrentBlock == self.params.BlocksPerRun - 1:
					if self.states.regionSeleccionada == 0:
						self.states.CurrentBlock = 1
					if self.states.regionSeleccionada != 0:
						self.states.CurrentBlock = 2
				if self.states.CurrentBlock == self.params.BlocksPerRun:
					if self.states.SelectedTarget == 0:
						self.states.CurrentBlock = 2
					if self.states.SelectedTarget != 0:
						self.states.CurrentBlock = 1					

			if int(self.params.InterpretMode) == 2:
				if self.states.CurrentBlock == self.params.BlocksPerRun - 1:
					if self.states.regionSeleccionada == 0:
						self.states.CurrentBlock = 1
					if self.states.regionSeleccionada != 0:
						self.states.CurrentBlock = 2
				if self.states.CurrentBlock == self.params.BlocksPerRun:
					if self.states.SelectedTarget == 0:
						self.states.CurrentBlock = 2
					elif self.states.SelectedTarget != 0 and self.states.focusOn < len(self.params.textToSpell):
						self.states.siguienteBlock = 1
						self.states.CurrentBlock = 1
					elif self.states.SelectedTarget != 0 and self.states.focusOn == len(self.params.textToSpell):
						self.states.ultimoBlock = 1
		
		elif phase == 'procesarFrase':
			if self.states.SelectedTarget != 0:
				self.params.palabraActual = self.stimuli[self.params.estimulos[self.states.regionSeleccionada - 1][self.states.SelectedTarget - 1]].text
		
				resultado = formarFrase(self.params.palabraActual, self.stimuli['resultadoDeletro'].text, self.states.regionSeleccionada, self.params.listaPropuesta)	
				self.stimuli['resultadoDeletro'].text = resultado[0]
				for i in range(6):
					self.stimuli[self.params.estimulos[9][i]].text = resultado[1][i].upper()
					self.params.listaPropuesta[i] = resultado[1][i]
				self.states.PhaseInSequence = 3
			else:
				pass
				
		elif phase == 'ActualizarPantalla':
			# if self.states.PhaseInSequence == 1:
				# self.states.PhaseInSequence = 2
			# if self.states.PhaseInSequence == 3:
				# self.states.PhaseInSequence = 1
			if self.states.nivelActual == 1 and self.states.regionSeleccionada != 0:
				self.states.nivelActual = 2
				# self.params.estimuloProbable = 0.0
			elif self.states.nivelActual == 2 and self.states.SelectedTarget != 0:
				self.states.nivelActual = 1
				# self.params.estimuloProbable = 0.0
				
			if self.states.nivelActual == 2:
				for j in range(10):
					for i in range(6):
						self.stimuli[self.params.estimulos[j][i]].on = False
				for i in range(6):
					if self.states.regionSeleccionada < 10:
						self.stimuli[self.params['items'][i]].text = self.params.estimulos[self.states.regionSeleccionada - 1][i]
					elif self.states.regionSeleccionada == 10:
						self.stimuli[self.params['items'][i]].text = self.stimuli[self.params['estimulos'][9][i]].text 
				for i in range(6):
					self.stimuli[self.params['items'][i]].on = True	
				self.params.estimuloProbable = 0.0
					
			if self.states.nivelActual == 1: #and self.states.SelectedTarget != 0: #Aca hemos seleccionado un blanco/letra/palabra/frase y debo volver al inicio
				for i in range(6):
					self.stimuli[self.params['items'][i]].on = False
				for j in range(9):
					for i in range(6):
						self.stimuli[self.params.estimulos[j][i]].on = True

				for i in range(6):
					self.stimuli[self.params.estimulos[9][i]].on = True
					
				if int(self.params.InterpretMode) == 2 and self.states.focusOn < len(self.params.textToSpell):
					if self.states.focusOn < len(self.params.textToSpell):
						self.stimuli['RectanguloInicio'].color = (1.0,1.0,1.0)
						self.stimuli['RectanguloInicio'].on = True
						self.stimuli['textoFocusOn'].on = True
						self.stimuli['focusOn'].text = str(self.params.textToSpell[self.states.focusOn])
						self.stimuli['focusOn'].on = True
						for i in range(9):
							for j in range(6):
								if self.params.textToSpell[self.states.focusOn] == self.params.estimulos[i][j]:
									self.states.StimulusTypeNivel1 = i + 1
									self.states.StimulusTypeNivel2 = (i+1)*10 + j + 1
						self.states.focusOn = self.states.focusOn + 1
						self.states.siguienteBlock = 0
				self.states.regionSeleccionada = 0
				self.states.SelectedTarget = 0
				self.params.estimuloProbable = 0.0

				
		elif phase == 'mostrarPantalla':
			if self.states.PhaseInSequence == 3:
				self.states.PhaseInSequence = 1
			if int(self.params.InterpretMode) == 2:
				self.stimuli['RectanguloInicio'].on = False
				self.stimuli['textoFocusOn'].on = False
				self.stimuli['focusOn'].on = False
			else: 
				pass
			
######************** FASE 'on' ******************************************************************************************************************************************** 
		elif phase == 'on':
			if self.states.PhaseInSequence == 1:
				self.states.PhaseInSequence = 2
			if self.states.nivelActual == 1:

				if self.states['limiteEstConArbol'] <= 10:
					self.states['grupoActual']= int(self.params.estConArbol[self.states['limiteEstConArbol']])
					# self.states['StimulusBegin'] = 1
					self.states['StimulusCode'] = self.states['grupoActual']#asigno un valor a StimulusCode para que el P3SignalProcessing sepa el estímulo o blanco (target) actual
					for i in range(6):
						self.stimuli[self.params.estimulos[self.states['grupoActual'] - 1][i]].color = (1.0, 1.0, 1.0)
						
					if self.params['InterpretMode'].val == 2 and self.states['StimulusCode'] == self.states.StimulusTypeNivel1:
						self.states['StimulusType'] = 1
						
			if self.states.nivelActual == 2:
				if self.states['limiteEstItems'] <= 6:
					itemActual = str(self.states.regionSeleccionada) + str(self.params.estItems[self.states['limiteEstItems']])
					# self.states['StimulusBegin'] = 1
					self.states['StimulusCode'] = int(itemActual)
					
					if self.params['InterpretMode'].val == 2 and self.states['StimulusCode'] == self.states.StimulusTypeNivel2:
						self.states['StimulusType'] = 1
					
					self.stimuli[self.params['items'][self.params.estItems[self.states.limiteEstItems]]].color = (1.0, 1.0, 1.0)
					
					if int(self.params.InterpretMode) == 2 and str(self.params.textToSpell[self.states.focusOn-1]) == self.stimuli[self.params['items'][self.params.estItems[self.states.limiteEstItems]]].text:
						self.states.StimulusType = 1
			
					
######************** FASE 'off' ******************************************************************************************************************************************* 	
		elif phase == 'interTrial':
			# self.states['StimulusBegin'] = 0
			pass
			
		elif phase == 'off':
			# self.states['StimulusBegin'] = 0
			self.states['StimulusCode'] = 0
			self.states['StimulusType'] = 0
			if self.states.nivelActual == 1:
				for i in range(6):
					self.stimuli[self.params.estimulos[self.states['grupoActual'] - 1][i]].color = (0.3, 0.3,0.3)
				# self.states['StimulusCode'] = 0
				# self.states['StimulusType'] = 0
					
				if self.states['limiteEstConArbol'] <= 10:
					self.states['limiteEstConArbol'] = self.states['limiteEstConArbol'] + 1
					if self.states['limiteEstConArbol'] == 10:
						self.states['limiteEstConArbol'] = 0
						random.shuffle(self.params.estConArbol)
										
			if self.states.nivelActual == 2:
				# self.states['StimulusCode'] = 0
				if self.states['limiteEstItems'] <= 6:
					self.stimuli[self.params['items'][self.params.estItems[self.states.limiteEstItems]]].color = (0.3, 0.3,0.3)
					# self.states['StimulusCode'] = 0
					# self.states.StimulusType = 0
					self.states['limiteEstItems'] = self.states['limiteEstItems']  + 1
					if self.states['limiteEstItems'] == 6:
						self.states['limiteEstItems'] = 0
						random.shuffle(self.params.estItems)
			# self.states['StimulusCode'] = 0
			# self.states.StimulusType = 0

					
######************** FASE 'finalSesion **************************************************************************************************************************************** 	
		elif phase == 'finalSesion':
			# self.states.PhaseInSequence = 3
			self.stimuli['finSesion'].on = True
				
	#############################################################
	
	def Process(self, sig): #aca se entra cada vez que termina un SampleBlockSize
		if int(self.params.selecKey) == 0 and int(self.params.selecAutomatica) == 0 and self.params.InterpretMode == 3: #selección aleatoria de región y caracter (modo depuración)
			if self.in_phase('on') or self.in_phase('off'): #aca deberíamos procesar la información obtenida del P3SignalProcessing
				if self.states.regionSeleccionada == 0 and self.states.nivelActual == 1:
					self.states.regionSeleccionada = random.randrange(9)
				if self.states.SelectedTarget == 0 and self.states.nivelActual == 2:
					self.states.SelectedTarget = random.randrange(6)
					
		elif self.params['InterpretMode'].val == 1: #modo Online
			# if self.in_phase('on') or self.in_phase('off') or self.in_phase('interTrial'):
			# if self.states.StimulusCodeRes == 0:
				# self.params['estimuloProbable'] = 0.0
			if self.states.StimulusCodeRes != 0 and self.states.StimulusCodeResAnterior != self.states.StimulusCodeRes:
				self.states.Contador += 1
				print self.states.StimulusCodeRes
				print abs(self.in_signal)
				self.states.StimulusCodeResAnterior = self.states.StimulusCodeRes
				if abs(self.in_signal) > float(self.params['estimuloProbable']):
					self.params.estimuloProbable = abs(self.in_signal)
					if self.states.nivelActual == 1:
						self.states.regionSeleccionada = self.states.StimulusCodeRes
						if self.states.Contador == 10:
							self.states.Contador = 0
							self.params.estimuloProbable = 0.0
					elif self.states.nivelActual == 2:
						SelectedTarget = int(self.states.StimulusCodeRes)
						SelectedTarget = str(SelectedTarget/10.0)
						SelectedTarget = SelectedTarget.split('.')
						self.states.SelectedTarget = int(SelectedTarget[1])
						if self.states.Contador == 6:
							self.states.Contador = 0
							self.params.estimuloProbable = 0.0

					
		# elif self.params['selecAutomatica'].val == 1: #Selección automatica para modo de entrenamiento CopyMode
			# if self.states.nivelActual == 1:
				# self.states.regionSeleccionada = self.states.StimulusTypeNivel1
				
			# elif  self.states.nivelActual == 2:
				# SelectedTarget = str(self.states.StimulusTypeNivel2/10.0)
				# SelectedTarget = SelectedTarget.split('.')
				# self.states.SelectedTarget = int(SelectedTarget[1])
				
		elif self.params['InterpretMode'].val == 2:
			if self.states.StimulusCodeRes != 0 and self.states.StimulusCodeResAnterior != self.states.StimulusCodeRes:
				self.states.Contador += 1
				print self.states.StimulusCodeRes
				print abs(self.in_signal)
				self.states.StimulusCodeResAnterior = self.states.StimulusCodeRes
				if abs(self.in_signal) > float(self.params['estimuloProbable']):
					self.params.estimuloProbable = abs(self.in_signal)
					if self.states.nivelActual == 1:
						self.states.regionSeleccionada = self.states.StimulusCodeRes
						if self.states.Contador == 10:
							self.states.Contador = 0
							self.params.estimuloProbable = 0.0
					elif self.states.nivelActual == 2:
						SelectedTarget = int(self.states.StimulusCodeRes)
						SelectedTarget = str(SelectedTarget/10.0)
						SelectedTarget = SelectedTarget.split('.')
						self.states.SelectedTarget = int(SelectedTarget[1])
						if self.states.Contador == 6:
							self.states.Contador = 0
							self.params.estimuloProbable = 0.0
			
		# pass  # or not
		
	#############################################################
	
	def Frame(self, phase):
		# update stimulus parameters if they need to be animated on a frame-by-frame basis
		intensity = 0.5 + 0.5 * numpy.sin(2.0 * numpy.pi * 0.8 * self.since('run')['msec']/1000.0)
		self.stimuli['RectanguloInicio'].color = [intensity + 0.3 if intensity < 1.0 else 0.0, 0.0, 1.0]
		# pass
		
	#############################################################
	
	def Event(self, phase, event):
		# respond to pygame keyboard and mouse events
		# import pygame.locals
		# if self.phase == 'on' or self.phase == 'off':
		if self.phase != 'procesarFrase' and self.phase != 'ActualizarPantalla' and self.phase != 'InterBlock':
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					#self.states.PhaseInSequence = 3
					self.change_phase('finalSesion')
				if int(self.params.selecKey) == 1:	
					if self.states.nivelActual == 1:
						if event.key > 48 and event.key  <58:
							self.states.regionSeleccionada = (48 - event.key)*-1
						if event.key == 48:
							self.states.regionSeleccionada = 10
					if self.states.nivelActual == 2:
						if event.key > 48 and event.key  <55:
							self.states.SelectedTarget = (48 - event.key)*-1
		
	#############################################################
	
	def StopRun(self):
		pass
			
	
		