"""
Archivo que define las clases de las piezas de Ajedrez así como sus métodos.
"""
from array import array
from enum import Enum

class Color(Enum):
    BLANCA = 1
    NEGRA = 2

class Pieza:

    posicion_actual_entera: array
    # Constructor de la clase pieza
    def __init__(self, color):
        if not isinstance(color, Color):
            raise ValueError(f"Error, color inválido: {color}. Solo se permite BLANCA o NEGRA")
        self._color:  Color = color                                     # Color: BLANCA o NEGRA
        self.posicion_actual_entera: array = array('i', [0, 0])         # Posición en un array de enteros
        self._valor_relativo: int = 0                                   # Valor de la pieza
        
    @staticmethod
    def transformar_estandar_a_entero(posicion: list):
        """
        Transforma la posición estándar a posición entera.

        Args:
            posicion (list): Posicion en tipo lista, por ejemplo ['A', 1].

        Returns:
            posicion_transformada (array de enteros): Posicion transformada a un array de enteros, por ejemplo [0, 0]
        """
        posicion_transformada: array = array('i', [0, 0])
        diccionario_letra_a_entero = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6,
            'H': 7
        }
        posicion_transformada[0] = diccionario_letra_a_entero[posicion[0]]
        posicion_transformada[1] = int(posicion[1]) - 1
        return posicion_transformada

    # Método para validar el movimiento entero de una pieza genérica
    def comprobar_movimiento_valido(self, movimiento: array, tablero):
        """
        Comprueba si el movimiento que se introduce es válido y si lo es devuelve True.
        Args:
            movimiento (array): Posicion de destino de la pieza como array de enteros.
        Returns:
            bool: True si el movimiento del peón es válido, False en otro caso.
        """
        return (movimiento[0] in range(8)) and (movimiento[1] in range(8))

    # Método para mover una pieza genérica
    def mover_pieza(self, movimiento: list, tablero):
        """
        Mueve una pieza tras comprobar que el movimiento es válido.
        Args:
            movimiento (list): Movimiento en formato estándar.
        """
        movimiento_transformado = self.transformar_estandar_a_entero(movimiento)
        if (self.comprobar_movimiento_valido(movimiento_transformado, tablero)):
            self.posicion_actual_entera[0] = movimiento_transformado[0]
            self.posicion_actual_entera[1] = movimiento_transformado[1]
    
    def capturar(self):
        """
        Devuelve el valor relativo de la pieza para sumar al oponente.
        Returns:
            valor_relativo (int): valor relativo de la pieza
        """
        return self._valor_relativo

class Peon(Pieza):

    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 1

    def comprobar_movimiento_valido(self, movimiento, tablero):
        columna_actual, fila_actual = self.posicion_actual_entera
        columna_destino, fila_destino = movimiento
        esta_ocupada: bool = False

        # Comprueba que el movimiento está dentro del tablero
        if not(columna_destino in range(8) and fila_destino in range(8)):
            # print("Movimiento fuera de los límites del tablero.")
            return False

        if self._color == Color.BLANCA:
            direccion = 1
        else:
            direccion = -1

        if self._color == Color.BLANCA:
            fila_inicial = 1
        else:
            fila_inicial = 6

        # Comprueba si la casilla a la que se quiere mover está ocupada
        if tablero[fila_destino, columna_destino] != 0:
            esta_ocupada = True

        # Avanza una casilla hacia delante
        if (columna_destino == columna_actual and
             fila_destino == fila_actual + direccion and
             not esta_ocupada):
            return True
        
        # Avanza dos casillas hacia delante si es su primer movimiento
        if (columna_destino == columna_actual and
            fila_actual == fila_inicial and
            fila_destino == fila_actual + 2 * direccion and
            tablero[fila_actual + 2 *direccion, columna_destino] == 0 and
            tablero[fila_actual + direccion, columna_destino] == 0):
            return True
        
        # Avanza en diagonal si hay una pieza en medio y es una pieza enemiga
        if (abs(columna_destino - columna_actual) == 1 and
            fila_destino == fila_actual + direccion):
            casilla = tablero[fila_destino, columna_destino]
            if (self._color == Color.BLANCA and casilla == -1) or (self._color == Color.NEGRA and casilla == 1):
                return True
        
        # print("Movimiento no válido.")
        return False
    
    def puede_transformarse(self):
        _, fila_actual = self.posicion_actual_entera
        if ((self._color == Color.BLANCA and fila_actual == 7) or
            (self._color == Color.NEGRA and fila_actual == 0)):
            return True
        return False
    
    def transformarse(self):
        if not self.puede_transformarse():
            print("El peón aún no puede transformarse.")
            return None
        
        print("En qué pieza quieres transformar el peón.")
        print("1. Dama\n 2. Torre\n3. Alfil\n 4. Caballo")
        opcion = input("Introduce el número de la pieza: ")

        if opcion == "1":
            return Dama(self._color)
        elif opcion == "2":
            return Torre(self._color)
        elif opcion == "3":
            return Alfil(self._color)
        elif opcion == "4":
            return Caballo(self._color)
        else:
            print("Opción no válida. Se transforma a Dama por defecto.")
            return Dama(self._color)
    
class Caballo(Pieza):

    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 3   

    def comprobar_movimiento_valido(self, movimiento, tablero):
        fila_destino = movimiento[0]
        columna_destino = movimiento[1]
        casilla_destino_ocupada: bool = False

        if (tablero[fila_destino][columna_destino] != 0):
            casilla_destino_ocupada = True
        
        
        return False

class Alfil(Pieza):
    
    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 3   

class Torre(Pieza):
    
    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 5   

class Dama(Pieza):
    
    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 9   

class Rey(Pieza):
    
    def __init__(self, color):
        super().__init__(color)

