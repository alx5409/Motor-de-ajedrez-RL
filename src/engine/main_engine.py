from array import array
import random
from typing import Any

from tablero import Tablero
from reglas import Reglas
from generador_movimiento import Generador_movimientos
from color import Color

def main_engine(max_turnos: int = 200, mostrar: bool = True, semilla: int | None = None) -> dict[str, Any]:
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
    while turnos_jugados < max_turnos:
        if mostrar:
            print(f"\\nTurno {turnos_jugados + 1} - Juegan: {color_actual.name}")
            tablero.mostrar_tablero()

        # Estados terminales antes de mover
        if reglas.es_jaque_mate(color_actual):
            ganador = color_actual.opuesto()
            if mostrar:
                print(f"Jaque mate. Gana: {ganador.name}")
            return {"estado": "jaque_mate", "ganador": ganador, "turnos": turnos_jugados}

        if reglas.es_ahogado(color_actual) or reglas.es_tablas():
            if mostrar:
                print("Tablas.")
            return {"estado": "tablas", "ganador": None, "turnos": turnos_jugados}

        generador = Generador_movimientos(tablero, reglas, color_actual)
        movimientos = generador.generar_movimientos_legales()

        if not movimientos:
            # Salvaguarda por consistencia
            if reglas.es_jaque(color_actual):
                ganador = color_actual.opuesto()
                if mostrar:
                    print(f"Sin movimientos legales y en jaque. Gana: {ganador.name}")
                return {"estado": "jaque_mate", "ganador": ganador, "turnos": turnos_jugados}
            if mostrar:
                print("Sin movimientos legales. Tablas.")
            return {"estado": "tablas", "ganador": None, "turnos": turnos_jugados}

        # Elegir un movimiento legal al azar y aplicarlo
        movimiento_aplicado = False
        while movimientos and not movimiento_aplicado:
            idx = rng.randrange(len(movimientos))
            pieza, destino = movimientos.pop(idx)

            origen = array("i", [int(pieza.posicion_actual_entera[0]), int(pieza.posicion_actual_entera[1])])
            movimiento_aplicado = tablero.mover_pieza(origen, destino)

        if not movimiento_aplicado:
            # Estado inesperado: el generador dio movimientos que no pudieron aplicarse
            if mostrar:
                print("Error de consistencia: no se pudo aplicar ningún movimiento legal.")
            return {"estado": "error_consistencia", "ganador": None, "turnos": turnos_jugados}

        color_actual = color_actual.opuesto()
        turnos_jugados += 1

    if mostrar:
        print("Límite de turnos alcanzado. Tablas por límite.")
    return {"estado": "tablas_limite_turnos", "ganador": None, "turnos": turnos_jugados}

if __name__ == "__main__":
    resultado = main_engine(max_turnos=100, mostrar=True, semilla=42)
    print(f"Resultado final: {resultado}")