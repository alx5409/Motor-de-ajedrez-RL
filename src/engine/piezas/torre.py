import numpy as np
from array import array

from color import Color
from .pieza import Pieza

class Torre(Pieza):

    def __init__(self, color: Color):
        """
        Inicializa una torre con su color.
        """
        super().__init__(color)
        self.valor_relativo = 5
        self.se_ha_movido = False        # Se usa para comprobar si se puede enrocar

    def comprobar_movimiento_valido(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba si el movimiento es válido para una torre.
        """
        if not super().comprobar_movimiento_valido(movimiento, tablero):
            return False

        fila_actual, columna_actual = self.posicion_actual_entera
        fila_destino, columna_destino = movimiento

        # El movimiento debe ser en línea recta: o bien la fila es igual (movimiento horizontal) o bien la columna es igual (movimiento vertical)
        if not ((fila_actual == fila_destino) or (columna_actual == columna_destino)):
            return False

        # Comprueba si no hay ninguna pieza en medio del movimiento
        paso_fila = 0 if fila_actual == fila_destino else (1 if fila_destino > fila_actual else -1)
        paso_columna = 0 if columna_actual == columna_destino else (1 if columna_destino > columna_actual else -1)
        fila = fila_actual + paso_fila
        columna = columna_actual + paso_columna
        while (fila != fila_destino or columna != columna_destino):
            if tablero[fila, columna] != 0:
                return False
            fila += paso_fila
            columna += paso_columna
        return True