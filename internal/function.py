from rich.console import Console
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import RPi.GPIO as GPIO
import time

pines_input = [2,3,4,17,27,22,10,9] #LOS PRIMEROS PINES TIENEN A LOS BIT MAS SIGNIFICATIVOS
pines_output = [23,24,25,8,7,1,12,16]
console = Console()
clear = 0
result_old = [0,0]
def init_pines():
##
   #Se configuran 8 pines como salida y 8 como entrada. Los que se configuran como entrada se los inicializa en 0
    ##
   GPIO.setmode(GPIO.BCM)  # Usar el número del pin GPIO según la nomenclatura BCM
 
   for pin in pines_input:
       GPIO.setup(pin, GPIO.IN)

   for pin in pines_output:
       GPIO.setup(pin, GPIO.OUT)
       GPIO.output(pin, GPIO.LOW)

def show_data(registro_32_bits,console,encoder):
##
   #Se realizan operaciones de desplazamiento y luego se hace una and para obtener los grados, minutos y segudos. El signo esta compuesto de un solo BIT, de los 32 bits, 3 no son usados.
   #Una vez que se obtienen los valores se imprimi el panel para mostrar los datos por consola. Solo se actualizan los datos si cambiaron

   #:param int[32] registro_32_bits: se guardan los bits que se obtinen de los 4 latch correspodiente al encoder seleccionado.

   #:param console : Se pasa la consola creada imprir los resultados y tambien limpiar cada vez que se actualizan los datos.

   #:param int encoder: Es una macro creada para edenfiticar el encoder, tiene solo dos valores (1 y 2)
    ##
    signo_str="-"
    signo           = (registro_32_bits >> 31) & 1
    centena_grado   = (registro_32_bits >> 27) & 0b1111
    decena_grado    = (registro_32_bits >> 20) & 0b1111
    unidad_grado    = (registro_32_bits >> 16) & 0b1111
    decena_minutos  = (registro_32_bits >> 12) & 0b1111
    unidad_minutos  = (registro_32_bits >> 8) & 0b1111
    decena_segundos = (registro_32_bits >> 4) & 0b1111
    unidad_segundos = registro_32_bits & 0b1111
    global panel1
    global result_old
    global clear
    if(signo==1):
      signo_str="+"
    if(encoder ==1):
      result_str= signo_str+" "+ str (centena_grado)+str(decena_grado)+str(unidad_grado)+":"+str(decena_minutos)+str(unidad_minutos)+":"+str(decena_segundos)+str(unidad_segundos)
      panel1 = Panel(result_str, title="ENCODER DELTA", border_style="red")
      if(result_old[0] == registro_32_bits):
        clear = 0
      result_old[0] = registro_32_bits
    else:
      result_str= signo_str+" "+ str (centena_grado)+str(decena_grado)+str(unidad_grado)+":"+str(decena_minutos)+str(unidad_minutos)+":"+str(decena_segundos)+str(unidad_segundos)
      panel2 = Panel.fit(result_str, title="ENCODER ALFA", style="bold white on black", padding=(1, 2))
      if((result_old[1] != registro_32_bits) or clear != 0):
        columns = Columns([panel1, panel2], equal=True)
        columns = Align.center(columns, vertical = "middle")
        console.clear(columns)
        console.print("\n" *8,columns)
      result_old[1] = registro_32_bits
      clear = 1
    #print("-------------------------------")
    #print(signo)
    #print(centena_grado)
    #print(decena_grado)
    #print(unidad_grado)
    #print(decena_minutos)
    #print(unidad_minutos)
    #print(decena_segundos)
    #print(unidad_segundos)
    #print("-------------------------------")
    #print("-------------------------------")


def read_pins(pines_input):
##
    #Esta función lee 8 pines y guarda su estados en un array.

    #:param int[8] pines_input: representa cada GPIO.

    #:return: int[8]: se guardan los estados (LOW or HIGH)
    ##
    estados = [GPIO.input(pin) for pin in pines_input]
    byte=0
    #guardo de mas significativo a menos significativo
    for i, estado in enumerate(estados):
       byte |= estado << 7-i
    return byte


def create_register(indece, encoder):
##
    #Se toman los valores de los latchs correspodientes a cada encoder, aqui se arma el registro de 32 bits.
    #Cuando se arma el registro se llama a la funcion que actualiza la informacion en el consola
    #:param int indece: segun el encoder puede valer 0 o 4 para recorrer asi los 4 latchs de un encoder en particular.

    #:param int indece: macro que permite identificar al encoder
    ##
    size_former=indece#index old
    registro=0
    for i in range(4):
        GPIO.output(pines_output[size_former], GPIO.LOW)
        GPIO.output(pines_output[indece], GPIO.HIGH)
        size_former=indece
        aux=read_pins(pines_input)
        registro |= aux << 8*i #de mas significativo a menos significativo
        indece=indece+1

    show_data(registro,console, encoder )
