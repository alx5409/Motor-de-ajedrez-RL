import numpy as np
from array import array 

from color import Color
from piezas import Alfil, Pieza, Torre

class Dama(Pieza):
    def __init__(self, color: Color):
        """
        Inicializa una dama con su color.
        """
        super().__init__(color)
        self._valor_relativo = 9

    def comprobar_movimiento_valido(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba si el movimiento es válido para una dama.
        La dama tiene los movimientos válidos de la torre y el alfil.
        """
        torre = Torre(self._color)
        torre.posicion_actual_entera = self.posicion_actual_entera
        alfil = Alfil(self._color)
        alfil.posicion_actual_entera = self.posicion_actual_entera

        return (
            torre.comprobar_movimiento_valido(movimiento, tablero) or
            alfil.comprobar_movimiento_valido(movimiento, tablero)
        )