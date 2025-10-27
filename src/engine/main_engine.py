import logging

from tablero import Tablero
from reglas import Reglas
from generador_movimiento import Generador_movimientos
from ..utils import config
import piezas

def _leer_configuracion_archivo(config_path:str = "config.txt") -> dict:
    """
    Lee el archivo de configuración y devuelve un diccionario con los valores y las claves encontrados. 
    """
    configuracion = {}
    with open(config_path, "r") as config_file:
        for linea in config_file:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if "=" in linea:
                clave, valor = linea.split("=", 1)
                clave = clave.strip()
                valor = valor.strip()
                # Intenta convertir a int o float
                if clave == "DIM_TABLERO":
                    valor = int(valor)
                elif clave == "SEED":
                    valor = int(valor)
                elif clave in ("material", "movilidad", "estructura_peones", "seguridad_rey",
                            "control_centro", "mate", "max_movilidad"):
                    valor = float(valor)
                configuracion[clave] = valor

    return configuracion
    

def configurar(config_path: str = "config.txt") -> dict:
    """
    Carga y aplica la configuración global del motor de ajedrez desde un archivo de texto.
    Permite especificar:
    - pesos de la evaluación
    - dimensión del tablero
    - modo de juego
    - semilla aleatoria

    Si falta alguna clave, usa valores por defecto
    """
    # Valores por defecto
    configuracion = {
        "DIM_TABLERO": 8,
        "MODO_JUEGO": "greedy",
        "SEED": None,
        "material": 1.0,
        "movilidad": 0.05,
        "estructura_peones": 0.2,
        "seguridad_rey": 0.5,
        "control_centro": 0.1,
        "mate": 1000000,
        "max_movilidad": 40.0,
    }
    # Modifica la configuración si lee correctamente del archivo
    try:
        configuracion.update(_leer_configuracion_archivo(config_path))
    except FileNotFoundError:
        logging.error(f"Archivo de configuración {config_path} no encontrado. Usando la configuración por defecto.")

    return configuracion

def seleccionar_movimiento(tablero, generador, evaluador, modo="greedy"):
    """
    Selecciona el siguiente movimiento a aplicar según el modo: greedy, aleatorio, agente o manual.
    """
    movimientos = generador.generar_movimientos_legales()
    if not movimientos:
        return None

    if modo == "aleatorio":
        import random
        return random.choice(movimientos)
    elif modo == "greedy":
        mejor_mov = None
        mejor_valor = float('-inf')
        for mov in movimientos:
            # Simula el movimiento en una copia del tablero
            tablero_copia = tablero.copiar()
            pieza, destino = mov
            tablero_copia.mover(pieza, destino)
            valor = evaluador.evaluar()
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        return mejor_mov
    else:
        # Por defecto, devuelve el primer movimiento legal
        return movimientos[0]

def main_engine():
    """
    Orquesta la ejecución del motor de ajedrez.
    """
    config_dict = configurar()
    dim = config_dict["DIM_TABLERO"]
    modo = config_dict["MODO_JUEGO"]

    # Inicialización de componentes principales
    tablero = Tablero(dim)
    reglas = Reglas(tablero)
    generador = Generador_movimientos(tablero, reglas)
    from evaluador import Evaluador
    evaluador = Evaluador(tablero, reglas, color=tablero.color_actual, pesos=config_dict)

    historial = []
    ply = 0
    max_plies = 200

    while ply < max_plies:
        if reglas.es_jaque_mate(tablero.color_actual):
            print("Jaque mate. Fin de la partida.")
            break
        if reglas.es_tablas():
            print("Tablas. Fin de la partida.")
            break

        mov = seleccionar_movimiento(tablero, generador, evaluador, modo=modo)
        if mov is None:
            print("No hay movimientos legales. Fin de la partida.")
            break

        pieza, destino = mov
        tablero.mover(pieza, destino)
        historial.append((pieza, destino))
        ply += 1

        # Mostrar tablero tras cada jugada (opcional)
        print(tablero)

    print("Partida finalizada.")
    # Aquí podrías guardar el historial o exportar la partida si lo deseas

if __name__ == "__main__":
    main_engine()