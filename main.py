import subprocess
from tablero import Tablero
from fichas_mover import Mover
import input_manager as im

t = Tablero()
m = Mover(t)

def limpiar():
    subprocess.run("cls", shell=True) # Limpiar pantalla

t.preparar_fichas_debug() # Preparar fichas de inicio 

while True:
    limpiar()
    t.imprimir_tablero()

    fin = False
    s = ""

    while not fin:
        s = input("Introduce ficha de origen: ")
        if im.origen_correcto(t.turno_blanco, s, t):
            fin = True

    indices_orig = im.traducir_input_a_indices(s)
    movs_correctos = m.obtener_movs(indices_orig[0], indices_orig[1])
    limpiar()

    t.imprimir_tablero_movs_correctos(movs_correctos, casilla_orig=s)

    fin = False
    while not fin:
        d = input("Introduce ficha de destino: ")
        if im.destino_correcto(t.turno_blanco, d, t, movs_correctos):
            fin = True

    indices_dest = im.traducir_input_a_indices(d)
    m.mover_ficha(indices_orig[0], indices_orig[1], indices_dest[0], indices_dest[1])

    t.cambiar_turno()
