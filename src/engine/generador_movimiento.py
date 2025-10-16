from array import array

from tablero import Tablero
from color import Color
from piezas import *
from reglas import Reglas

class Generador_movimientos:
    
    def __init__(self, tablero: Tablero, reglas: Reglas, color: Color):
        self._tablero = tablero
        self._reglas = reglas
        self._color_actual = color
    
    def generar_movimientos_legales(self) -> list:
        """
        Genera todos los posibles movimientos legales posibles para el color actual en el tablero.
        Returns:
            list[tuple[Pieza, array]]: Lista de tuplas donde cada tupla es una pieza y su destino
        """
        movimientos_legales: list = []
        piezas_color: list[Pieza] = self._tablero.listar_piezas_por_color(self._color_actual)
        # Recorre todas las piezas de color del tablero
        for pieza in piezas_color:
            for fila in range(self._tablero.DIM_TABLERO):
                for columna in range(self._tablero.DIM_TABLERO):
                    # Para cada pieza fija como destino todas las casillas del tablero y comprueba si en cada una el movimiento es valido
                    destino = array('i', [fila, columna])
                    if self._reglas.es_movimiento_legal(pieza, destino):
                        # Si el movimiento es valido lo agrega a la lista de movimientos válidos
                        movimientos_legales.append((pieza, destino))
        
        return movimientos_legales

    def generar_movimiento_para_pieza(self, pieza: Pieza) -> list:
        pass

    def es_movimiento_legal(self, pieza: Pieza) -> list:
        pass

    def generar_capturas(self) -> list:
        pass