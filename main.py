from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

def calcular_ts(puntos, fga, fta):
    """Calcula el True Shooting Percentage (TS%) de un jugador."""
    posesiones_tiro = fga + 0.44 * fta
    if posesiones_tiro == 0:
        return 0.0  # Evitar división por cero si el jugador no ha lanzado tiros
    
    ts_porcentaje = (puntos / (2 * posesiones_tiro)) * 100
    return round(ts_porcentaje, 2)

def obtener_stats_nba(nombre_buscado):
    """Busca un jugador en la NBA y devuelve sus promedios de su última temporada."""
    resultados = players.find_players_by_full_name(nombre_buscado)

    if not resultados:
        print(f"\nNo se encontró ningún jugador llamado '{nombre_buscado}'.")
        return None

    # Priorizar jugadores activos y limitar a las 5 mejores coincidencias
    resultados_ordenados = sorted(resultados, key=lambda x: x["is_active"], reverse=True)[:5]

    if len(resultados_ordenados) == 1:
        jugador_elegido = resultados_ordenados[0]
    else:
        print("\nSe encontraron varios jugadores:")
        for i, p in enumerate(resultados_ordenados, start=1):
            estado = "Activo" if p["is_active"] else "Retirado"
            print(f"{i}. {p['full_name']} ({estado})")

        while True:
            try:
                opcion = int(input("Elige el número del jugador (0 para cancelar): "))
                if opcion == 0:
                    return None
                if 1 <= opcion <= len(resultados_ordenados):
                    jugador_elegido = resultados_ordenados[opcion - 1]
                    break
                print(f"Por favor, introduce un número entre 0 y {len(resultados_ordenados)}.")
            except ValueError:
                print("Error: Introduce un número válido.")

    print(f"\nConsultando estadísticas oficiales de {jugador_elegido['full_name']}...")

    try:
        carrera = playercareerstats.PlayerCareerStats(
            player_id=jugador_elegido["id"],
            per_mode36="PerGame"
        )
        df_temporadas = carrera.get_data_frames()[0]

        if df_temporadas.empty:
            print("Este jugador aún no tiene estadísticas registradas en la NBA.")
            return None

        ultima_temporada = df_temporadas.iloc[-1]

        return {
            "nombre": jugador_elegido["full_name"],
            "temporada": ultima_temporada["SEASON_ID"],
            "equipo": ultima_temporada["TEAM_ABBREVIATION"],
            "puntos": float(ultima_temporada["PTS"]),
            "fga": float(ultima_temporada["FGA"]),
            "fta": float(ultima_temporada["FTA"]),
        }

    except Exception as e:
        print(f"\nError al conectar con la API de la NBA: {e}")
        return None

# 1. Mensaje de bienvenida
print("=== CALCULADORA NBA v2.0 ===")
print("Bienvenido a la calculadora de estadísticas de la NBA!")

while True:
    # 2. Selección de modo
    print("\nModos disponibles:")
    print("1. Automático (buscar jugador real en la NBA)")
    print("2. Manual (introducir estadísticas a mano)")
    modo = input("Elige una opción (1/2): ").strip()

    if modo == "1":
        nombre_input = input("\nNombre del jugador a buscar: ").strip()
        datos = obtener_stats_nba(nombre_input)

        if datos is None:
            continue  # Vuelve al inicio si no se encontró o hubo error

        jugador = f"{datos['nombre']} ({datos['temporada']} - {datos['equipo']})"
        puntos = datos["puntos"]
        fga = datos["fga"]
        fta = datos["fta"]

    elif modo == "2":
        try:
            jugador = input("\nNombre del jugador: ")
            puntos = float(input("Puntos anotados por partido: "))
            fga = float(input("Tiros de campo intentados (FGA): "))
            fta = float(input("Tiros libres intentados (FTA): "))
        except ValueError:
            print("\nError: Por favor, introduce valores numéricos válidos para puntos, FGA y FTA.")
            continue
    else:
        print("\nOpción no válida. Por favor, elige '1' o '2'.")
        continue

    # 3. Cálculo del True Shooting (TS%)
    ts_redondeado = calcular_ts(puntos, fga, fta)

    # 4. Resultados y evaluación
    print(f"Promedios registrados para {jugador} con {puntos} pts, {fga} FGA y {fta} FTA.")
    print(f"\n--- Informe de {jugador} ---")
    print(f"True Shooting Percentage (TS%): {ts_redondeado}%")

    if ts_redondeado >= 60:
        print("Veredicto: Eficiencia de élite (nivel All-Star / MVP).")
    elif ts_redondeado >= 57.5:
        print("Veredicto: Muy eficiente, por encima de la media de la NBA actual.")
    elif ts_redondeado >= 45:
        print("Veredicto: Mala temporada, eficiencia por debajo de la media de la NBA actual.")
    else:
        print("Veredicto: Mejor probar con otro deporte.")

    # Preguntamos si quiere continuar
    while True:
        continuar = input("\n¿Quieres analizar otro jugador? (s/n): ").strip().lower()
        if continuar in ("s", "n"):
            break
        print("Por favor, introduce 's' para sí o 'n' para no.")

    if continuar == "n":
        print("¡Hasta la próxima!")
        break