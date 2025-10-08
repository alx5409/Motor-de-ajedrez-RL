from piezas import Color, Rey, Pieza
from tablero import Tablero

class Reglas:
    def __init__(self, tablero: Tablero):
        self.tablero = tablero

    def es_jaque(self, color: Color) -> bool:
        rey: Rey = self.tablero.buscar_rey(color)
        if not rey:
            return False  # No hay rey del color especificado en el tablero

        posicion_rey = rey.posicion_actual_entera
        piezas_oponentes = self.tablero.listar_piezas_por_color(Color.NEGRA if color == Color.BLANCA else Color.BLANCA)