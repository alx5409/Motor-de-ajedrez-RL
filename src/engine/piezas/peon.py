from array import array
import numpy as np

from color import Color
from piezas import Alfil, Caballo, Dama, Pieza, Torre

class Peon(Pieza):

    def __init__(self, color: Color):
        """
        Inicializa un peón con su color.
        """
        super().__init__(color)
        self.valor_relativo = 1

    def comprobar_movimiento_valido(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba si el movimiento es válido para un peón.
        """
        if not super().comprobar_movimiento_valido(movimiento, tablero):
            return False

        fila_actual, columna_actual = self.posicion_actual_entera
        fila_destino, columna_destino = movimiento

        direccion = 1 if self.color == Color.BLANCA else -1
        fila_inicial = 1 if self.color == Color.BLANCA else 6

        casilla_destino = tablero[fila_destino, columna_destino]
        destino_esta_ocupado = casilla_destino != 0

        # Avanza una casilla hacia delante
        es_avance_simple = (
            columna_destino == columna_actual and
            fila_destino == fila_actual + direccion and
            not destino_esta_ocupado
        )
        if es_avance_simple:
            return True

        # Avanza dos casillas desde la posición inicial
        es_avance_doble = (
            columna_destino == columna_actual and
            fila_actual == fila_inicial and
            fila_destino == fila_actual + 2 * direccion and
            tablero[fila_actual + direccion, columna_destino] == 0 and
            casilla_destino == 0
        )
        if es_avance_doble:
            return True

        # Captura en diagonal
        es_diagonal = (
            abs(columna_destino - columna_actual) == 1 and
            fila_destino == fila_actual + direccion
        )
        if es_diagonal:
            es_enemigo = (
                (self.color == Color.BLANCA and casilla_destino == -1) or
                (self.color == Color.NEGRA and casilla_destino == 1)
            )
            if es_enemigo:
                return True

        return False

    def puede_transformarse(self) -> bool:
        """
        Comprueba si el peón ha llegado a la última fila.
        Returns:
            bool: True si puede transformarse, False en caso contrario.
        """
        fila_actual, _ = self.posicion_actual_entera
        return ((self.color == Color.BLANCA and fila_actual == 7) or
                (self.color == Color.NEGRA and fila_actual == 0))

    def transformarse(self):
        """
        Permite al usuario elegir la pieza a la que se transforma el peón.
        Returns:
            Pieza: Nueva pieza elegida por el usuario.
        """
        if not self.puede_transformarse():
            return None

        print("En qué pieza quieres transformar el peón.")
        print("1. Dama\n2. Torre\n3. Alfil\n4. Caballo")
        opcion = input("Introduce el número de la pieza: ")

        if opcion == "1":
            return Dama(self.color)
        if opcion == "2":
            return Torre(self.color)
        if opcion == "3":
            return Alfil(self.color)
        if opcion == "4":
            return Caballo(self.color)

        print("Opción no válida. Se transforma a Dama por defecto.")
        return Dama(self.color)