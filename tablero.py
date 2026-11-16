from colorama import Fore, Style, init

# Inicializar colorama una sola vez fuera de las funciones
init(autoreset=True)

class Tablero:
    def __init__(self):
        self.tablero = [["_" for i in range(8)] for j in range(8)]
        self.turno_blanco = True
        self.fichas_blancas = 16
        self.fichas_negras = 16

    def preparar_tablero(self):
        for i in range(0, 10, 7):
            self.tablero[i][0] = '♖' if i == 0 else '♜'
            self.tablero[i][1] = '♘' if i == 0 else '♞'
            self.tablero[i][2] = '♗' if i == 0 else '♝'
            self.tablero[i][3] = '♕' if i == 0 else '♛'
            self.tablero[i][4] = '♔' if i == 0 else '♚'
            self.tablero[i][5] = '♗' if i == 0 else '♝'
            self.tablero[i][6] = '♘' if i == 0 else '♞'
            self.tablero[i][7] = '♖' if i == 0 else '♜'

        for j in range(1, 10, 5):
            for k in range(8):
                self.tablero[j][k] = '♙' if j == 1 else '♟'

    def cambiar_turno(self):
        self.turno_blanco = not self.turno_blanco

    def __formatear_casilla(self, casilla):
        if casilla == "_":
            return "_  "
        elif casilla in ['♖', '♘', '♗', '♕', '♔', '♙']:
            return Style.DIM + Fore.WHITE + casilla + "  "
        else:
            return Style.BRIGHT + Fore.WHITE + casilla + "  "

    def imprimir_tablero(self):
        i = 0
        print("\t    A  B  C  D  E  F  G  H")
        print()
        for fila in self.tablero:
            i += 1
            print(f"\t{i}   ", end="")
            for casilla in fila:
                print(self.__formatear_casilla(casilla), end="")
            
            if i == 3:
                print(f"   Turno: {'Blanco' if self.turno_blanco else 'Negro'}", end="")
            elif i == 4:
                print(f"   Fichas Blancas: {self.fichas_blancas} | Fichas Negras: {self.fichas_negras}", end="")
            print()
        print()
        print()

    def imprimir_tablero_movs_correctos(self, movs_correctos, casilla_orig):
        tab_copia = [fila[:] for fila in self.tablero]
        c1, c2 = (int(casilla_orig[1]) - 1, ord(casilla_orig[0].upper()) - 65)

        i = 0
        print("\t    A  B  C  D  E  F  G  H")
        print()
        for fila_idx, fila in enumerate(tab_copia):
            i += 1
            print(f"\t{i}   ", end="")
            for col_idx, casilla in enumerate(fila):
                if (fila_idx, col_idx) == (c1, c2):
                    print(Style.BRIGHT + Fore.BLUE + casilla + "  ", end="")
                elif (fila_idx, col_idx) in movs_correctos:
                    if casilla == "_":
                        print(Style.BRIGHT + Fore.YELLOW + "·  ", end="")
                    else:
                        print(Style.BRIGHT + Fore.RED + casilla + "  ", end="")
                else:
                    print(self.__formatear_casilla(casilla), end="")
            
            if i == 3:
                print(f"   Turno: {'Blanco' if self.turno_blanco else 'Negro'}", end="")
            elif i == 4:
                print(f"   Fichas Blancas: {self.fichas_blancas} | Fichas Negras: {self.fichas_negras}", end="")
            print()
            
        print()
        print()

    def preparar_fichas_debug(self):
        self.tablero = [["_" for i in range(8)] for j in range(8)]
        
        self.tablero[4][1] = '♖' # Torre
        self.tablero[4][2] = '♘' # Caballo
        self.tablero[4][4] = '♗' # Alfil
        self.tablero[5][3] = '♕' # Reina
        self.tablero[6][4] = '♔' # Rey
        self.tablero[6][0] = '♙' # Peón blanco (fila inicial)

        # Fichas negras
        self.tablero[3][1] = '♜' # Torre
        self.tablero[3][2] = '♞' # Caballo
        self.tablero[3][4] = '♝' # Alfil
        self.tablero[2][3] = '♛' # Reina
        self.tablero[1][4] = '♚' # Rey
        self.tablero[1][0] = '♟' # Peón negro (fila inicial)

        # Ajustar los contadores
        self.fichas_blancas = 6
        self.fichas_negras = 6