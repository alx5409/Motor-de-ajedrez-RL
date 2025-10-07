import numpy as np
from array import array

from pieza import Color, Pieza

class Alfil(Pieza):

    def __init__(self, color: Color):
        """
        Inicializa un alfil con su color.
        """
        super().__init__(color)
        self._valor_relativo = 3

    def comprobar_movimiento_valido(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba si el movimiento es válido para un alfil.
        """
        if not super().comprobar_movimiento_valido(movimiento, tablero):
            return False

        fila_actual, columna_actual = self.posicion_actual_entera
        fila_destino, columna_destino = movimiento

        # Comprueba si el movimiento es en diagonal
        if not(abs(fila_destino - fila_actual) == abs(columna_destino - columna_actual)):
            return False

        # Comprueba si no hay ninguna pieza en medio del movimiento
        paso_fila = 1 if fila_destino > fila_actual else -1
        paso_columna = 1 if columna_destino > columna_actual else -1
        fila = fila_actual + paso_fila
        columna = columna_actual + paso_columna
        while (fila != fila_destino or columna != columna_destino):
            if tablero[fila, columna] != 0:
                return False
            fila += paso_fila
            columna += paso_columna

        return True