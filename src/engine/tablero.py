"""
Este archivo es para gestionar todo lo relacionado con el tablero, tanto la
distribución como la vista del tablero, la gestión de las piezas.
"""
from enum import Enum
from array import array
import numpy as np
import copy

from color import Color
from piezas import Alfil, Caballo, Dama, Peon, Pieza, Rey, Torre

class EstadoCasilla(Enum):
    LIBRE = 0
    OCUPADA_BLANCA = 1
    OCUPADA_NEGRA = -1    

class Tablero:
    DIM_TABLERO = 8                          # Dimensión del tablero estándar 8x8
    matriz_coordenadas_estandar: list[list]  # Coordenadas estándar ej: ['A', 2]
    matriz_coordenadas_enteras: np.ndarray   # Representación con coordenadas enteras para la lógica

    def __init__(self):     
        self.matriz_piezas = [[None for _ in range(self.DIM_TABLERO)] for _ in range(self.DIM_TABLERO)]  # Matriz de referencias a las piezas
        self.historial: list[tuple[Pieza, array, array]] = []                                             # Lista del historial de los movimientos de las piezas      
        # Peones
        for col in range(self.DIM_TABLERO):
            peon_blanco = Peon(Color.BLANCA)
            peon_blanco.posicion_actual_entera = array('i', [1, col])  # fila, columna
            self.matriz_piezas[1][col] = peon_blanco

            peon_negro = Peon(Color.NEGRA)
            peon_negro.posicion_actual_entera = array('i', [self.DIM_TABLERO - 2, col])  # fila, columna
            self.matriz_piezas[self.DIM_TABLERO - 2][col] = peon_negro

        # Torres
        torres_blancas = []
        torres_negras = []
        for fila, col, color, lista in [(0, 0, Color.BLANCA, torres_blancas), (0, self.DIM_TABLERO - 1, Color.BLANCA, torres_blancas),
                                        (self.DIM_TABLERO - 1, 0, Color.NEGRA, torres_negras), (self.DIM_TABLERO - 1, self.DIM_TABLERO - 1, Color.NEGRA, torres_negras)]:
            torre = Torre(color)
            torre.posicion_actual_entera = array('i', [fila, col])
            self.matriz_piezas[fila][col] = torre
            lista.append(torre)

        # Caballos
        caballos_blancos = []
        caballos_negras = []
        for fila, col, color, lista in [(0, 1, Color.BLANCA, caballos_blancos), (0, self.DIM_TABLERO - 2, Color.BLANCA, caballos_blancos),
                                        (self.DIM_TABLERO - 1, 1, Color.NEGRA, caballos_negras), (self.DIM_TABLERO - 1, self.DIM_TABLERO - 2, Color.NEGRA, caballos_negras)]:
            caballo = Caballo(color)
            caballo.posicion_actual_entera = array('i', [fila, col])
            self.matriz_piezas[fila][col] = caballo
            lista.append(caballo)

        # Alfiles
        alfiles_blancos = []
        alfiles_negras = []
        for fila, col, color, lista in [(0, 2, Color.BLANCA, alfiles_blancos), (0, self.DIM_TABLERO - 3, Color.BLANCA, alfiles_blancos),
                                        (self.DIM_TABLERO - 1, 2, Color.NEGRA, alfiles_negras), (self.DIM_TABLERO - 1, self.DIM_TABLERO - 3, Color.NEGRA, alfiles_negras)]:
            alfil = Alfil(color)
            alfil.posicion_actual_entera = array('i', [fila, col])
            self.matriz_piezas[fila][col] = alfil
            lista.append(alfil)

        # Damas
        dama_blanca = Dama(Color.BLANCA)
        dama_blanca.posicion_actual_entera = array('i', [0, 3])
        self.matriz_piezas[0][3] = dama_blanca

        dama_negra = Dama(Color.NEGRA)
        dama_negra.posicion_actual_entera = array('i', [self.DIM_TABLERO - 1, 3])
        self.matriz_piezas[self.DIM_TABLERO - 1][3] = dama_negra

        # Reyes
        rey_blanco = Rey(Color.BLANCA)
        rey_blanco.posicion_actual_entera = array('i', [0, 4])
        self.matriz_piezas[0][4] = rey_blanco

        rey_negro = Rey(Color.NEGRA)
        rey_negro.posicion_actual_entera = array('i', [self.DIM_TABLERO - 1, 4])
        self.matriz_piezas[self.DIM_TABLERO - 1][4] = rey_negro
    
    @property
    def matriz_piezas(self):
        """
        Método getter que devuelve la matriz de las piezas.
        """
        return self.matriz_piezas
    
    def mostrar_tablero(self):
        """
        Imprime el tablero en la consola.
        """
        for fila in reversed(self.matriz_piezas):
            print(" ".join([type(pieza).__name__[0] if pieza else "." for pieza in fila]))
        
    def mover_pieza(self, posicion_actual: array, posicion_destino: list) -> bool:
        """
        Mueve una pieza de la posicion actual a la posicion de destino si el movimiento es válido.
        """
        pieza: Pieza = self.matriz_piezas[posicion_actual[0]][posicion_actual[1]]
        if pieza and pieza.comprobar_movimiento_valido(posicion_destino):               # Comprueba si el movimiento es válido
            self.matriz_piezas[posicion_destino[0]][posicion_destino[1]] = pieza       # Mueve la pieza a la nueva posición
            self.matriz_piezas[posicion_actual[0]][posicion_actual[1]] = None          # Actualiza la posición de la pieza    
            return True
        return False
    
    def obtener_estado_matriz(self) -> np.ndarray:
        """
        Devuelve una matriz que representa el estado del tablero.
        0 para casillas libres, 1 para piezas blancas, -1 para piezas negras.
        """
        matriz = np.zeros((self.DIM_TABLERO, self.DIM_TABLERO), dtype=int)
        for fila in range(self.DIM_TABLERO):
            for col in range(self.DIM_TABLERO):
                pieza = self.matriz_piezas[fila][col]
                if pieza:                                                           # Comprueba si hay una pieza en la casilla
                    matriz[fila][col] = 1 if pieza.color == Color.BLANCA else -1    # 1 para blanca, -1 para negra
        return matriz
    
    def buscar_rey(self, color: Color):
        """
        Busca la posición del rey del color especificado.
        """
        for fila in range(self.DIM_TABLERO):
            for col in range(self.DIM_TABLERO):
                pieza = self.matriz_piezas[fila][col]
                if pieza and isinstance(pieza, Rey) and pieza.color == color:
                    return (fila, col)
        return None
    
    def clonar(self):
        """
        Devuelve una copia profunda del tablero. Esto es útil para simular movimientos sin afectar el estado actual.
        """
        return copy.deepcopy(self)
    
    def listar_piezas_por_color(self, color: Color) -> list[Pieza]:
        """
        Devuelve una lista de todas las piezas del color especificado en el tablero.
        """
        return [pieza for fila in self.matriz_piezas for pieza in fila if isinstance(pieza, Pieza) and pieza.color == color]