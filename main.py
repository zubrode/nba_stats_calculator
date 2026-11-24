def calcular_ts(puntos, fga, fta):
    """Calcula el True Shooting Percentage (TS%) de un jugador."""
    posesiones_tiro = fga + 0.44 * fta
    if posesiones_tiro == 0:
        return 0.0  # Evitar división por cero si el jugador no ha lanzado tiros
    
    ts_porcentaje = (puntos / (2 * posesiones_tiro)) * 100
    return round(ts_porcentaje, 2)

# 2. Mensaje de bienvenida
print("=== CALCULADORA NBA v1.0 ===")
print("Bienvenido a la calculadora de estadísticas de la NBA!")

while True:
    # 3. Entrada de datos
    try:  # Uso de try-except para manejar errores de entrada
        jugador = input("\nNombre del jugador: ")
        puntos = float(input("Puntos anotados por partido: "))
        fga = float(input("Tiros de campo intentados (FGA): "))
        fta = float(input("Tiros libres intentados (FTA): "))

        # 4. Cálculo del True Shooting (TS%)
        ts_redondeado = calcular_ts(puntos, fga, fta)

        # 5. Resultados y evaluación
        print(f"Has introducido a {jugador} con {puntos} pts, {fga} FGA y {fta} FTA.")
        print(f"\n--- Informe de {jugador} ---")
        print(f"True Shooting Percentage (TS%): {ts_redondeado}%")

        if ts_redondeado >= 60:
            print("Veredicto: Eficiencia de élite (nivel All-Star / MVP).")
        elif ts_redondeado >= 57.5:
            print("Veredicto: Muy eficiente, por encima de la media de la NBA.")
        elif ts_redondeado >= 45:
            print("Veredicto: Mala temporada, eficiencia por debajo de la media de la NBA.")
        else:
            print("Veredicto: Mejor probar con otro deporte.")

    except ValueError:
        print("\nError: Por favor, introduce valores numéricos válidos para puntos, FGA y FTA. Utilice un punto (.) como separador decimal si es necesario.")

    # Preguntamos si quiere continuar
    while True:
        continuar = input("\n¿Quieres analizar otro jugador? (s/n): ").strip().lower()
        if continuar in ("s", "n"):
            break
        print("Por favor, introduce 's' para sí o 'n' para no.")

    if continuar == "n":
        print("¡Hasta la próxima!")
        break