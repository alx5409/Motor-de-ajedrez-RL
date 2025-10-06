"""
Archivo que define las clases de las piezas de Ajedrez así como sus métodos.
"""
from array import array
from enum import Enum

class Color(Enum):
    BLANCA = 1
    NEGRA = 2

class Pieza:

    # Constructor de la clase pieza
    def __init__(self, color):
        if not isinstance(color, Color):
            raise ValueError(f"Error, color inválido: {color}. Solo se permite BLANCA o NEGRA")
        self._color:  Color = color                                     # Color: BLANCA o NEGRA
        self._posicion_actual_entera: array = array('i', [0, 0])   # Posición en un array de enteros
        self._valor_relativo: int = 0                                   # Valor de la pieza
        
    
    def transformar_estandar_a_entero(posicion: list):
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
    def comprobar_movimiento_valido(self, movimiento: array):
        return (movimiento[0] in range(8)) and (movimiento[1] in range(8))

    # Método para mover una pieza genérica
    def mover_pieza(self, movimiento: list):
        movimiento_transformado = self.transformar_estandar_a_entero(movimiento)
        if (self.comprobar_movimiento_valido(movimiento_transformado)):
            self._posicion_actual_entera[0] = movimiento_transformado[0]
            self._posicion_actual_entera[1] = movimiento_transformado[1]

class Peon(Pieza):

    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 1    

class Caballo(Pieza):

    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 3   

class Alfil(Pieza):
    
    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 3   

class Torre(Pieza):
    
    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 5   

class Reina(Pieza):
    
    def __init__(self, color):
        super().__init__(color)
        self._valor_relativo = 9   

class Rey(Pieza):
    
    def __init__(self, color):
        super().__init__(color)

