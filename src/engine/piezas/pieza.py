"""
Archivo que define las clases de las piezas de Ajedrez así como sus métodos.
"""
from array import array
from enum import Enum
import numpy as np

class Color(Enum):
    BLANCA = 1
    NEGRA = 2

class Pieza:
    posicion_actual_entera: array

    def __init__(self, color: Color):
        """
        Inicializa una pieza con su color y posición inicial.
        """
        if not isinstance(color, Color):
            raise ValueError(f"Error, color inválido: {color}. Solo se permite BLANCA o NEGRA")
        self._color: Color = color
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
        if (self._color == Color.BLANCA and casilla_destino == 1) or (self._color == Color.NEGRA and casilla_destino == -1):
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

class Torre(Pieza):

    def __init__(self, color: Color):
        """
        Inicializa una torre con su color.
        """
        super().__init__(color)
        self._valor_relativo = 5

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

class Rey(Pieza):
    def __init__(self, color: Color):
        """
        Inicializa un rey con su color.
        """
        super().__init__(color)

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

