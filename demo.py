SMART PLANT CARE 
#MFC
#CAMM
#JGRA

##CENTRO DE EXCELENCIA Y APROPIACION EN IoT
#Demo AgroIndustria y medio ambiente



import time, mraa,json
#from upm import pyupm_buzzer as upmBuzzer
from ubidots import ApiClient

def ubidots_parser(json_msg):
    try:
        parsed = json.loads(json_msg) #Dict that contain the parsed json
    except: 
        print "Invalid Json Format"
        return UBIDOTS_ERROR_INVALID_JSON
    try:
        value = parsed['value']
    except:
        print "Invalid UBIDOTS message. Missing value"
        return UBIDOTS_ERROR_INVALID_FORMAT
    return (UBIDOTS_ERROR_NONE, value)


for i in range(0,5):
    try:
        print "Connecting to Ubidots"
        api = ApiClient(token='f2y6yP4gLubPvrqx2NsYh5n5gRRTm1') 
        break

    except:
        print "No internet connection, retrying..."
        time.sleep(5)

#Api_client_key ='96b2b5ca0a40f72f7fd3f303fbbf47b98eab3247'
#Api_Hum_var =['580a233f76254206cdeaa181']  
#api = ApiClient(Api_client_key)

a0 = mraa.Aio(0)
a1 = mraa.Aio(1)
# digital output - buzzer
buzPin = mraa.Gpio(8)
buzPin.dir(mraa.DIR_OUT)
buzPin.write(0)

##
while (1):


	try:
		luzdato=a1.read();
		humedato=a0.read();

		rele=api.get_variable('580a67d076254256cd395f0e')
		lastValue = rele.get_values(1) 						#Get the last value of valve from Ubidots 
		#print lastValue

		for a in lastValue: 										
			if(a['value']):								#Turn on or off the relay 
				valorActualRele=1
				buzPin.write(1)
			else:
				valorActualRele=0 
				buzPin.write(0)
       		

		#print valorActualRele
		#error, data=ubidots_parser(lastValue)
		#print data
		#Valorrele = pifacedigital.relays[0].value #Save relay state
		#print lastValue[{'value'}]
		#valorRele = relay0_control.get_values(1)
		#print valorRele['values']
		#print(luzdato)
		#api.save_collection([{'variable': '580a233f76254206cdeaa181','value':luzdato},{'variable': '580a5bcd7625421558337722','value'humedato}])
		api.save_collection([{'variable': '580a233f76254206cdeaa181','value':a1.read()}, {'variable': '580a5bcd7625421558337722','value':a0.read()}])


	#for i in Api_Hum_var:
	#my_variable = api.get_va
	except:
		print("Couldn't send data.")
		continue
