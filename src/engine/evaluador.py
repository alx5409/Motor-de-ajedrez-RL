from tablero import Tablero
from color import Color
from piezas import *

class Evaluador:

    def __init__(self, tablero: Tablero, color_a_evaluar: Color = Color.BLANCA):
        pass

    def evaluar(self) -> float:
        pass

    def evaluar_mobilidad(self) -> float:
        pass

    def evaluar_estructura_peones(self) -> float:
        pass

    def evaluar_seguridad_rey(self) -> float:
        pass

    def evaluar_control_centro(self) -> float:
        pass

    def es_jaque_mate(self) -> bool:
        pass

    def es_tablas(self) -> bool:
        pass