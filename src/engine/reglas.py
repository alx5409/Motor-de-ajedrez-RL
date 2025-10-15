from array import array

from piezas import Alfil, Caballo, Color, Rey, Pieza, Peon
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
        if (not self.es_jaque()):
            return False
        
        # Comprueba si todas las piezas del color tienen las casillas de los movimientos validos del rey en objetivo
        piezas_propias = self.tablero.listar_piezas_por_color(color)
        for pieza in piezas_propias:
            # Prueba todos los movimientos posibles en el tablero
            for fila in range(8):
                for columna in range(8):
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

        piezas_propias = self.tablero.listar_piezas_por_color(color)
        for pieza in piezas_propias:
            for fila in range(8):
                for columna in range(8):
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
        pass
        
    def puede_enrocar(self, color: Color, lado:str) -> bool:
        pass

    def puede_capturar_al_paso(self, peon: Peon) -> bool:
        pass
    
    def simular_movimiento(self, pieza: Pieza, destino: array) -> Tablero:
        pass
