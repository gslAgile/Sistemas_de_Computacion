# https://www.youtube.com/watch?v=cFAB5uWnuZQ
# www.ubidots.com
# https://pypi.python.org/pypi/ubidots/1.6.1

# Declaracion de librerias a utilizar
import sys
import serial
from ubidots import ApiClient
from time import sleep

# Excepcion para verificar si se conecto correctamente con la API de ubidots
try:
	print("Conectando a API Ubidots")
	api = ApiClient(token="A1E-kzn1qv9m8IDl8HveHrQyYKqzhEpDF3")
	variable = api.get_variable("5a4dba34c03f9774e0a8dd57")
	porcentaje_alimento = api.get_variable("5a60647bc03f9707bd47f11d")
	print("Conexion exitosa!!!")
except:
	print("FALLO LA CONEXION API")


#arduino = serial.Serial('/dev/ttyACM0', 9600)
arduino = serial.Serial('/dev/ttyUSB0', 9600) 
comando="1"
pulsador=0

while (comando!='3'):
	try:
		print("\n--- Interfaz Pet Feeder ---")
		print(" MENU DE OPCIONES:")
		print(" 1- Habilitar modo local.")
		print(" 2- Habilitar modo remoto.")
		print(" 3- Salir de aplicacion.")
		print("---------------------------\n")
		comando = raw_input('Ingrese una opcion: ') #Input
		if comando == '1':
			print('MODO LOCAL HABILITADO')
			comando2="1"
			while (comando2!='4'):
				print("\n--- Interfaz Pet Feeder: MODO LOCAL ---")
				print(" MENU DE OPCIONES:")
				print(" 1- Cargar alimento.")
				print(" 2- Ver porcentaje de alimento.")
				print(" 3- Salir del modo local.")
				print(" 4- Salir de aplicacion.")
				print("---------------------------------------\n")
				comando2 = raw_input('Ingrese una opcion: ') #Input
				if comando2 == '1':
					print('Enviando por puerto serial. Datos: '+comando2)
					arduino.write(comando2) # Mando dato hacia Arduino
				elif comando2 == '2':
					print('Enviando por puerto serial. Datos: '+comando2)
					arduino.write(comando2) # Mando dato hacia Arduino
					recepcion_arduino=arduino.readline() # Espero recpcion de arduino
					print('Arduino-Uno:~$ El nivel de alimento es: '+recepcion_arduino)
					aux = int(recepcion_arduino) # convierto cadena a entero
					new_value = porcentaje_alimento.save_value({'value': aux})
				elif comando2 == '3':
					break
				elif comando2 == '4':
					print "\nCerrando aplicacion...."
					arduino.close() # Finalizamos la comunicacion UART
					sys.exit()
					exit(0)
				else:
					comando2='1'
					print('El numero ingresado no se corresponde a ninguna opcion.')
					print('Intente nuevamente.')

		elif comando == '2': # Analisis de variable API Ubidots cada 1 segundo
			print('MODO REMOTO HABILITADO')
			print("\n--- Pet Feeder en MODO REMOTO ---")
			print(" Analizando variables desde API UBIDOTS")
			print(" Para salir presione [Ctrl + c]\n")
			while True:
				try:
					last_value = variable.get_values(1)
					if last_value[0].get("value") == 1:
						if pulsador==0:
							print('Boton virtual: Encendido')
							print('Enviando por puerto serial. Datos enviados: 1')
							arduino.write("1") # Mando dato hacia Arduino
							#pulsador=1
							new_value = variable.save_value({'value': 0})
					#elif pulsador==1:
					#	pulsador=0
					#	print('Boton virtual: Apagado')

					sleep(1) # Sleep for 1 seconds

				except KeyboardInterrupt: # ctrl+C
					print "\nCerrando aplicacion...."
					arduino.close() # Finalizamos la comunicacion UART
					sys.exit()
			
		elif comando == '3':
			print "\nCerrando aplicacion...."
			arduino.close() # Finalizamos la comunicacion UART
			sys.exit()
			exit(0)

		else:
			comando='1'
			print('El numero ingresado no se corresponde a ninguna opcion.')
			print('Intente nuevamente.')

	except KeyboardInterrupt: # ctrl+C
		print "\nCerrando aplicacion...."
		arduino.close() # Finalizamos la comunicacion UART
		sys.exit()
