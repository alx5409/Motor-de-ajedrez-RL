"""
Este archivo es para gestionar todo lo relacionado con el tablero,tanto la
 distribución como la vista del tablero, la gestión de las piezas. 
"""
class Tablero:

    matriz_coordenadas_enteras : int[int]   # Representación con coordenadas enteras para la lógica
    def __init__(self):
        self.__matriz_coordenadas_estandar : list[list[int]]  # Representación estándar de ajedrez A a H y 1 a 8.
