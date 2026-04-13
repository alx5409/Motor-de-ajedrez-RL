from enum import Enum

class Color(Enum):
    BLANCA = 1
    NEGRA = 2

    def opuesto(self):
        """
        Devuelve el color opuesto.
        """
        return Color.BLANCA if self == Color.NEGRA else Color.NEGRA