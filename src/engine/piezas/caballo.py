import numpy as np
from array import array
from pieza import Color, Pieza

class Caballo(Pieza):

    def __init__(self, color: Color):
        """
        Inicializa un caballo con su color.
        """
        super().__init__(color)
        self._valor_relativo = 3

    def comprobar_movimiento_valido(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba si el movimiento es válido para un caballo.
        """
        if not super().comprobar_movimiento_valido(movimiento, tablero):
            return False

        fila_actual, columna_actual = self.posicion_actual_entera
        fila_destino, columna_destino = movimiento

        # Comprueba los movimientos de la L cuando se mueven dos filas y una columna
        if (abs(fila_destino - fila_actual) == 2):
            if (abs(columna_destino - columna_actual) == 1):
                return True
        # Comprueba los movimientos de la L cuando se mueven dos columnas y una fila
        if (abs(columna_destino - columna_actual) == 2):
            if (abs(fila_destino - fila_actual) == 1):
                return True

        return False