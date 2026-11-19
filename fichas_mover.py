from fichas import Ficha

class Mover:
    def __init__(self, t):
        self.t = t # Tablero

        # Posiciones de spawn peones 
        self.primer_mov_peon = {}
        for i in range(1, 10 ,5):
            for j in range(8):
                self.primer_mov_peon[(i,j)] = True


    def mover_ficha(self, oi: int, oj: int, di: int, dj: int):
        if (not self.indices_validos(oi, oj) and not self.indices_validos(di, dj)):
            raise ValueError("Valor fuera del límite")

        elif self.t.tablero[oi][oj] == Ficha.VACIA.value:
            raise ValueError("Ficha no existente")

        movs_disponibles = self.obtener_movs(oi, oj) # Movimientos a los que se puede mover

        if (di, dj) not in movs_disponibles: # Intento de moverse a posición ilegal
            raise ValueError("Movimiento no válido")

        # Control de ficha capturada para actualizar contador
        ficha = self.t.tablero[di][dj]
        if ficha != Ficha.VACIA.value:
            if Ficha.es_blanco(ficha):
                self.t.fichas_blancas -= 1
            else:
                self.t.fichas_negras -= 1

        # Vaciar posición de origen de ficha movida
        self.t.tablero[di][dj] = self.t.tablero[oi][oj]
        self.t.tablero[oi][oj] = Ficha.VACIA.value

    def indices_validos(self, oi: int, oj: int):
        return 0 <= oi <= 7 and 0 <= oj <= 7

    def __pieza_mismo_equipo(self, oi: int, oj: int, di: int, dj: int):
        # Si son del mismo equipo, son del mismo color
        return (self.t.tablero[di][dj] != Ficha.VACIA.value 
            and Ficha.es_blanco(self.t.tablero[oi][oj]) == Ficha.es_blanco(self.t.tablero[di][dj]))
            
    def __movs_torre(self, oi: int, oj: int):
        movs = [] # Lista en la que se añadirán los movimientos legales de la torre
        vectores_direccion = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for delta_i, delta_j in vectores_direccion:
            i = oi + delta_i
            j = oj + delta_j

            while self.indices_validos(i,j):
                casilla = self.t.tablero[i][j]

                if casilla == '_':
                    movs.append((i, j))
                else:
                    if not self.__pieza_mismo_equipo(oi, oj, i, j):
                        movs.append((i, j))
                    break

                i += delta_i
                j += delta_j

        return movs

    def __movs_alfil(self, oi: int, oj: int) -> list[tuple[int, int]]:
        movs = [] # Lista en la que se añadirán los movimientos legales del alfil
        vectores_direccion = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

        for delta_i, delta_j in vectores_direccion:
            i = oi + delta_i
            j = oj + delta_j

            while self.indices_validos(i,j):
                casilla = self.t.tablero[i][j]

                if casilla == '_':
                    movs.append((i, j))
                else:
                    if not self.__pieza_mismo_equipo(oi, oj, i, j):
                        movs.append((i, j))
                    break

                i += delta_i
                j += delta_j

        return movs

    def __movs_reina(self, oi: int, oj: int):
        # La reina tiene los movimientos de la torre y el alfil combinados
        p1 = self.__movs_torre(oi, oj)
        p2 = self.__movs_alfil(oi, oj)

        return p1 + p2

    def __movs_peon(self, oi: int, oj: int) -> list[tuple[int, int]]:
        movs = []
        es_blanco = Ficha.es_blanco(self.t.tablero[oi][oj])
        direccion = -1 if es_blanco else 1
        fila_inicial = 6 if es_blanco else 1

    # Avance simple y doble
        i1 = oi + direccion
        if self.indices_validos(i1, oj) and self.t.tablero[i1][oj] == Ficha.VACIA.value:
            movs.append((i1, oj))

            i2 = oi + 2 * direccion
            if oi == fila_inicial and self.t.tablero[i2][oj] == Ficha.VACIA.value:
                movs.append((i2, oj))

    # Capturas en diagonal
        for dj in (-1, 1):
            ci = oi + direccion
            cj = oj + dj

            if (self.indices_validos(ci, cj)
                and self.t.tablero[ci][cj] != Ficha.VACIA.value
                and not self.__pieza_mismo_equipo(oi, oj, ci, cj)):
                movs.append((ci, cj))

        return movs
        
            
    def obtener_movs(self, oi: int, oj: int):
        deltas_mov = { # None = Delta de movimiento dependiente del tablero
            Ficha.TORRE_NEGRO.value: None,
            Ficha.TORRE_BLANCO.value: None,
            Ficha.CABALLO_NEGRO.value: [(2, 1), (1, 2), (2, -1), (-2, 1), (-2, -1), (-1, 2), (1, -2), (-1, -2)],
            Ficha.CABALLO_BLANCO.value: [(2, 1), (1, 2), (2, -1), (-2, 1), (-2, -1), (-1, 2), (1, -2), (-1, -2)],
            Ficha.ALFIL_NEGRO.value: None,
            Ficha.ALFIL_BLANCO.value: None,
            Ficha.REINA_NEGRO.value: None,
            Ficha.REINA_BLANCO.value: None,
            Ficha.REY_NEGRO.value: [(1,0), (1,1), (0,1), (-1,0), (-1,-1), (0,-1), (1,-1), (-1,1)],
            Ficha.REY_BLANCO.value: [(1,0), (1,1), (0,1), (-1,0), (-1,-1), (0,-1), (1,-1), (-1,1)],
            Ficha.PEON_NEGRO.value: None,
            Ficha.PEON_BLANCO.value: None
        }

        ficha = Ficha(self.t.tablero[oi][oj]) # Obtener enum de la ficha
        lista_deltas = deltas_mov[ficha.value]
        lista_movs = []

        if lista_deltas == None:
            if ficha == Ficha.TORRE_NEGRO or ficha == Ficha.TORRE_BLANCO:
                lista_movs = self.__movs_torre(oi, oj)
            elif ficha == Ficha.ALFIL_NEGRO or ficha == Ficha.ALFIL_BLANCO:
                lista_movs = self.__movs_alfil(oi, oj)
            elif ficha == Ficha.REINA_NEGRO or ficha == Ficha.REINA_BLANCO:
                lista_movs = self.__movs_reina(oi, oj) 
            elif ficha == Ficha.PEON_NEGRO or ficha == Ficha.PEON_BLANCO:
                lista_movs = self.__movs_peon(oi, oj)
        else:
            for delta in lista_deltas:
                di = oi + delta[0]
                dj = oj + delta[1]

                if (self.indices_validos(di, dj) and not self.__pieza_mismo_equipo(oi, oj, di, dj)):
                    lista_movs.append((di, dj))

        return lista_movs