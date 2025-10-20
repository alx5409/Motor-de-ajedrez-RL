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
        pass
    
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
        """
        Calcula la movilidad neta normalizada para el color evaluado.
        """
        movimientos_propios = self._contar_movimientos(self._color)
        color_oponente = Color.BLANCA if self._color == Color.NEGRA else Color.NEGRA
        movimientos_oponente = self._contar_movimientos(color_oponente)

        movilidad_maxima = float(self._pesos.get("max_movilidad", 40.0))
        movilidad_neta = (movimientos_propios - movimientos_oponente) / movilidad_maxima
        return float(movilidad_neta)
    
    def evaluar_estructura_peones(self) -> float:
        """
        Evalúa la estructura de peones para el color evaluado.
        """
        peso = float(self._pesos.get("estructura_peones", 0.2))

        color_propio = self._color
        color_oponente = Color.BLANCA if color_propio == Color.NEGRA else Color.NEGRA

        #Recopilar peones propios y enemigos por columna
        peones_propios = self._peones_por_columna(color_propio)
        peones_oponente = self._peones_por_columna(color_oponente)

        cantidad_peones_aislados_propios = self._contar_peones_aislados(peones_propios)
        cantidad_peones_doblados_propios = self._contar_peones_doblados(peones_propios)
        cantidad_peones_pasados_propios = self._contar_peones_pasados(peones_propios, peones_oponente, color_propio)

        # Coeficientes
        penalizacion_aislado = 0.5
        penalizacion_doblado = 0.5
        bono_pasado = 1.0

        puntuacion_unidades = (
            cantidad_peones_pasados_propios * bono_pasado
            - cantidad_peones_doblados_propios * penalizacion_doblado
            - cantidad_peones_aislados_propios * penalizacion_aislado)
        return float(puntuacion_unidades * peso)
    
    def evaluar_seguridad_rey(self) -> float:
        pass

    def evaluar_control_centro(self) -> float:
        pass
    
    def _contar_movimientos(self, color: Color) -> int:
        """
        Cuenta cuántos movimientos legales del color dado hay (con límite opcional).
        """
        generador = Generador_movimientos(self._tablero, self._reglas, color)
        return generador.contar_movimientos_legales()
    
    def _peones_por_columna(self, color: Color) -> dict:
        columnas: dict[int, array] = {}         # Diccionario 
        for pieza in self._tablero.listar_piezas_por_color(color):
            # Solo consideramos los peones
            if not isinstance(pieza, Peon):
                continue

            posicion = pieza.posicion_actual_entera
            if posicion is None:
                # Si la pieza no tiene posición saltamos la iteración
                continue
            fila, columna = int(posicion[0]), int(posicion[1])
            # Añadir la fila a la lista de la columna correspondiente
            columnas.setdefault(columna, []).append(fila)
        return columnas
        
    def _contar_peones_doblados(self, columnas_propias: dict) -> int:
        """
        Número de peones doblados (peones extras en la misma columna).
        """
        # Para cada lista de filas en las columnas, contar los peones extras.
        return sum(max(0, len(filas) - 1) for filas in columnas_propias.values())

    def _contar_peones_aislados(self, columnas_propias: dict) -> int:
        """
        Cuenta peones aislados: peones cuya columna no tiene peones propios en columnas adyacentes.
        """
        aislados = 0
        for columna, fila in columnas_propias.items():
            # Si no hay peones en las columnas adyacentes, todos los peones de la columna se consideran aislados
            if ((columna - 1) not in columnas_propias) and ((columna + 1) not in columnas_propias):
                aislados += len(fila)
        return aislados

    def _contar_peones_pasados(self, columnas_propias: dict, columnas_oponente: dict, color: Color) -> int:
        """
        Cuenta peones pasados: peones que no tienen peones enemigos en la misma
        columna o columnas adyacentes por delante (según el color).
        """
        dim = self._tablero.DIM_TABLERO
        pasados = 0
        # Para cada peón propio comprobamos la presencia de peones enemigos delante de la misma columna o en
        # columnas adyacentes.
        for columnas, filas in columnas_propias.items():
            for fila in filas:
                delante_enemigos = False
                # Comprobar columnas propia y adyacentes
                for columna in (columnas - 1, columnas, columnas + 1):
                    # Si está fuera del tablero, saltar
                    if columna < 0 or columna >= dim:
                        continue
                    filas_oponente = columnas_oponente.get(columna, [])
                    if color == Color.BLANCA:
                        # Para blancas, delante significa fila mayor
                        if any(fila_oponente > fila for fila_oponente in filas_oponente):
                            delante_enemigos = True
                            break
                    else:
                        # Para negras, delante significa fila menor
                        if any(fila_oponente < fila for fila_oponente in filas_oponente):
                            delante_enemigos = True
                            break
                if not delante_enemigos:
                    pasados += 1
        return pasados

    
    # def es_jaque(self, color: Color) -> bool:
    #     return self._reglas.es_jaque(color)

    # def es_jaque_mate(self, color: Color) -> bool:
    #     return self._reglas.es_jaque_mate(color)

    # def es_tablas(self) -> bool:
    #     return self._reglas.es_tablas()