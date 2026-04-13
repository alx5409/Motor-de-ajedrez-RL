from engine.main_engine import main_engine, EngineResultado
from engine.color import Color

def main() -> None:
    max_turnos = 200
    mostrar = True
    semilla = 42

    resultado: EngineResultado = main_engine(max_turnos=max_turnos, mostrar=mostrar, semilla=semilla)
    print(f"Resultado final: {resultado.estado}")
    ganador: Color | None = resultado.ganador
    if ganador:
        print(f"Ganador: {ganador.name}")
    
if __name__ == "__main__":
    main()