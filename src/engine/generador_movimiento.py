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

    def generar_movimiento_para_pieza(self, pieza: Pieza) -> list:
        """
        Genera todos los movimientos legales posibles para la pieza dada.
        Returns:
            list[array]: Lista de destinos legales (array de dos enteros [fila, columna]).
        """
        movimientos_pieza = []
        for fila in range(self._tablero.DIM_TABLERO):
            for columna in range(self._tablero.DIM_TABLERO):
                destino = array('i', [fila, columna])
                if self.es_movimiento_legal(pieza, destino):
                    movimientos_pieza.append(destino)
        return movimientos_pieza
    
    def generar_movimientos_legales(self) -> list:
        """
        Genera todos los posibles movimientos legales posibles para el color actual en el tablero.
        Returns:
            list[tuple[Pieza, array]]: Lista de tuplas donde cada tupla es una pieza y su destino.
        """
        movimientos_legales: list = []
        piezas_color: list[Pieza] = self._tablero.listar_piezas_por_color(self._color_actual)
        # Recorre todas las piezas de color del tablero
        for pieza in piezas_color:
            for destino in self.generar_movimiento_para_pieza(pieza):
                    # Si el movimiento es valido lo agrega a la lista de movimientos válidos
                    movimientos_legales.append((pieza, destino))
        return movimientos_legales

    def es_movimiento_legal(self, pieza: Pieza, destino: array) -> bool:
        """
        Devuelte Trie si el movimiento es legal según las relgas de ajedrez.
        """
        return self._reglas.es_movimiento_legal(pieza, destino)

    def generar_capturas(self) -> list:
        """
        Genera todos los movimientos legales que son posibles capturas para el color actual.
        Returns:
            list[tuple[Pieza, array]]: Lista de tuplas (pieza, destino) que son capturas.
        """
        capturas = []
        for pieza, destino in self.generar_movimientos_legales():
            pieza_en_destino: Pieza = self._tablero.matriz_piezas[destino[0]][destino[1]]
            if pieza_en_destino and pieza_en_destino._color != self._color_actual:
                capturas.append((pieza, destino))
        
        return capturas
    
    def contar_movimientos_legales(self) -> int:
        """
        Cuenta todos los movimientos legales del color en el tablero.
        """
        return len(self.generar_movimientos_legales())