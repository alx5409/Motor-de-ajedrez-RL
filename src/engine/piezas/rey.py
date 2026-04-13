import numpy as np
from array import array

from color import Color
from .pieza import Pieza

class Rey(Pieza):
    def __init__(self, color: Color):
        """
        Inicializa un rey con su color.
        """
        super().__init__(color)
        self.se_ha_movido = False       # Se usa para comprobar si se puede enrocar 

    def comprobar_movimiento_valido(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba si el movimiento es válido para un rey (una casilla en cualquier dirección).
        """
        if not super().comprobar_movimiento_valido(movimiento, tablero):
            return False

        fila_actual, columna_actual = self.posicion_actual_entera
        fila_destino, columna_destino = movimiento

        if (abs(fila_destino - fila_actual) <= 1) and (abs(columna_destino - columna_actual) <= 1):
            return True

        return False