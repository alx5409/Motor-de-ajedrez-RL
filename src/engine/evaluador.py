from array import array

from generador_movimiento import Generador_movimientos
from tablero import Tablero
from color import Color
from piezas import *
from utils import config
from reglas import Reglas

class Evaluador:

    def __init__(self, tablero: Tablero, reglas: Reglas, color_a_evaluar: Color = Color.BLANCA, pesos: dict = None):
        self._tablero = tablero
        self._reglas = reglas
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
    
    def evaluar_material(self) -> float:
        """
        Calcula la diferencia de material entre el color evaluado y el oponente.
        """
        color_propias = self._color
        color_oponente = Color.BLANCA if self._color == Color.NEGRA else Color.NEGRA

        piezas_propias = self._tablero.listar_piezas_por_color(color_propias)
        piezas_oponente = self._tablero.listar_piezas_por_color(color_oponente)

        valor_propias = 0
        for pieza_propia in piezas_propias:
            valor_propias += getattr(pieza_propia, "_valor_relativo", 0)

        valor_oponente = 0
        for pieza_oponente in piezas_oponente:
            valor_oponente += getattr(pieza_oponente, "_valor_relativo", 0)
        
        return float(valor_propias - valor_oponente)

    def evaluar_movilidad(self) -> float:
        pass

    def evaluar_estructura_peones(self) -> float:
        pass

    def evaluar_seguridad_rey(self) -> float:
        pass

    def evaluar_control_centro(self) -> float:
        pass
    
    # def _contar_movimientos(self, color: Color) -> int:
    #     """
    #     Cuenta cuántos movimientos legales del color dado hay (con límite opcional).
    #     """
    #     generador = Generador_movimientos(self._tablero, self._reglas, color)
    #     return generador.contar_movimientos_legales()
    
    # def es_jaque(self, color: Color) -> bool:
    #     return self._reglas.es_jaque(color)

    # def es_jaque_mate(self, color: Color) -> bool:
    #     return self._reglas.es_jaque_mate(color)

    # def es_tablas(self) -> bool:
    #     return self._reglas.es_tablas()