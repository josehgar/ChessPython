from tablero import Tablero

columnas_ajedrez = "abcdefghABCDEFGH"
fichas_negras = ['♖', '♘', '♗', '♕', '♔', '♙']

def traducir_input_a_indices(mov: str):
    return (int(mov[1]) - 1, ord(mov[0].upper()) - 65)

def traducir_indices_a_input(i: int, j: int):
    return f"{chr(j + 65)}{i + 1}"

def formato_correcto(i: str):
    return len(i) == 2 and i[0] in columnas_ajedrez and i[1] in "12345678"

def origen_correcto(turno_blanco: bool, o: str, t: Tablero):

    if not formato_correcto(o): return False

    fila, col = traducir_input_a_indices(o)
    casilla = t.tablero[fila][col]

    if casilla == '_':
        return False

    return (casilla not in fichas_negras) if turno_blanco else (casilla in fichas_negras)

def destino_correcto(turno_blanco: bool, d: str, t: Tablero, movs):

    if not formato_correcto(d): return False

    fila, col = traducir_input_a_indices(d)

    return (fila, col) in movs
