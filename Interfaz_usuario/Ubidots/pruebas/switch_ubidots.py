# https://www.youtube.com/watch?v=cFAB5uWnuZQ
# www.ubidots.com
# https://pypi.python.org/pypi/ubidots/1.6.1

# Declaracion de librerias a utilizar
import RPi.GPIO as GPIO
from ubidots import ApiClient
from time import sleep
import sys

# Excepcion para verificar si se conecto correctamente con la API de ubidots
try:
    print("Conectando a API Ubidots")
    api = ApiClient(token="A1E-kzn1qv9m8IDl8HveHrQyYKqzhEpDF3")
    variable = api.get_variable("5a4dba34c03f9774e0a8dd57")
    print("Conexion exitosa!!!")
except:
    print("FALLO LA CONEXION API")

pin=12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

while True:
    try:
    	last_value = variable.get_values(1)
    	if last_value[0].get("value") == 1:
        	GPIO.output(pin, GPIO.HIGH)
    	else:
        	GPIO.output(pin, GPIO.LOW)
    		sleep(1) # Sleep for 1 seconds

    except KeyboardInterrupt: # ctrl+C
	print "Cerrando aplicacion...."
	GPIO.cleanup()
	sys.exit()
