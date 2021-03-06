/* Inclusion de librerias*/
#include <Servo.h>           /* Libreria para uso de Servo */
#include <avr/io.h>          /* Libreria para uso de intrrupciones por timer */
#include <avr/interrupt.h>   /* Libreria para uso de intrrupciones por timer */

/* Declaracion de funciones propias */
void config_timer2_interrup();

/* Declaracion de variables globales*/
/* Variables Servo */
Servo servo1;           /* crea objeto servo*/
int PINSERVO = 7;       /* pin 7 conectado a señal del servo */
int PULSOMIN = 650;     /* pulso minimo en microsegundos */
int PULSOMAX = 2400;    /* pulso maximo en microsegundos */

/* Variables interrupcion externa 0 */
int PinUARTInterrupt=2; /* pin de interrupcion externa para deteccion de recepcion UART: pin 3*/
int flagRx=0;
char c;

/* Variables interrupcion externa 1*/
int PinInterruptE=3; /* pin de interrupcion externa: pin 3 */
volatile byte flagIE=0;

/* Variables interrupcion por timer 2*/
volatile int contador=0;

/* Otras variables globales*/
int PinLed=4;

/* Funcion de inicializacion: inicio de variables a utilizar y configuraciones*/
void setup(){
  
  /* Configuracion de I/O Digitales*/
  pinMode(PinLed, OUTPUT);

  /* Inicializacion de servo : attach(pin,microseg min, microseg max) */
  servo1.attach(PINSERVO, PULSOMIN, PULSOMAX);

  /* Inicializo el puerto serial a 9600 baudios */
  Serial.begin(9600);

  cli(); /* Deshabilitamos interrupciones globales durante configuracion de timer 2*/
  
  /* Configuracion de interrupcion por timer*/
  config_timer2_interrup();

  /* Configuracion de interrupcion externa 0 */
  attachInterrupt(digitalPinToInterrupt(PinUARTInterrupt), interrupcion_UART, FALLING); /* se selecciona interrupcion 1 atraves de pin 3*/
                                                                                        /* con rutina ISR llamada sensor*/
                                                                                        /* FALLING: interrupcion por flanco de bajada*/
  /* Configuracion de interrupcion externa 1 */
  attachInterrupt(digitalPinToInterrupt(PinInterruptE), sensor, RISING); /* se selecciona interrupcion 0 atraves de pin 2*/
                                                                         /* con rutina ISR llamada sensor*/
                                                                         /* RISING: interrupcion por flanco de subida*/
  sei(); /* habilitamos las interrupciones globales */
}

/* Funcion principal luego de iniciar variables*/
void loop(){

  if(flagIE==1)
  {
    servo1.write(0);    /* ubica el servo a 0 grados */
  }
    
  if(flagIE==2)
  {
    servo1.write(90);    /* ubica el servo a 90 grados */
    flagIE=0;
  }
}

/* Implementacion de funciones propias*/
void config_timer2_interrup()
{ 
  /* Configuracion de interrupcion por timer*/
  TCCR2A=0; /* limpiamos registro */
  TCCR2B=0; /* limpiamos registro */
  TCCR2B |= (1<<CS10); /* Preescaler en 1024*/
  TCCR2B |= (1<<CS12); /* (CS12 CS11 CS10) = 1 0 1 */
  
  TIMSK2=(1<<TOIE2); /* habilitamos interrupcion por timer 2*/
}

/* Interrupcion por timer 2*/
ISR(TIMER2_OVF_vect)
{
  contador++;
  if(contador==100 && flagRx==1) /* si ai recepcion RX por UART */
  {
    flagRx=0;
    if(Serial.available()) {        /* Si está disponible */
      c = Serial.read();            /* Guardamos la lectura en una variable char */
      if (c == '1') {               /* Si es '1', giro servo */
         digitalWrite(PinLed, HIGH);
         contador=0;
         flagIE=1;
      } else if (c == '2') {        /* Si es una '2', apago el LED */
         digitalWrite(PinLed, LOW);
      }
    }
  }
  
  if(contador == 200)
  {
    contador = 0;
    
    if(flagIE==1)
      flagIE=2;
  }
}

/* Funcion de interrpcion externa 1: rutina ISR */
void sensor()
{
  if(flagIE==0) /* if para evitar el antirrebote, ya que flagIE se hace 0 luego de los 20 ms*/
  {
    digitalWrite(PinLed, !digitalRead(PinLed));
    contador=0;
    flagIE=1;
  }
}

/*Funcion de interrupcion externa 0: Interrupcion por UART */
void interrupcion_UART()
{  
   if(flagRx==0) /* if para evitar el antirrebote, ya que flagRx se hace 0 luego de los 20 ms*/
   {
      contador=0; /* Receteamos contador par esperar la recepcion de UART */
      flagRx=1;   /* Indicamos que se debe analizar la recepcion */
   }
}
