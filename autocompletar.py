# -*- coding: utf-8 -*-

import autocomplete
from autocomplete import predict
import re
import string

def iniciar():
	autocomplete.load()

def formatearTexto(texto):
	largo = len(texto)
	index = texto.rfind(' ')
	if largo == index +1: #implica que el texto posee al menos un espacio al final
		return ' '.join(texto.split()) + ' '
	elif largo > index+1 and index != -1:
		return ' '.join(texto.split())
	elif index == -1:
		return texto

def cortarTexto (texto):
	texto = formatearTexto(texto)
	indexPrincipal = texto.rfind(' ')
	textoSinUltima = texto[:indexPrincipal if indexPrincipal != -1 else len(texto)]
	flag = 0
	if len(texto)-len(textoSinUltima) == 1:
		flag = 1#implica que tenemos un espacio inmediatamente despues del caracter o palabra
	else:
		flag = 2
		
	espacios = ' '
	textoLimpio = re.sub('[,¿?¡!.-]',' ',texto)#limpio el texto de caracteres especiales
	textoLimpio = espacios.join(textoLimpio.split())#saco los espacios sobrantes

	index = textoLimpio.rfind(' ')#encuentro posición del ultimo "espacio" 
	if index == -1:
		textoNuevo = textoLimpio[:index if index != -1 else len(textoLimpio)]
		primerPalabra = ''
		segundaPalabra = textoNuevo
	else:
		textoNuevo = textoLimpio[:index if index != -1 else len(textoLimpio)]
		primerPalabra = textoLimpio[index + 1 if index != -1 else 0:]
		if flag == 1:
			segundaPalabra = primerPalabra
			primerPalabra = ''
		if flag == 2:
			index2 = textoNuevo.rfind(' ')
			# segundoTexto = textoNuevo[:index2 if index2 != -1 else len(textoNuevo)]
			# print 'segundo texto: ' + segundoTexto
			segundaPalabra = textoNuevo[index2 + 1 if index2 != -1 else 0:]
			
	return textoSinUltima,segundaPalabra,primerPalabra,indexPrincipal
	
def formarFrase(caracterActual, textoDeletreado,regionSeleccionada,listaAnterior):

	listaPrediccion = []
	# print 'texto inicial: ' + textoDeletreado
	textoCortado = cortarTexto(textoDeletreado)
	textoNuevo = textoCortado[0]
	# print "texto nuevo: " + textoNuevo 
	anteUltimaPalabra = textoCortado[1]
	# print "ante ultima palabra: " +anteUltimaPalabra
	# print "texto limpo: " + textoNuevo
	# print textoCortado
	
	if textoCortado[3] == -1:
		palabraNueva = anteUltimaPalabra
	else:
		palabraNueva = textoCortado[2]

	if regionSeleccionada < 8:
		if caracterActual == 'ESP':
			palabraNueva += ' '
		else:
			palabraNueva += caracterActual
	elif regionSeleccionada == 8 or regionSeleccionada == 9 or regionSeleccionada == 10:
		palabraNueva = ' ' + caracterActual + ' '
	# elif regionSeleccionada == 10:
		# palabraNueva = caracterActual + ' '
	
	# print "palabra nueva: " + palabraNueva	
	
	if textoCortado[3] == -1:
		try:
			predicciones = predict((palabraNueva.lower()).strip(),'')
			for i in predicciones:
				listaPrediccion.append(i[0])
		except:
			predicciones = listaAnterior
	else:
		try:
			predicciones = predict((anteUltimaPalabra.lower()).strip(),(palabraNueva.lower()).strip())
			if len(predicciones) == 0:
				predicciones = predict((palabraNueva.lower()).strip(),'')
			for i in predicciones:
				listaPrediccion.append(i[0])
		except:
			predicciones = listaAnterior
			
	if len(listaPrediccion) < 6: #ahora debo asegurarme que predicciones tenga si o si 6 palabras que mostrar
		for i in range(6 - len(listaPrediccion)):
			listaPrediccion.append(listaAnterior[i])
			
	listaPrediccion = listaPrediccion[:6]

	# if textoCortado[3] == -1 and (regionSeleccionada == 8 or regionSeleccionada == 9):
		# textoNuevo = textoDeletreado + ' ' + palabraNueva + ' '
	# if textoCortado[3] == -1 and regionSeleccionada == 10:
		# textoNuevo = palabraNueva + ' '
	# else:
		# textoNuevo += ' ' + palabraNueva
	if textoCortado[3] == -1: #primer palabra
		if regionSeleccionada < 7:
			textoNuevo = palabraNueva
		if regionSeleccionada == 8 or regionSeleccionada == 9:
			textoNuevo = textoCortado[0] + palabraNueva 
		if regionSeleccionada == 10:
			textoNuevo = palabraNueva

	elif textoCortado != -1:
		if regionSeleccionada == 8 or regionSeleccionada == 9 or regionSeleccionada == 10:
			textoNuevo = textoCortado[0] + palabraNueva 
			# textoNuevo = palabraNueva
		# if regionSeleccionada == 10:
			# textoNuevo = palabraNueva
		if regionSeleccionada < 8:
			# textoNuevo += palabraNueva
			textoNuevo = textoCortado[0] + ' ' +  palabraNueva 
	return textoNuevo.upper(),listaPrediccion

# autocomplete.load()
# caracterActual = 'U'
# textoDeletreado= 'LL'
# regionSeleccionada = 2
# listaAnterior = ['yo','tu','el','nosotros','ella','ellos']
# resultado = formarFrase(caracterActual, textoDeletreado,regionSeleccionada,listaAnterior)
# print resultado