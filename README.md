# Motor de Ajedrez con Aprendizaje por Refuerzo

Este proyecto consiste en el desarrollo de un motor de ajedrez utilizando técnicas de aprendizaje por refuerzo. El objetivo es crear un agente inteligente capaz de jugar al ajedrez a un nivel competitivo frente a jugadores humanos.

## Estructura del Proyecto

```
chess-rl-engine
├── src
│   ├── engine
│   │   ├── color.py                    # Enum de color: BLANCA y NEGRA
│   │   ├── evaluador.py                # Evaluador de posiciones del tablero
│   │   ├── generador_movimiento.py     # Generador de movimientos legales
│   │   ├── main_engine.py              # Main del motor
│   │   ├── piezas                      # Carpeta que aloja las clases de las piezas
│   │   ├── reglas.py                   # Clase que aloja las reglas del ajedrez
│   │   └── tablero.py                  # Clase que representa el tablero de ajedrez
│   ├── rl
│   │   ├── agente.py                   # Implementación del agente de aprendizaje por refuerzo
│   │   ├── entrenamiento.py            # Bucle de entrenamiento del agente
│   │   ├── experiencias_buffer.py      # Memoria de experiencias
│   │   └── main_agent.py               # Main del agente
│   ├── utils           
│   │   ├── config.py                   # Gestión de configuración
│   │   ├── logger.py                   # Utilidad para registro de eventos y métricas
│   │   └── main_utils.py               # Main de las utilidades
│   ├── main.py                         # Punto de entrada de la aplicación
│   └── tipos           
│       └── index.py                    # Tipos y constantes usados en el proyecto
├── tests           
│   ├── test_engine.py                  # Pruebas unitarias del módulo engine
│   ├── test_rl.py                      # Pruebas unitarias del módulo de aprendizaje por 
│   └── test_utils.py                   # Pruebas unitarias de utilidades
├── requirements.txt                    # Dependencias del proyecto
├── setup.py                            # Configuración de empaquetado
└── README.md                           # Documentación del proyecto
```

## Instalación

Para instalar el proyecto, clona el repositorio e instala las dependencias necesarias:

```bash
git clone https://github.com/alx5409/Motor-de-ajedrez-RL.git
cd chess-rl-engine
pip install -r requirements.txt
```

## Uso

Para iniciar el proceso de entrenamiento del agente, ejecuta el siguiente comando:

```bash
python src/main.py
```

## Contribuciones

¡Las contribuciones son bienvenidas! Puedes enviar un pull request o abrir un issue con sugerencias o mejoras.

## Licencia

Este proyecto está bajo licencia MIT. Consulta el archivo LICENSE para más información.