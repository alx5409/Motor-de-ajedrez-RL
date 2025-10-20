from array import array
from copy import deepcopy

from color import Color
from piezas import Alfil, Caballo, Rey, Pieza, Peon, Torre
from tablero import Tablero

class Reglas:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero

    def es_jaque(self, color: Color) -> bool:
        """
        Devuelve True si el rey del color dado está en jaque, , False en caso contrario.
        """
        rey: Rey = self.tablero.buscar_rey(color)
        if not rey:
            return False  # No hay rey del color especificado en el tablero

        posicion_rey = rey.posicion_actual_entera
        piezas_oponentes = self.tablero.listar_piezas_por_color(Color.NEGRA if color == Color.BLANCA else Color.BLANCA)
        #Comprueba que las piezas tienen un movimiento valido en la posición del rey
        for pieza in piezas_oponentes:
            if pieza.comprobar_movimiento_valido(posicion_rey, self.tablero.matriz_piezas):
                return True
        return False
    
    def es_jaque_mate(self, color: Color) -> bool:
        """
        Devuelve True si el rey del color está en jaque mate, False en caso contrario.
        """
        # Comprueba si el rey del color está en jaque.
        if (not self.es_jaque(color)):
            return False
        
        # Comprueba si todas las piezas del color tienen las casillas de los movimientos validos del rey en objetivo
        piezas_propias = self.tablero.listar_piezas_por_color(color)
        for pieza in piezas_propias:
            # Prueba todos los movimientos posibles para todas las piezas del color dado
            for fila in range(self.tablero.DIM_TABLERO):
                for columna in range(self.tablero.DIM_TABLERO):
                    destino = array('i', [fila, columna])
                    # Si el movimiento es legal y tras simularlo el rey no está en jaque, no es jaque mate
                    es_valido = pieza.comprobar_movimiento_valido(destino, self.tablero.matriz_piezas)
                    if not es_valido:
                        continue
                    tablero_simulado = self.simular_movimiento(pieza, destino)
                    reglas_simuladas = Reglas(tablero_simulado)
                    if not reglas_simuladas.es_jaque(color):
                        return False
                    
        return True
        
    def es_ahogado(self, color: Color) -> bool:
        """
        Devuelve True si el jugador del color dado está ahogado (no tiene movimientos legales y no está en jaque).
        """
        if self.es_jaque(color):
            return False
        # Comprueba exhaustivamente todos los movimientos validos de todas las piezas del color dado
        piezas_propias = self.tablero.listar_piezas_por_color(color)
        for pieza in piezas_propias:
            for fila in range(self.tablero.DIM_TABLERO):
                for columna in range(self.tablero.DIM_TABLERO):
                    destino = array('i', [fila, columna])
                    es_valido = pieza.comprobar_movimiento_valido(destino, self.tablero.matriz_piezas)
                    if not es_valido:
                        continue
                    tablero_simulado = self.simular_movimiento(pieza, destino)
                    reglas_simuladas = Reglas(tablero_simulado)
                    if not reglas_simuladas.es_jaque(color):
                        return False
                    
        return True

    def es_tablas(self) -> bool:
        """
        Devuelve True si la partida es tablas (ahogado o material insuficiente).
        """
        # Tablas si los dos jugadores están ahogados
        if self.es_ahogado(Color.BLANCA) or self.es_ahogado(Color.NEGRA):
            return True

        # Tablas por material insuficiente
        piezas = [pieza for fila in self.tablero.matriz_piezas for pieza in fila if pieza is not None]
        if all(isinstance(pieza, (Rey, Alfil, Caballo)) for pieza in piezas):
            # Solo reyes
            if all(isinstance(pieza, Rey) for pieza in piezas):
                return True
            # Rey vs rey + alfil o rey vs rey + caballo
            if len(piezas) == 3 and any(isinstance(pieza, (Alfil, Caballo)) for pieza in piezas):
                return True
        return False
        # TODO Añadir comprobacion de la regla de los 50 movimientos y repetición de posición

    def es_movimiento_legal(self, pieza: Pieza, destino: array) -> bool:
        """
        Devuelve True si el movimiento es legal según las reglas.
        """
        # Comprueba si el movimiento de la pieza en particular es valido
        if not pieza.comprobar_movimiento_valido(destino, self.tablero.matriz_piezas):
            return False
        
        # Si es valido, comprueba si es legal, es decir que sale del jaque
        tablero_simulado = self.simular_movimiento(pieza, destino)
        reglas_simuladas = Reglas(tablero_simulado)
        if reglas_simuladas.es_jaque(pieza.color):
            return False
        
        return True
        
    def puede_enrocar(self, color: Color, lado: str) -> bool:
        """
        Devuelve True si el jugador del color dado puede enrocar en el lado especificado ('corto' o 'largo').
        """
        # Busca el rey y las torres
        rey :Rey = self.tablero.buscar_rey(color)
        if not rey or rey.se_ha_movido:
            return False

        fila = rey.posicion_actual_entera[0]
        if lado == "corto":
            torre_col = 7
            cols_entre = [5, 6]
        elif lado == "largo":
            torre_col = 0
            cols_entre = [1, 2, 3]
        else:
            return False

        torre :Torre = self.tablero.matriz_piezas[fila][torre_col]
        if not torre or not isinstance(torre, Torre) or torre.se_ha_movido:
            return False

        # Comprobar que no hay piezas entre el rey y la torre
        for col in cols_entre:
            if self.tablero.matriz_piezas[fila][col] is not None:
                return False

        # Comprobar que el rey no está en jaque, ni pasa por ni termina en jaque
        for col in ([4] + cols_entre if lado == "largo" else [4, 5, 6]):
            tablero_simulado = self.simular_movimiento(rey, array('i', [fila, col]))
            reglas_simuladas = Reglas(tablero_simulado)
            if reglas_simuladas.es_jaque(color):
                return False

        return True

    def puede_capturar_al_paso(self, peon: Peon) -> bool:
        """
        Devuelve True si el peón puede capturar al paso según el estado actual del tablero.
        """
        # Comprobar que hay historial suficiente
        if not hasattr(self.tablero, "historial") or not self.tablero.historial:
            return False
        
        ultimo_mov = self.tablero.historial[-1]
        pieza_movida, origen, destino = ultimo_mov  # origen y destino son arrays [fila, columna]

        # El último movimiento debe ser de un peón que avanza dos casillas
        if not isinstance(pieza_movida, Peon):
            return False
        if pieza_movida.color == peon.color:
            return False

        # El peón rival debe estar en la columna adyacente y en la misma fila que el peón actual
        fila_peon, col_peon = peon.posicion_actual_entera
        fila_destino, col_destino = destino

        # El peón rival debe haber avanzado dos filas en un solo movimiento
        if abs(fila_destino - origen[0]) != 2:
            return False

        # El peón rival debe estar en la misma fila que el peón actual
        if fila_destino != fila_peon:
            return False

        # Deben estar en columnas adyacentes
        if abs(col_destino - col_peon) != 1:
            return False

        # La casilla de captura al paso debe estar vacía y dentro del tablero
        direccion = 1 if peon.color == Color.BLANCA else -1
        fila_captura = fila_peon + direccion
        if not (0 <= fila_captura < self.tablero.DIM_TABLERO):
            return False
        if self.tablero.matriz_piezas[fila_captura][col_destino] is not None:
            return False

        return True

    def simular_movimiento(self, pieza: Pieza, destino: array) -> Tablero:
        """
        Devuelve una copia del tablero tras simular el movimiento de la pieza al destino.
        Al ser una copia, no modifica el tablero original.
        """
        tablero_copia = deepcopy(self.tablero)
        origen = array('i', pieza.posicion_actual_entera)

        # Elimina la pieza de la posición original
        tablero_copia.matriz_piezas[origen[0]][origen[1]] = None

        # Crea una copia de la pieza, actualiza su posición y colócala en el destino
        pieza_copiada = deepcopy(pieza)
        pieza_copiada.posicion_actual_entera = array('i', [destino[0], destino[1]])
        tablero_copia.matriz_piezas[destino[0]][destino[1]] = pieza_copiada

        return tablero_copia
