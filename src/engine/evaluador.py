from array import array

from generador_movimiento import Generador_movimientos
from tablero import Tablero
from color import Color
from piezas.pieza import Pieza
from piezas.peon import Peon
# from piezas.rey import Rey
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
        Combina las métricas parciales y devuelve una evaluación para el color a evaluar.
        Casos terminales:
        - si el rey del color a evaluar está en jaque mate -> valor muy negativo
        - si el rey del oponente está en jaque mate -> valor muy positivo

        Las métricas parciales se combinan usando los pesos que se introducen en el constructor.
        """
        # colores
        color_oponente = Color.BLANCA if self._color == Color.NEGRA else Color.NEGRA

        # valores terminales
        mate_valor = float(self._pesos.get("mate", 1e6))    # Se escoge un valor muy grande

        # Casos terminales gestionados por Reglas
        if self._reglas.es_jaque_mate(self._color):
            return -mate_valor
        if self._reglas.es_jaque_mate(color_oponente):
            return mate_valor
        if self._reglas.es_tablas():
            return 0.0

        # Pesos
        peso_material = float(self._pesos.get("material", 1.0))
        peso_movilidad = float(self._pesos.get("movilidad", 0.05))
        peso_estructura = float(self._pesos.get("estructura_peones", 0.2))
        peso_seguridad = float(self._pesos.get("seguridad_rey", 0.5))
        peso_centro = float(self._pesos.get("control_centro", 0.1))

        # Métricas parciales (todas desde la perspectiva de self._color)
        material = self.evaluar_material()
        movilidad = self.evaluar_movilidad()
        estructura = self.evaluar_estructura_peones()
        seguridad = self.evaluar_seguridad_rey()
        centro = self.evaluar_control_centro()

        # Combinación lineal de las puntuaciones parciales
        puntuacion_global = (
            material * peso_material
            + movilidad * peso_movilidad
            + estructura * peso_estructura
            + seguridad * peso_seguridad
            + centro * peso_centro
        )

        return float(puntuacion_global)
    
    def evaluar_material(self) -> float:
        """
        Calcula la diferencia de material entre el color evaluado y el oponente.
        """
        color_propio = self._color
        color_oponente = Color.BLANCA if self._color == Color.NEGRA else Color.NEGRA

        piezas_propias = self._tablero.listar_piezas_por_color(color_propio)
        piezas_oponente = self._tablero.listar_piezas_por_color(color_oponente)

        valor_propio = 0
        for pieza_propia in piezas_propias:
            valor_propio += pieza_propia.valor_relativo

        valor_oponente = 0
        for pieza_oponente in piezas_oponente:
            valor_oponente += pieza_oponente.valor_relativo
        
        return float(valor_propio - valor_oponente)

    def evaluar_movilidad(self) -> float:
        """
        Calcula la movilidad neta normalizada para el color evaluado.
        """
        movimientos_propios = self._contar_movimientos(self._color)
        color_oponente = Color.BLANCA if self._color == Color.NEGRA else Color.NEGRA
        movimientos_oponente = self._contar_movimientos(color_oponente)

        movilidad_maxima = float(self._pesos.get("max_movilidad", 40.0))
        # Arregla el bug de un 0 y posible bucle infinito
        if movilidad_maxima == 0.0:
            movilidad_maxima = 1.0
        movilidad_neta = (movimientos_propios - movimientos_oponente) / movilidad_maxima
        return float(movilidad_neta)
    
    def evaluar_estructura_peones(self) -> float:
        """
        Evalúa la estructura de peones para el color evaluado.
        """
        peso = float(self._pesos.get("estructura_peones", 0.2))

        color_propio = self._color
        color_oponente = Color.BLANCA if color_propio == Color.NEGRA else Color.NEGRA

        # Obtener diccionarios columna -> [filas]
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
            - cantidad_peones_aislados_propios * penalizacion_aislado
        )
        return float(puntuacion_unidades * peso)
    
    def evaluar_seguridad_rey(self) -> float:
        """
        Evalua la seguridad del rey para el color evaluado. Devuelve un valor positivo si la seguridad es
        favorable para el color y negativo si está en peligro.
        """
        peso = float(self._pesos.get("seguridad_rey", 0.5))
        dim = self._tablero.DIM_TABLERO

        # Buscar la posición del rey
        pos_rey = self._tablero.buscar_rey(self._color)
        # Si no existe la posicion devuelve 0
        if pos_rey is None:
            return 0.0
        
        # Normaliza las coordenadas del rey
        fila_rey, columna_rey = int(pos_rey[0]), int(pos_rey[1])

        # Penalización por exposición en el centro del tablero
        penalizacion_central = 0.5 if (2 <= fila_rey <= dim - 3 and 2 <= columna_rey <= dim - 3) else 0.0

        # Casillas críticas: casillas del rey + adyacentes
        casillas_criticas = self._casillas_criticas_rey(pos_rey, dim)

        # Shields: peones propios adyacentes que protegen al rey
        shields_contador = self._contar_shields(pos_rey, casillas_criticas)
        shield_bonus = shields_contador * 0.25  # Cada peón escudo aporta este bono

        # Atacantes enemigos a las casillas críticas
        color_oponente = Color.BLANCA if self._color == Color.NEGRA else Color.NEGRA
        contador_atacante = self._contar_atacantes_casillas(casillas_criticas, color_oponente)
        penalizacion_atacante = contador_atacante * 0.6

        # Combinar factores
        puntuacion = shield_bonus - penalizacion_atacante - penalizacion_central

        # Devuelve la puntuación normalizada
        return float(puntuacion * peso)
    
    def evaluar_control_centro(self) -> float:
        """
        Evalúa el control del centro (las 4 casillas centrales: d4, e4, c5 y e5 en un tablero estándar)
        para el color evaluado.
        Devuelve un valor positivo si el control favorece al color evaluado.
        """
        peso = float(self._pesos.get("control_centro", 0.1))
        dim = self._tablero.DIM_TABLERO

        centros = self._centros_tablero(dim)
        if not centros:
            return 0.0
        
        color_propio = self._color
        color_oponente = Color.BLANCA if self._color == Color.NEGRA else Color.NEGRA

        control_propio = sum(1 for casilla in centros if self._casilla_controlada_por(casilla, color_propio))
        control_oponente = sum(1 for casilla in centros if self._casilla_controlada_por(casilla, color_oponente))

        # Normalizar por número de casillas centrales y escalar por peso
        puntuacion = (control_propio - control_oponente) / float(len(centros))
        return puntuacion * peso

        
    def _centros_tablero(self, dim: int) -> list:
        """
        Devuelve la lista de coordenadas que se consideran centrales en un tablero de dimension genérica.
        - dim par: devuelve el bloque 2x2 central.
        - dim impar: devuelve la 3x3 centrada.
        """
        # Comprueba que la dimension es positiva para continuar
        if dim <= 0:
            return []
        
        mid = dim // 2
        if dim % 2 == 0:
            # 2x2 casillas centrales
            return [(mid - 1, mid - 1), (mid - 1, mid), (mid, mid - 1), (mid, mid)]
        else:
            # 3x3 casillas alrededor del centro
            offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
            centros = []
            for dr, dc in offsets:
                fila, columna = mid + dr, mid + dc
                if 0 <= fila < dim and 0 <= columna < dim:
                    centros.append((fila, columna))
            return centros
    
    def _casilla_controlada_por(self, casilla: tuple[int, int], color: Color) -> bool:
        """
        Devuelve True si la casila está ocupada por el color a evaluar o si alguna pieza del color 
        a evaluar puede legalmente mover/atacar allí.
        """
        fila, columna = casilla
        # Validación de los límites
        dim = self._tablero.DIM_TABLERO
        if not (0 <= fila < dim and 0 <= columna < dim):
            return False
        
        ocupante: Pieza = self._tablero.matriz_piezas[fila][columna]
        if ocupante is not None and ocupante.color == color:
            return True
        
        # Comprobar si alguna pieza del color puede mover a la casilla
        for pieza in self._tablero.listar_piezas_por_color(color):
            try:
                if self._reglas.es_movimiento_legal(pieza, array('i', [fila, columna])):
                    return True
            # Ignorar comprobaciones que fallen y continuar con otras piezas
            except IndexError:
                continue

        return False

    def _contar_movimientos(self, color: Color) -> int:
        """
        Cuenta cuántos movimientos legales del color dado hay.
        """
        generador = Generador_movimientos(self._tablero, self._reglas, color)
        return generador.contar_movimientos_legales()
    
    def _contar_shields(self, posicion_rey: tuple[int, int], casillas_criticas: list) -> int:
        """
        Cuenta peones propios en las casillas adyacentes al rey (excluyendo la casilla del rey).
        """
        shield = 0          # Contador de peones escudo
        # Comprueba si la posicion del rey existe
        if posicion_rey is None:
            return shield
        rey_pos = (int(posicion_rey[0]), int(posicion_rey[1]))
        
        for casilla in casillas_criticas:
            fila, columna = int(casilla[0]), int(casilla[1])
            # Excluye la casilla del rey
            if (fila, columna) == rey_pos:
                continue
            # Accede solo a los peones propios 
            pieza: Peon = self._tablero.matriz_piezas[fila][columna]
            if pieza is not None and isinstance(pieza, Peon) and pieza.color == self._color:
                shield += 1
        
        return shield
    
    def _contar_atacantes_casillas(self, casillas_criticas: list, color_oponente: Color) -> int:
        """
        Cuenta atacantes únicos del conjunto de casillas críticas por parte del color oponente.
        """
        atacantes = set()
        piezas_enemigas = self._tablero.listar_piezas_por_color(color_oponente)
        for pieza in piezas_enemigas:
            for destino in casillas_criticas:
                try:
                    if self._reglas.es_movimiento_legal(pieza, destino):
                        atacantes.add(id(pieza))  # identificar pieza por id
                        break
                # Si reglas falla para una comprobación concreta, ignorarla y continuar
                except Exception:
                    continue
        return len(atacantes)

    def _casillas_criticas_rey(self, posicion_rey: tuple[int, int], dim: int) ->list:
        """
        Devuelve la lista de casillas críticas (casillas de rey + adyacentes) como arrays.
        """
        vecinos = [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]
        casillas: list = []

        # Comprueba sila posicion del rey existe
        if posicion_rey is None:
            return casillas
        
        fila_rey, columna_rey = int(posicion_rey[0]), int (posicion_rey[1])
        for coordenada_fila, coordenada_columna in vecinos:
            fila, columna = fila_rey + coordenada_fila, columna_rey + coordenada_columna
            if (0 <= fila < dim and 0 <= columna < dim):
                casillas.append(array('i', [fila, columna]))
        
        return casillas
    
    def _peones_por_columna(self, color: Color) -> dict:
        columnas: dict[int, list[int]] = {}
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
        for columna, filas in columnas_propias.items():
            # Si no hay peones en las columnas adyacentes, todos los peones de la columna se consideran aislados
            if ((columna - 1) not in columnas_propias) and ((columna + 1) not in columnas_propias):
                aislados += len(filas)
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
        for columna, filas in columnas_propias.items():
            for fila in filas:
                delante_enemigos = False
                # Comprobar columnas propia y adyacentes
                for col in (columna - 1, columna, columna + 1):
                    # Si está fuera del tablero, saltar
                    if col < 0 or col >= dim:
                        continue
                    filas_oponente = columnas_oponente.get(col, [])
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