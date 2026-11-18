class Mover:
    def __init__(self, t):
        self.t = t
        self.primer_mov_peon = {}
        for i in range(1, 10 ,5):
            for j in range(8):
                self.primer_mov_peon[(i,j)] = True


    def mover_ficha(self, oi: int, oj: int, di: int, dj: int):
        if ((oi > 7 or oi < 0) or (oj > 7 or oj < 0) or
            (di > 7 or di < 0) or (dj > 7 or dj < 0)):

            raise ValueError("Valor fuera del límite")

        elif self.t.tablero[oi][oj] == "_":
            raise ValueError("Ficha no existente")

        movs_disponibles = self.obtener_movs(oi, oj)
        if (di, dj) not in movs_disponibles:
            raise ValueError("Movimiento no válido")

        ficha = self.t.tablero[di][dj]
        if ficha != "_":
            if self.__es_blanca(ficha):
                self.t.fichas_blancas -= 1
            else:
                self.t.fichas_negras -= 1
        self.t.tablero[di][dj] = self.t.tablero[oi][oj]
        self.t.tablero[oi][oj] = "_"

    def __es_blanca(self, ficha):
        return ficha not in ['♖', '♘', '♗', '♕', '♔', '♙']

    def __pieza_mismo_equipo(self, oi: int, oj: int, di: int, dj: int):
        return (self.t.tablero[di][dj] != "_" 
            and self.__es_blanca(self.t.tablero[oi][oj]) == self.__es_blanca(self.t.tablero[di][dj]))
            
    def __movs_torre(self, oi: int, oj: int):
        ficha_ref = self.t.tablero[oi][oj]
        movs = []
        i_actual = oi
        j_actual = oj

        fin_bucle = False

        while not fin_bucle and i_actual < 7:
            i_actual += 1

            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion

            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        fin_bucle = False
        i_actual = oi

        while not fin_bucle and i_actual > 0:
            i_actual -= 1
        
            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion
        
            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        fin_bucle = False
        i_actual = oi
        
        while not fin_bucle and j_actual < 7:
            j_actual += 1
                
            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion
                
            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        fin_bucle = False
        j_actual = oj
                
        while not fin_bucle and j_actual > 0:
            j_actual -= 1
                        
            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion
                        
            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        return movs

    def __movs_alfil(self, oi: int, oj: int):
        ficha_ref = self.t.tablero[oi][oj]
        movs = []
        i_actual = oi
        j_actual = oj

        fin_bucle = False

        while not fin_bucle and (i_actual > 0 and j_actual > 0):
            i_actual -= 1
            j_actual -= 1

            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion

            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        i_actual = oi
        j_actual = oj
        fin_bucle = False

        while not fin_bucle and (i_actual < 7 and j_actual > 0):
            i_actual += 1
            j_actual -= 1

            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion
            
            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        i_actual = oi
        j_actual = oj
        fin_bucle = False

        while not fin_bucle and (i_actual > 0 and j_actual < 7):
            i_actual -= 1
            j_actual += 1

            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion
            
            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        i_actual = oi
        j_actual = oj
        fin_bucle = False

        while not fin_bucle and (i_actual < 7 and j_actual < 7):
            i_actual += 1
            j_actual += 1

            if (self.t.tablero[i_actual][j_actual] == '_'):
                movs.append((i_actual, j_actual))
                continue # Siguiente iteracion
            
            if (self.__es_blanca(ficha_ref) != self.__es_blanca(self.t.tablero[i_actual][j_actual])):
                movs.append((i_actual, j_actual))
            fin_bucle = True

        return movs

    def __movs_reina(self, oi: int, oj: int):
        p1 = self.__movs_torre(oi, oj)
        p2 = self.__movs_alfil(oi, oj)

        return p1 + p2

    def __movs_peon(self, oi: int, oj: int):
        movs = []
        es_blanco = self.__es_blanca(self.t.tablero[oi][oj])
        direccion = -1 if es_blanco else 1
        fila_inicial = 6 if es_blanco else 1

        ai = oi + direccion
        if 0 <= ai <= 7 and self.t.tablero[ai][oj] == "_":
            movs.append((ai, oj))

            if oi == fila_inicial and self.t.tablero[oi + 2 * direccion][oj] == "_":
                movs.append((oi + 2 * direccion, oj))

        for dj in (-1, 1):
            ci, cj = oi + direccion, oj + dj
            if 0 <= ci <= 7 and 0 <= cj <= 7:
                if (self.t.tablero[ci][cj] != "_"
                        and not self.__pieza_mismo_equipo(oi, oj, ci, cj)):
                    movs.append((ci, cj))

        return movs
        
            
    def obtener_movs(self, oi: int, oj: int):
        deltas_mov = { # None = Delta de movimiento dependiente del tablero
            '♖': None,
            '♜': None,
            '♘': [(2, 1), (1, 2), (2, -1), (-2, 1), (-2, -1), (-1, 2), (1, -2), (-1, -2)],
            '♞': [(2, 1), (1, 2), (2, -1), (-2, 1), (-2, -1), (-1, 2), (1, -2), (-1, -2)],
            '♗': None,
            '♝': None,
            '♕': None,
            '♛': None,
            '♔': [(1,0), (1,1), (0,1), (-1,0), (-1,-1), (0,-1), (1,-1), (-1,1)],
            '♚': [(1,0), (1,1), (0,1), (-1,0), (-1,-1), (0,-1), (1,-1), (-1,1)],
            '♙': None,
            '♟': None
        }

        ficha = self.t.tablero[oi][oj]
        lista_deltas = deltas_mov[ficha]
        lista_movs = []

        if (lista_deltas == None):
            if ficha in ('♖', '♜'):
                lista_movs = self.__movs_torre(oi, oj)
            elif ficha in ('♗', '♝'):
                lista_movs = self.__movs_alfil(oi, oj)
            elif ficha in ('♕', '♛'):
                lista_movs = self.__movs_reina(oi, oj) 
            elif ficha in ('♙', '♟'):
                lista_movs = self.__movs_peon(oi, oj)
        else:
            for delta in lista_deltas:
                di = oi + delta[0]
                dj = oj + delta[1]

                if (0 <= di <= 7 and 0 <= dj <= 7
                and not self.__pieza_mismo_equipo(oi, oj, di, dj)):
                    lista_movs.append((di, dj))

        return lista_movs