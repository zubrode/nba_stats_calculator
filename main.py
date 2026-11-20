print("=== CALCULADORA NBA v0.1 ===")
print("Bienvenido a la calculadora de estadísticas de la NBA!")

# 1. Entrada de datos
jugador = input("Nombre del jugador: ")
puntos = float(input("Puntos anotados por partido: "))
tiros_campo = float(input("Tiros de campo intentados (FGA): "))
tiros_libres = float(input("Tiros libres intentados (FTA): "))

# 2. Cálculo del True Shooting (TS%)
posesiones_tiro = tiros_campo + 0.44 * tiros_libres
ts_porcentaje = (puntos / (2 * posesiones_tiro)) * 100
ts_redondeado = round(ts_porcentaje, 2)

# 3. Resultados y evaluación
print(f"Has introducido a {jugador} con {puntos} pts, {tiros_campo} FGA y {tiros_libres} FTA.")
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