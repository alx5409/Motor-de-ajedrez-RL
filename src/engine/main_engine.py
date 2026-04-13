from array import array
import random
from typing import Any, TypedDict

from piezas import Pieza
from tablero import Tablero
from reglas import Reglas
from generador_movimiento import Generador_movimientos
from color import Color

type Movimiento = tuple[Pieza, array]

class EngineResultado(TypedDict):
    estado: str
    ganador: Color | None
    turnos: int
    semilla: int | None
    max_turnos: int
    ultimo_movimiento: str | None
    detalle: str | None

    def actualizar(self, estado: str, ganador: Color | None, turnos: int, ultimo_movimiento: str | None = None, detalle: str | None = None) -> None:
        """
        Actualiza los campos del resultado con la información proporcionada.
        """
        self.estado = estado
        self.ganador = ganador
        self.turnos = turnos
        self.ultimo_movimiento = ultimo_movimiento
        self.detalle = detalle
    
def _seleccionar_movimiento_aleatorio(movimientos: list[Movimiento], rng: random.Random) -> Movimiento | None:
    """
    Selecciona un movimiento aleatorio de la lista de movimientos disponibles.
    Devuelve None si la lista está vacía.
    """
    if not movimientos:
        return None
    idx = rng.randrange(len(movimientos))
    return movimientos[idx]

def main_engine(max_turnos: int = 200, mostrar: bool = True, semilla: int | None = None) -> EngineResultado:
    """
    Función principal del motor de ajedrez.
    Args:
        max_turnos (int): Número máximo de turnos antes de declarar un empate.
        mostrar (bool): Si es True, muestra el tablero después de cada movimiento.
        semilla (int | None): Semilla para la generación de movimientos aleatorios.
    """

    tablero = Tablero()
    reglas = Reglas(tablero)
    color_actual = Color.BLANCA
    rng = random.Random(semilla)
    turnos_jugados = 0
    resultado: EngineResultado = EngineResultado(semilla=semilla, max_turnos=max_turnos, ultimo_movimiento=None, detalle=None)
    while turnos_jugados < max_turnos:
        if mostrar:
            print(f"\\nTurno {turnos_jugados + 1} - Juegan: {color_actual.name}")
            tablero.mostrar_tablero()

        # Estados terminales antes de mover
        if reglas.es_jaque_mate(color_actual):
            ganador = color_actual.opuesto()
            resultado.actualizar(estado="jaque_mate", ganador=ganador, turnos=turnos_jugados, ultimo_movimiento=None)
            if mostrar:
                print(f"Jaque mate. Gana: {ganador.name}")
            return resultado

        if reglas.es_ahogado(color_actual) or reglas.es_tablas():
            resultado.actualizar(estado="tablas", ganador=None, turnos=turnos_jugados, ultimo_movimiento=None)
            if mostrar:
                print("Tablas.")
            return resultado

        generador = Generador_movimientos(tablero, reglas, color_actual)
        movimientos = generador.generar_movimientos_legales()

        if not movimientos:
            # Salvaguarda por consistencia
            if reglas.es_jaque(color_actual):
                ganador = color_actual.opuesto()
                resultado.actualizar(estado="jaque_mate", ganador=ganador, turnos=turnos_jugados, ultimo_movimiento=None)
                if mostrar:
                    print(f"Sin movimientos legales y en jaque. Gana: {ganador.name}")
                return resultado
            if mostrar:
                print("Sin movimientos legales. Tablas.")
            resultado.actualizar(estado="tablas", ganador=None, turnos=turnos_jugados, ultimo_movimiento=None)
            return resultado

        # Elegir un movimiento legal al azar y aplicarlo
        movimiento_aplicado = False
        while movimientos and not movimiento_aplicado:
            movimiento = _seleccionar_movimiento_aleatorio(movimientos, rng)
            if movimiento is None:
                break
            pieza, destino = movimiento
            movimientos.remove(movimiento)

            origen = array("i", [int(pieza.posicion_actual_entera[0]), int(pieza.posicion_actual_entera[1])])
            movimiento_aplicado = tablero.mover_pieza(origen, destino)

        if not movimiento_aplicado:
            # Estado inesperado: el generador dio movimientos que no pudieron aplicarse
            if mostrar:
                print("Error de consistencia: no se pudo aplicar ningún movimiento legal.")
            resultado.actualizar(estado="error_consistencia", ganador=None, turnos=turnos_jugados, ultimo_movimiento=None, detalle="No se pudo aplicar ningún movimiento generado como legal.")
            return resultado

        color_actual = color_actual.opuesto()
        turnos_jugados += 1

    if mostrar:
        print("Límite de turnos alcanzado. Tablas por límite.")
    resultado.actualizar(estado="tablas_limite_turnos", ganador=None, turnos=turnos_jugados, ultimo_movimiento=None, detalle=None)
    return resultado

if __name__ == "__main__":
    resultado = main_engine(max_turnos=100, mostrar=True, semilla=42)
    print(f"Resultado final: {resultado}")