/* Inclusion de librerias*/
#include <Servo.h>           /* Libreria para uso de Servo */
#include <MsTimer2.h>        /* Libreria parauso de timer 2 */

/* Declaracion de funciones propias */
void interrupcion_UART();
void sensor();
void flash();
int calcular_distancia();
void porcentaje_led(int p_porcentaje);

/* Declaracion de variables globales*/

/* Variables Servo */
Servo servo1;           /* crea objeto servo*/
const int PINSERVO = 7;       /* pin 7 conectado a señal del servo */
const int PULSOMIN = 650;     /* pulso minimo en microsegundos */
const int PULSOMAX = 2400;    /* pulso maximo en microsegundos */
volatile byte flagConfigP=0;   /* flag de configuracion de posicion final*/
volatile int pos_start=0;

/* Variables interrupcion externa 0 */
const int PinUARTInterrupt=2; /* pin de interrupcion externa para deteccion de recepcion UART: pin 3*/
int flagRx=0;
char c;

/* Variables interrupcion externa 1*/
const int PinInterruptE=3; /* pin de interrupcion externa: pin 3 */
volatile byte flagIE=0;

/* Variables interrupcion por timer 2*/
volatile int contador=0;
volatile int contador_temp=0;
volatile int segundos_conf=10;
volatile int minutos_conf=0;
volatile int segundos=0;
volatile int minutos=0;
volatile byte flagTemp=0;
volatile byte flagTemp_OK=0;

/* Otras variables globales*/
volatile int duracion;
volatile int distancia;
volatile byte flagSD=0; /* Flag del sensor de distancia */
int porcentaje=0;
const int PinLedRed=4;
const int PinLedYellow=8;
const int PinLedGreen=12;
const int PinLedBlue=11;
const int EchoPin = 9;
const int TriggerPin = 10;

/* Funcion de inicializacion: inicio de variables a utilizar y configuraciones*/
void setup(){
  
  /* Configuracion de I/O Digitales*/
  pinMode(PinLedRed, OUTPUT);
  pinMode(PinLedYellow, OUTPUT);
  pinMode(PinLedGreen, OUTPUT);
  pinMode(PinLedBlue, OUTPUT);

  /* Configuraciones para sensor ultrasonico: sensor de distancia */
  pinMode(TriggerPin, OUTPUT);  /* trigger como salida */
  pinMode(EchoPin, INPUT);      /* echo como entrada */

  /* Inicializacion de servo : attach(pin,microseg min, microseg max) */
  servo1.attach(PINSERVO, PULSOMIN, PULSOMAX);

  /* Inicializo el puerto serial a 9600 baudios */
  Serial.begin(9600);
  
  /* Configuracion de interrupcion por timer*/
  MsTimer2::set(100, flash); // 100ms period
  MsTimer2::start();

  /* Configuracion de interrupcion externa 0 */
  attachInterrupt(digitalPinToInterrupt(PinUARTInterrupt), interrupcion_UART, FALLING); /* se selecciona interrupcion 1 atraves de pin 3*/
                                                                                        /* con rutina ISR llamada sensor*/
                                                                                        /* FALLING: interrupcion por flanco de bajada*/
  /* Configuracion de interrupcion externa 1 */
  attachInterrupt(digitalPinToInterrupt(PinInterruptE), sensor, RISING); /* se selecciona interrupcion 0 atraves de pin 2*/
                                                                         /* con rutina ISR llamada sensor*/
                                                                         /* RISING: interrupcion por flanco de subida*/
}

/* Funcion principal luego de iniciar variables*/
void loop(){
  
  if(flagIE==1)
  {
      servo1.write(pos_start);    /* ubica el servo a 0 grados, segun calibracion de posicion realizada */
  }
    
  if(flagIE==2)
  {
    servo1.write(pos_start+90);    /* ubica el servo a 90 grados, segun calibracion de posicion realizada */
    flagIE=0;
  }
  
  if(flagConfigP==2)
  {
    int envio_tx=1;
    Serial.println(envio_tx, DEC);      /* envio de valor 1 por UART, para calibrar angulo*/
    flagConfigP=3;
  }
  
  if(flagConfigP==4)
  {
    servo1.write(pos_start);    /* ubica el servo a posicion final en grados */
    flagConfigP=0;
  }

  if(flagTemp && !flagTemp_OK)
  {
     digitalWrite(PinLedBlue, HIGH);
     flagTemp_OK=1;
  }

  if(!flagTemp && flagTemp_OK)
  {
     digitalWrite(PinLedBlue, LOW);
     flagTemp_OK=0;
  }

  if(flagSD==1)
  {
    flagSD=0;
    distancia = calcular_distancia();
    if(distancia>0 && distancia<17)
    {
      if(distancia==4)
        porcentaje= 100;

      else if(distancia==5)
        porcentaje=85;

      else if(distancia==6)
        porcentaje=70;

      else
        porcentaje = 100 - ((distancia*100)/16);
    }
    else
      porcentaje = 0;

    porcentaje_led(porcentaje);

    Serial.println(porcentaje);    /* envio de valor de porcentaje por monitor*/
  }
}

/* Implementacion de funciones propias*/
int calcular_distancia()
{
  digitalWrite(TriggerPin, LOW);    /* Nos aseguramos de que el trigger está desactivado */
  delayMicroseconds(2);             /* Para estar seguros de que el trigger ya está LOW durante 2us */
  digitalWrite(TriggerPin, HIGH);   /* generacion del pulso a enviar */
  delayMicroseconds(10);            /* Esperamos 10 us. El pulso sigue active este tiempo del sensor */
  digitalWrite(TriggerPin, LOW);    /* Desactivamos trigger */

  duracion = pulseIn(EchoPin, HIGH);  /* con funcion pulseIn se espera un pulso alto en Echo */

  return duracion/58.2;          /* distancia medida en centimetros */
}

void porcentaje_led(int p_porcentaje)
{
  if(p_porcentaje<=100 && p_porcentaje>66)
    {
      digitalWrite(PinLedRed, LOW);
      digitalWrite(PinLedYellow, LOW);
      digitalWrite(PinLedGreen, HIGH);
    }
    
    else if(p_porcentaje<=66 && p_porcentaje>33)
    {
      digitalWrite(PinLedRed, LOW);
      digitalWrite(PinLedYellow, HIGH);
      digitalWrite(PinLedGreen, LOW);
    }

    else
    {
      digitalWrite(PinLedRed, HIGH);
      digitalWrite(PinLedYellow, LOW);
      digitalWrite(PinLedGreen, LOW);
    }
}

/* Interrupcion por timer 2*/
void flash()
{
  contador++;
  
  if(contador==1 && flagRx==1) /* si ai recepcion RX por UART */
  {
    flagRx=0;
    if(Serial.available()) {        /* Si está disponible */
      c = Serial.read();            /* Guardamos la lectura en una variable char */
      if (c == '1') {               /* Si es '1', giro servo */
         contador=0;
         flagIE=1;
         flagSD=1;
      } 
      else if (c == '2') {        /* Si es una '2', envio calculo de distancia por UART */
         flagSD=1;
      }
      else if (c == '3') {        /* Si es una '3', configuracion de posicion cero en servo */
         flagConfigP=1;
         contador=0;
      }
      else if (c == 'I' || c == 'i') {        /* Si es una 'I', se trata de un incremento de angulo */
        pos_start=pos_start+10;
        if(pos_start > 90)
          pos_start=90;

        flagConfigP=4;
      }
      else if (c == 'D' || c == 'd') {        /* Si es una 'D', se trata de un decremento de angulo */
        pos_start=pos_start-10;
        if(pos_start < -180)
          pos_start= -180;
        
        flagConfigP=4;
      }
      else if (c == '4') {        /* Si es una '4', habilitar modo de cargas por temporizador */
         flagTemp=1;
         contador_temp=0;
         segundos=0;
         minutos=0;
      }
      else if(c == 'S' || c == 's')
      {
        segundos_conf=segundos_conf+1;
        if(segundos_conf>60)
          segundos_conf=60;
      }
      else if(c == 'R' || c == 'r')
      {
        segundos_conf=0;
      }
      else if(c == 'M' || c == 'm')
      {
        minutos_conf=minutos_conf+1;
        if(minutos_conf>60)
          minutos_conf=60;
      }
      else if(c == 'N' || c == 'n')
      {
        minutos_conf=0;
      }
      else if (c == '5') {        /* Si es una '5', deshabilitar modo de cargas por temporizador */
         flagTemp=0;
         contador_temp=0;
         segundos=0;
         minutos=0;
      }
      c=0; /* Limpiamos dato de recepcion*/
    }
  }
  
  if(contador == 5)
  { 
    if(flagIE==1)
      flagIE=2;
  }

  if(contador == 8)
  {
    if(flagConfigP==1)
      flagConfigP=2;
  }

  if(flagTemp)
  {
    contador_temp++;
    if(contador_temp==10)
    {
      segundos++;
      contador_temp=0;
    }

    if(segundos==60)
    {
      minutos++;
      segundos=0;
    }

    if(minutos==minutos_conf && segundos==segundos_conf)
    {
      contador=0;
      flagIE=1;
      flagSD=1;
      segundos=0;
      minutos=0;
    }
  }
}

/* Funcion de interrpcion externa 1: rutina ISR */
void sensor()
{
  if(flagIE==0) /* if para evitar el antirrebote, ya que flagIE se hace 0 luego de los 20 ms*/
  {
    contador=0;
    flagIE=1;
    flagSD=1;
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
