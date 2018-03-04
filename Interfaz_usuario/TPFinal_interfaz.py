# https://www.youtube.com/watch?v=cFAB5uWnuZQ
# www.ubidots.com
# https://pypi.python.org/pypi/ubidots/1.6.1

# Declaracion de librerias a utilizar
import sys
import serial
from ubidots import ApiClient
from time import sleep

#arduino = serial.Serial('/dev/ttyACM0', 9600)
arduino = serial.Serial('/dev/ttyUSB0', 9600) 
comando="1"
pulsador=0
contador_op1=1

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
			while (comando2!='9'):
				print("\n--- Interfaz Pet Feeder: MODO LOCAL ---")
				print(" MENU DE OPCIONES:")
				print(" 1- Cargar alimento.")
				print(" 2- Ver porcentaje de alimento.")
				print(" 3- Incrementar angulo de posicion de carga.")
				print(" 4- Decrementar angulo de posicion de carga.")
				print(" 5- Modificar numero de cargas.")
				print(" 6- Habilitar y configurar modo de cargas fijas por tiempo.")
				print(" 7- Deshabilitar modo de cargas fijas por tiempo.")
				print(" 8- Salir del modo local.")
				print(" 9- Salir de aplicacion.")
				print("---------------------------------------\n")
				comando2 = raw_input('Ingrese una opcion: ') #Input
				if comando2 == '1':
					contador_op1_temp=contador_op1
					while(contador_op1_temp>0):
						print('Enviando por puerto serial. Datos: '+comando2)
						arduino.write(comando2) # Mando dato hacia Arduino
						contador_op1_temp=contador_op1_temp-1
						sleep(0.8)
				elif comando2 == '2':
					print('Enviando por puerto serial. Datos: '+comando2)
					arduino.write(comando2) # Mando dato hacia Arduino
					recepcion_arduino=arduino.readline() # Espero recpcion de arduino
					print('Arduino-Uno:~$ El nivel de alimento es: '+recepcion_arduino)
					#aux = int(recepcion_arduino) # convierto cadena a entero # Saco lineas pq no son del modo remoto
					#new_value = porcentaje_alimento.save_value({'value': aux}) # Saco lineas pq no son del modo remoto
				elif comando2 == '3':
					continuar_op3="1"
					while (continuar_op3=='1'):
						print('Enviando por puerto serial. Datos: '+comando2)
						arduino.write(comando2) # Mando dato hacia Arduino
						recepcion_arduino2=arduino.readline() # Espero recpcion de arduino
						aux = int(recepcion_arduino2) # convierto cadena a entero
						if aux==1:
							print('Arduino-Uno-Config:~$ Ingrese un valor de angulo multiplo de 10')
							valor_angulo = raw_input(' Valor de angulo: ') #Input
							angulo_int = int(valor_angulo) # convierto cadena a entero
							angulo_int = angulo_int/10;
							if(angulo_int>9): # ya que giro maximo es de 180
								angulo_int=9;
							
							if(angulo_int<1):
								angulo_int=1;

							if((angulo_int <=9) and (angulo_int>0)):
								contador_op3 = angulo_int;
								while contador_op3>0:
									arduino.write("i") # Mando dato hacia Arduino
									contador_op3= contador_op3-1;
									sleep(0.5)

							else:
								print('Valor incorrecto')


						else:
							print('Arduino-Uno-Config:~$ Fallo peticion de incremento/decremento de angulo, recepcion: '+aux)
						continuar_op3 = raw_input('Continuar posicionando? Ingrese 1 para continuar, o 0 para salir: ') #Input

				elif comando2 == '4':
					continuar_op4="1"
					while (continuar_op4=='1'):
						print('Enviando por puerto serial. Datos: 3')
						arduino.write("3") # Mando dato hacia Arduino
						recepcion_arduino2=arduino.readline() # Espero recpcion de arduino
						aux = int(recepcion_arduino2) # convierto cadena a entero
						if aux==1:
							print('Arduino-Uno-Config:~$ Ingrese un valor de angulo multiplo de 10')
							valor_angulo = raw_input(' Valor de angulo: ') #Input
							angulo_int = int(valor_angulo) # convierto cadena a entero
							angulo_int = angulo_int/10;
							if(angulo_int>18): # ya que giro maximo es de 180
								angulo_int=18;
							
							if(angulo_int<1):
								angulo_int=1;

							if((angulo_int <=18) and (angulo_int>0)):
								contador_op4 = angulo_int;
								while contador_op4>0:
									arduino.write("d") # Mando dato hacia Arduino
									contador_op4= contador_op4-1;
									sleep(0.5)

							else:
								print('Valor incorrecto')


						else:
							print('Arduino-Uno-Config:~$ Fallo peticion de incremento/decremento de angulo, recepcion: '+aux)
						continuar_op4 = raw_input('Continuar posicionando? Ingrese 1 para continuar, o 0 para salir: ') #Input
				
				elif comando2 == '5':
					print('Arduino-Uno-Config:~$ Ingrese el numero de cargas que desea establecer.')
					contador_op1_char = raw_input(' Numero de cargas: ') #Input
					contador_op1 = int(contador_op1_char) # convierto cadena a entero
					if(contador_op1 > 10):
						contador_op1=10
						print('Arduino-Uno-Config:~$ El maximo valor es 10. El mismo se a configurado.')
					elif(contador_op1<1):
						contador_op1=1
						print('Arduino-Uno-Config:~$ El minimo valor es 1. El mismo se a configurado.')
					elif((contador_op1>0) and (contador_op1<=10)):
						print('Arduino-Uno-Config:~$ Numero de carga configurado a '+contador_op1_char)
					else:
						print('Arduino-Uno-Config:~$ El valor ingresado no es admitido')

				elif comando2 == '6':
					arduino.write("5") # Mando dato hacia Arduino, deshabilito modo de cargas por temporizador
					sleep(0.3)
					arduino.write("r") # Mando dato hacia Arduino, borro segundos configurados
					sleep(0.3)
					arduino.write("n") # Mando dato hacia Arduino, borro minutos configurados

					# Configuro nuevos segundos y minutos
					print('Arduino-Uno-Config:~$ Ingrese los minutos y segundos que desea establecer.')
					segundos_op6_char = raw_input(' Numero de segundos: ') #Input
					segundos_op6 = int(segundos_op6_char) # convierto cadena a entero
					if(segundos_op6 > 60):
						segundos_op6=60
						print('Arduino-Uno-Config:~$ El maximo valor es 60. El mismo se a configurado.')
					elif(segundos_op6<1):
						segundos_op6=1
						print('Arduino-Uno-Config:~$ El minimo valor es 1. El mismo se a configurado.')
					elif((segundos_op6>0) and (segundos_op6<=60)):
						print('Arduino-Uno-Config:~$ Numero de segundos configurado a '+segundos_op6_char)
						contador_op6 = segundos_op6;
						while contador_op6>0:
							arduino.write("s") # Mando dato hacia Arduino
							contador_op6= contador_op6-1;
							sleep(0.1)
					else:
						print('Arduino-Uno-Config:~$ El valor ingresado no es admitido')

					minutos_op6_char = raw_input(' Numero de minutos: ') #Input
					minutos_op6 = int(minutos_op6_char) # convierto cadena a entero
					if(minutos_op6 > 60):
						minutos_op6=60
						print('Arduino-Uno-Config:~$ El maximo valor es 60. El mismo se a configurado.')
					elif(minutos_op6<0):
						minutos_op6=0
						print('Arduino-Uno-Config:~$ El minimo valor es 0. El mismo se a configurado.')
					elif((minutos_op6>=0) and (minutos_op6<=60)):
						print('Arduino-Uno-Config:~$ Numero de segundos configurado a '+minutos_op6_char)
						contador_op6 = minutos_op6;
						while contador_op6>0:
							arduino.write("m") # Mando dato hacia Arduino
							contador_op6= contador_op6-1;
							sleep(0.1)
					else:
						print('Arduino-Uno-Config:~$ El valor ingresado no es admitido')

					arduino.write("4") # Mando dato hacia Arduino, habilito modo de cargas por temporizador

				elif comando2 == '7':
					arduino.write("5") # Mando dato hacia Arduino, deshabilito modo de cargas por temporizador

				elif comando2 == '8':
					break
				elif comando2 == '9':
					print "\nCerrando aplicacion...."
					arduino.close() # Finalizamos la comunicacion UART
					sys.exit()
					exit(0)
				else:
					comando2='1'
					print('El numero ingresado no se corresponde a ninguna opcion.')
					print('Intente nuevamente.')

		elif comando == '2': # Analisis de variable API Ubidots cada 1 segundo

			# Excepcion para verificar si se conecto correctamente con la API de ubidots
			try:
				print("Conectando a API Ubidots")
				api = ApiClient(token="A1E-kzn1qv9m8IDl8HveHrQyYKqzhEpDF3")
				variable = api.get_variable("5a4dba34c03f9774e0a8dd57")
				porcentaje_alimento = api.get_variable("5a60647bc03f9707bd47f11d")
				mostrar = api.get_variable("5a611773c03f97436c5ee58e")
				print("Conexion exitosa!!!")
			except:
				print("FALLO LA CONEXION API")
			
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
							new_value = variable.save_value({'value': 0})

					sleep(1)
					visualizar = mostrar.get_values(1)
					if visualizar[0].get("value") == 1:
						arduino.write(comando) # Mando dato hacia Arduino
						recepcion_arduino=arduino.readline() # Espero recepcion de arduino
						print('Arduino-Uno:~$ El nivel de alimento es: '+recepcion_arduino)
						aux = int(recepcion_arduino) # convierto cadena a entero
						new_pa = porcentaje_alimento.save_value({'value': aux})

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
