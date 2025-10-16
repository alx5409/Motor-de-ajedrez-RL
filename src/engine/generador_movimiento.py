from array import array

from tablero import Tablero
from color import Color
from piezas import *
from reglas import Reglas

class Generador_movimientos:
    
    def __init__(self, tablero: Tablero, reglas: Reglas, color: Color):
        pass
    
    def generar_movimientos_legales(self) -> list:
        pass

    def generar_movimiento_para_pieza(self, pieza: Pieza) -> list:
        pass

    def es_movimiento_legal(self, pieza: Pieza) -> list:
        pass

    def generar_capturas(self) -> list:
        pass