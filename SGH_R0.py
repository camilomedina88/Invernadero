"""Librerias"""
from __future__ import print_function
import sys, signal, atexit
import time, mraa,json
from ubidots import ApiClient
import pyupm_grove as grove
import pyupm_grovemoisture as upmMoisture


#from upm import pyupm_moisture as upmMoisture




"""Constantes"""
AUTO = 0
MAN = 1
"""Funciones"""
#Funcion de asignacion en modo target automatico
def asign_target_auto(api):
	#sp_luz_h_ubi = api.get_variable('5811199676254240e49e4726')
	#lastValue = sp_luz_h_ubi.get_values(1) 
	#sp_luz_h = lastValue [0]['value']
	#print ("setpoint luz HI ",sp_luz_h)

	#sp_luz_l_ubi = api.get_variable('581119a5762542406684468a')
	#lastValue = sp_luz_l_ubi.get_values(1) 
	#sp_luz_l = lastValue [0]['value']
	#print ("setpoint luz low ",sp_luz_l)


	#sp_HUMEDAD
	#sp_hum_h_ubi = api.get_variable('58127050762542774363f0ab')
	#lastValue = sp_hum_h_ubi.get_values(1) 
	#sp_hum_h = lastValue [0]['value']
	#print ("setpoint hume HI ",sp_hum_h)

	#sp_hum_l_ubi = api.get_variable('5812705c7625427797a162cf')
	#lastValue = sp_hum_l_ubi.get_values(1) 
	#sp_hum_l = lastValue [0]['value']
	#print ("setpoint hume low ",sp_hum_l)

	#sp_Temperatura
	#sp_temp_h_ubi = api.get_variable('581270b676254279a9aedd9a')
	#lastValue = sp_temp_h_ubi.get_values(1) 
	#sp_temp_h = lastValue [0]['value']
	#print ("setpoint temp HI ",sp_temp_h)

	#sp_temp_l_ubi = api.get_variable('5812749d76254215e9f86d72')
	#lastValue = sp_temp_l_ubi.get_values(1) 
	#sp_temp_l = lastValue [0]['value']
	#print ("setpoint temp low ",sp_temp_l)

	return 16, 7, 450, 116, 16, 15
	#return sp_luz_h, sp_luz_l, sp_hum_h, sp_hum_l, sp_temp_h, sp_temp_l

#Funcion de asignacion en modo target manual
def asign_target_man(api, out_hum):
	out_hum_ubi = api.get_variable('580a67d076254256cd395f0e')
	#new_value = out_hum_ubi.save_value({'value': out_hum})
	#out_hum_ubi = out_hum
	out_luz_ubi = 0			#asignacion temporal
	out_temp_ubi = 0		#asignacion temporal
	print ("output humedad :", out_hum)

#Funcion de control automatico
def ctrl_auto(luzdato, humdato, tempdato, sp_luz_h, sp_luz_l, sp_hum_h, sp_hum_l, sp_temp_h, sp_temp_l, actualLuz, actualTemp, actualHume):
	
	if (luzdato < sp_luz_l):
		out_luz = 1
	elif (luzdato > sp_luz_h):
		out_luz = 0
	else:
		out_luz=actualLuz

	if (humdato < sp_hum_l):
		out_humedad = 1
	elif (humdato > sp_hum_h):
		out_humedad = 0
	else:
		out_humedad=actualHume

	if (tempdato < sp_temp_l):
		out_temp = 0
	elif (tempdato > sp_temp_h):
		out_temp = 1
	else:
		out_temp=actualTemp
	#print "salida de control automatico luz, humedad, temperatura: ", out_luz, out_hum, out_temp

	return out_luz, out_humedad, out_temp

#Funcion de control manual
def ctrl_man(api):
	out_hum_ubi = api.get_variable('580a67d076254256cd395f0e')
	lastValue = out_hum_ubi.get_values(1) 
	out_hum = lastValue [0]['value']
	
	out_luz_ubi = api.get_variable('5812621f7625421e625289ce')
	lastValue = out_luz_ubi.get_values(1) 
	out_luz = lastValue [0]['value']
	
	out_temp_ubi = api.get_variable('58126fc67625427440101759')
	lastValue = out_temp_ubi.get_values(1) 
	out_temp = lastValue [0]['value']

	return out_luz, out_hum, out_temp
	

"""---------------------Main program-------------------"""	
#Estado inicial
current_mode = MAN
out_luzActual = 0
out_humActual = 0
out_tempActual = 0

#Inicio
#Conexion con ubidots
for i in range(0,5):
    try:
        #print "Connecting to Ubidots"
        print("Conectando a Ubidots")
        api = ApiClient(token='f2y6yP4gLubPvrqx2NsYh5n5gRRTm1') 
        break

    except:
        print ("No internet connection, retrying...")
        time.sleep(5)
#Analog Input
#a0 = mraa.Aio(0)
myMoisture = upmMoisture.GroveMoisture(0)
light = grove.GroveLight(1)
temp = grove.GroveTemp(2)
# Digital output
ValvePin = mraa.Gpio(8)
ValvePin.dir(mraa.DIR_OUT)
ValvePin.write(out_humActual)

LedsPin = mraa.Gpio(3)
LedsPin.dir(mraa.DIR_OUT)
LedsPin.write(out_luzActual)


VentiladorPin = mraa.Gpio(7)
VentiladorPin.dir(mraa.DIR_OUT)
VentiladorPin.write(out_tempActual)



while (1):
	#ACA DEBE IR LA ADQUISICION DE VARIABLES DE SENSORES Y DEL MODO TARGET DE UBIDOTS
	humedato = myMoisture.value()
	tempdato=0 #asignacion temporal
	target_mode_ubi = api.get_variable('5811165d762542316ec08081')
	lastValue = target_mode_ubi.get_values(1) 
	target_mode = lastValue [0]['value']
	luzActual=light.value()
	tempActual=temp.value()
	
	#print(tempActual)
	#target_mode = target_mode_ubi
	#DESPUES DE LA ADQUISICION SE ACTUALIZAN LAS VARIABLES DE UBIDOTS, SE PUEDE HACER TAMBIEN AL FINAL DE TODO DENTRO DEL WHILE
	#api.get_collection([{'variable': '580a67d076254256cd395f0e','value':out_hum}, {'variable': '580a5bcd7625421558337722','value':humedato}, {'variable': '580a233f76254206cdeaa181','value':luzActual},{'variable': '580be0e07625425bffac0aca','value':tempActual}])
	if target_mode != current_mode:
		if target_mode == AUTO:
			current_mode = AUTO
			#llamar funcion de asignacion en modo automatico
			sp_luz_h, sp_luz_l, sp_hum_h, sp_hum_l, sp_temp_h, sp_temp_l = asign_target_auto(api)
			out_luz, out_hum, out_temp = ctrl_auto(luzActual, humedato, tempActual, sp_luz_h, sp_luz_l, sp_hum_h, sp_hum_l, sp_temp_h, sp_temp_l, out_luzActual, out_tempActual,out_humActual)
		else:
			current_mode = MAN
			#llamar funcion de asignacion en modo manual
			asign_target_man(api, out_hum)
			out_luz, out_hum, out_temp = ctrl_man(api)
	else:
		if current_mode == AUTO:
			sp_luz_h, sp_luz_l, sp_hum_h, sp_hum_l, sp_temp_h, sp_temp_l = asign_target_auto(api)
			#llamar funcion de control en modo automatico
			out_luz, out_hum, out_temp = ctrl_auto(luzActual, humedato, tempActual, sp_luz_h, sp_luz_l, sp_hum_h, sp_hum_l, sp_temp_h, sp_temp_l, out_luzActual, out_tempActual,out_humActual)
		else:
			#llamar funcion de control en modo manual
			out_luz, out_hum, out_temp = ctrl_man(api)
		#Finalmente se escribe a las salidas fisicas

	print ("Estas son las salidas actuales humedad",humedato)
	print("salida valve ",out_hum)
	print("salida luz ",out_luz)
	print("salida temp",out_temp)


	if (out_hum==0.0):
		ValvePin.write(0)
		print ("apago valve")
	else:
		ValvePin.write(1)
		print ("prendio valve")

	if (out_luz==0.0):
		LedsPin.write(0)
		print ("apago leds")
	else:
		LedsPin.write(1)
		print ("prendio leds")

	if (out_temp==0.0):
		VentiladorPin.write(0)
		print ("apago ventilador")
	else:
		VentiladorPin.write(1)
		print ("prendio ventilador")



	#LedsPin.write(out_luz)
	#VentiladorPin.write(out_temp)


	api.save_collection([{'variable': '580a67d076254256cd395f0e','value':out_hum}, {'variable': '580a5bcd7625421558337722','value':humedato}, {'variable': '580a233f76254206cdeaa181','value':luzActual},{'variable': '580be0e07625425bffac0aca','value':tempActual}])