from array import array

from piezas import Color, Rey, Pieza, Peon
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
    
    def es_jaque_mate(self, color: Color) -> bool:
        pass

    def es_ahogado(self, color: Color) -> bool:
        pass

    def es_tablas(self) -> bool:
        pass

    def es_movimiento_legal(self, pieza: Pieza, destino: array) -> bool:
        pass
        
    def puede_enrocar(self, color: Color, lado:str) -> bool:
        pass

    def puede_capturar_al_paso(self, peon: Peon) -> bool:
        pass
    
    def simular_movimiento(self, pieza: Pieza, destino: array) -> Tablero:
        pass
    