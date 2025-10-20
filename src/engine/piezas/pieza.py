"""
Archivo que define las clases de las piezas de Ajedrez así como sus métodos.
"""
from array import array
import numpy as np

from color import Color

class Pieza:
    posicion_actual_entera: array

    def __init__(self, color: Color):
        """
        Inicializa una pieza con su color y posición inicial.
        """
        if not isinstance(color, Color):
            raise ValueError(f"Error, color inválido: {color}. Solo se permite BLANCA o NEGRA")
        self.color: Color = color
        self.posicion_actual_entera: array = array('i', [0, 0])
        self._valor_relativo: int = 0

    @staticmethod
    def transformar_estandar_a_entero(posicion: list) -> array:
        """
        Transforma la posición estándar a posición entera.

        Args:
            posicion (list): Posicion en tipo lista, por ejemplo ['A', 1].

        Returns:
            array: Posicion transformada a un array de enteros, por ejemplo [0, 0]
        """
        posicion_transformada: array = array('i', [0, 0])
        diccionario_letra_a_entero = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3,
            'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        posicion_transformada[0] = diccionario_letra_a_entero[posicion[0]]
        posicion_transformada[1] = int(posicion[1]) - 1
        return posicion_transformada

    def esta_dentro_tablero(self, movimiento: array) -> bool:
        """
        Comprueba si el movimiento está dentro de los límites del tablero.
        """
        return (movimiento[0] in range(8)) and (movimiento[1] in range(8))

    def casilla_no_ocupada_por_misma_pieza(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba que la casilla de destino no está ocupada por una pieza del mismo color.
        """
        fila_destino, columna_destino = movimiento
        casilla_destino = tablero[fila_destino, columna_destino]
        if (self.color == Color.BLANCA and casilla_destino == 1) or (self.color == Color.NEGRA and casilla_destino == -1):
            return False
        return True

    def comprobar_movimiento_valido(self, movimiento: array, tablero: np.ndarray) -> bool:
        """
        Comprueba si el movimiento es válido en general:
        - No quedarse en la misma casilla
        - Estar dentro del tablero
        - No capturar pieza propia
        """
        if (movimiento[0] == self.posicion_actual_entera[0]) and (movimiento[1] == self.posicion_actual_entera[1]):
            return False
        if not self.esta_dentro_tablero(movimiento):
            return False
        if not self.casilla_no_ocupada_por_misma_pieza(movimiento, tablero):
            return False
        return True

    def mover_pieza(self, movimiento: list, tablero: np.ndarray) -> None:
        """
        Mueve una pieza tras comprobar que el movimiento es válido.
        Args:
            movimiento (list): Movimiento en formato estándar.
            tablero (np.ndarray): Matriz del tablero.
        """
        movimiento_transformado = self.transformar_estandar_a_entero(movimiento)
        if self.comprobar_movimiento_valido(movimiento_transformado, tablero):
            tablero[self.posicion_actual_entera[0], self.posicion_actual_entera[1]] = 0
            tablero[movimiento_transformado[0], movimiento_transformado[1]] = self
            self.posicion_actual_entera[0] = movimiento_transformado[0]
            self.posicion_actual_entera[1] = movimiento_transformado[1]

    def capturar(self) -> int:
        """
        Devuelve el valor relativo de la pieza para sumar al oponente.
        Returns:
            int: valor relativo de la pieza
        """
        return self._valor_relativo