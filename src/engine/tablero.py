"""
Este archivo es para gestionar todo lo relacionado con el tablero,tanto la
 distribución como la vista del tablero, la gestión de las piezas. 
"""
from enum import Enum
from array import array
import numpy as np
from piezas import Peon, Caballo, Alfil, Torre, Dama, Rey
from piezas import Color

# Representación visual del tablero estándar de ajedrez:
#     A   B   C   D   E   F   G   H
#   +---+---+---+---+---+---+---+---+
# 8 | T | C | A | R | D | A | C | T | 8
#   +---+---+---+---+---+---+---+---+
# 7 | P | P | P | P | P | P | P | P | 7
#   +---+---+---+---+---+---+---+---+
# 6 |   |   |   |   |   |   |   |   | 6
#   +---+---+---+---+---+---+---+---+
# 5 |   |   |   |   |   |   |   |   | 5
#   +---+---+---+---+---+---+---+---+
# 4 |   |   |   |   |   |   |   |   | 4
#   +---+---+---+---+---+---+---+---+
# 3 |   |   |   |   |   |   |   |   | 3
#   +---+---+---+---+---+---+---+---+
# 2 | p | p | p | p | p | p | p | p | 2
#   +---+---+---+---+---+---+---+---+
# 1 | t | c | a | r | d | a | c | t | 1
#   +---+---+---+---+---+---+---+---+
#     A   B   C   D   E   F   G   H
#
# Mayúsculas = piezas blancas, minúsculas = piezas negras
# p = peón, c = caballo, a = alfil, t = torre, d = dama, r = rey

class EstadoCasilla(Enum):
    LIBRE = 0
    OCUPADA_BLANCA = 1
    OCUPADA_NEGRA = -1    
class Tablero:
    matriz_coordenadas_estandar: list[list]                                 # Coordenadas estandar
    matriz_coordenadas_enteras : np.ndarray                                 # Representación con coordenadas enteras para la lógica
    def __init__(self):           
        self._matriz_piezas = [[None for _ in range(8)] for _ in range(8)]      # Matriz de las referencias a las piezas
        
        # Inicializar las piezas del tablero
        # Peones
        for col in range(8):
            # Blancos
            peon_blanco = Peon(Color.BLANCA)
            peon_blanco.posicion_actual_entera = array('i', [col, 1])
            self._matriz_piezas[1][col] = peon_blanco
            # Negros
            peon_negro = Peon(Color.NEGRA)
            peon_negro.posicion_actual_entera = array('i', [col, 6])
            self._matriz_piezas[6][col] = peon_negro
        
        # Caballos
        # Blancos
        caballo_blanco_1 = Caballo(Color.BLANCA)
        caballo_blanco_1.posicion_actual_entera = array('i', [0, 1])
        self._matriz_piezas[0][1] = caballo_blanco_1

        caballo_blanco_2 = Caballo(Color.BLANCA)
        caballo_blanco_2.posicion_actual_entera = array('i', [0, 6])
        self._matriz_piezas[0][1] = caballo_blanco_2

        # Negros
        caballo_negro_1 = Caballo(Color.NEGRA)
        caballo_negro_1.posicion_actual_entera = array('i', [7, 1])
        self._matriz_piezas[0][1] = caballo_negro_1

        caballo_negro_2 = Caballo(Color.NEGRA)
        caballo_negro_2.posicion_actual_entera = array('i', [7, 6])
        self._matriz_piezas[0][1] = caballo_negro_2

        ## 