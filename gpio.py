from rich.panel import Panel
import time
from internal import function

panel1=Panel("", title="ENCODER DELTA", border_style="red")
ENCODER1 = 1
ENCODER2 = 2

# Crear una instancia de la consola Rich
function.init_pines()
#Primero leo el primer encoder
while True:
    function.create_register(0, ENCODER1)
    function.create_register(4, ENCODER2)
    #time.sleep(0.5)

