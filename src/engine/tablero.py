"""
Este archivo es para gestionar todo lo relacionado con el tablero, tanto la
distribución como la vista del tablero, la gestión de las piezas.
"""
from enum import Enum
from array import array
import numpy as np
from piezas import Alfil, Caballo, Dama, Peon, Color, Rey, Torre

class EstadoCasilla(Enum):
    LIBRE = 0
    OCUPADA_BLANCA = 1
    OCUPADA_NEGRA = -1    

class Tablero:
    matriz_coordenadas_estandar: list[list]  # Coordenadas estándar
    matriz_coordenadas_enteras: np.ndarray   # Representación con coordenadas enteras para la lógica

    def __init__(self):           
        self._matriz_piezas = [[None for _ in range(8)] for _ in range(8)]  # Matriz de referencias a las piezas

        # Peones
        for col in range(8):
            peon_blanco = Peon(Color.BLANCA)
            peon_blanco.posicion_actual_entera = array('i', [col, 1])
            self._matriz_piezas[1][col] = peon_blanco

            peon_negro = Peon(Color.NEGRA)
            peon_negro.posicion_actual_entera = array('i', [col, 6])
            self._matriz_piezas[6][col] = peon_negro

        # Torres
        torres_blancas = []
        torres_negras = []
        for col, fila, color, lista in [(0, 0, Color.BLANCA, torres_blancas), (7, 0, Color.BLANCA, torres_blancas),
                                        (0, 7, Color.NEGRA, torres_negras), (7, 7, Color.NEGRA, torres_negras)]:
            torre = Torre(color)
            torre.posicion_actual_entera = array('i', [col, fila])
            self._matriz_piezas[fila][col] = torre
            lista.append(torre)

        # Caballos
        caballos_blancos = []
        caballos_negras = []
        for col, fila, color, lista in [(1, 0, Color.BLANCA, caballos_blancos), (6, 0, Color.BLANCA, caballos_blancos),
                                        (1, 7, Color.NEGRA, caballos_negras), (6, 7, Color.NEGRA, caballos_negras)]:
            caballo = Caballo(color)
            caballo.posicion_actual_entera = array('i', [col, fila])
            self._matriz_piezas[fila][col] = caballo
            lista.append(caballo)

        # Alfiles
        alfiles_blancos = []
        alfiles_negras = []
        for col, fila, color, lista in [(2, 0, Color.BLANCA, alfiles_blancos), (5, 0, Color.BLANCA, alfiles_blancos),
                                        (2, 7, Color.NEGRA, alfiles_negras), (5, 7, Color.NEGRA, alfiles_negras)]:
            alfil = Alfil(color)
            alfil.posicion_actual_entera = array('i', [col, fila])
            self._matriz_piezas[fila][col] = alfil
            lista.append(alfil)

        # Damas
        dama_blanca = Dama(Color.BLANCA)
        dama_blanca.posicion_actual_entera = array('i', [3, 0])
        self._matriz_piezas[0][3] = dama_blanca

        dama_negra = Dama(Color.NEGRA)
        dama_negra.posicion_actual_entera = array('i', [3, 7])
        self._matriz_piezas[7][3] = dama_negra

        # Reyes
        rey_blanco = Rey(Color.BLANCA)
        rey_blanco.posicion_actual_entera = array('i', [4, 0])
        self._matriz_piezas[0][4] = rey_blanco

        rey_negro = Rey(Color.NEGRA)
        rey_negro.posicion_actual_entera = array('i', [4, 7])
        self._matriz_piezas[7][4] = rey_negro
