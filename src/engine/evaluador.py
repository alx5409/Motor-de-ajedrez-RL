from tablero import Tablero
from color import Color
from piezas import *
from utils import config

class Evaluador:

    def __init__(self, tablero: Tablero, color_a_evaluar: Color = Color.BLANCA, pesos: dict = None):
        self._tablero = tablero
        self._color = color_a_evaluar
        if (pesos is not None):
            self._pesos = pesos.copy()
        else:
            self._pesos = config.PESOS_POR_DEFECTO.copy()

    def __str__(self) -> str:
        return f"Evaluador para {self._color.name} (pesos: {len(self._pesos)})"

    def __repr__(self) -> str:
        return f"Evaluador (color={self._color.name}, pesos_llaves:  {list(self._pesos.keys())})"

    def evaluar(self) -> float:
        """
        Devuelve la evaluación global de la posición para el color dado.
        """
        

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