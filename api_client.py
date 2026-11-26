from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, leaguedashplayerstats

# Caché en memoria indexada por temporada (ej. {"actual": {...}, "2015-16": {...}})
_CACHE_MEDIAS_NBA = {}


def obtener_stats_nba(nombre_buscado, elegir_temporada=True):
    """Busca un jugador en la NBA y devuelve su Box Score de la temporada seleccionada."""
    resultados = players.find_players_by_full_name(nombre_buscado)

    if not resultados:
        print(f"\nNo se encontró ningún jugador llamado '{nombre_buscado}'.")
        return None

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

    print(f"\nConsultando historial oficial de {jugador_elegido['full_name']}...")

    try:
        carrera = playercareerstats.PlayerCareerStats(
            player_id=jugador_elegido["id"],
            per_mode36="PerGame"
        )
        df_temporadas = carrera.get_data_frames()[0]

        if df_temporadas.empty:
            print("Este jugador no tiene estadísticas registradas en la base de datos de la NBA.")
            return None

        if elegir_temporada and len(df_temporadas) > 1:
            df_temporadas = df_temporadas.reset_index(drop=True)
            print(f"\nTemporadas disponibles para {jugador_elegido['full_name']}:")
            for idx, fila in df_temporadas.iterrows():
                print(f"  {idx + 1}. {fila['SEASON_ID']} ({fila['TEAM_ABBREVIATION']}) - {int(fila['GP'])} GP")

            while True:
                eleccion = input(f"Elige temporada (1-{len(df_temporadas)}) o pulsa Enter para la última: ").strip()
                if eleccion == "":
                    seleccionada = df_temporadas.iloc[-1]
                    break
                try:
                    num = int(eleccion)
                    if 1 <= num <= len(df_temporadas):
                        seleccionada = df_temporadas.iloc[num - 1]
                        break
                    print(f"Por favor, introduce un número entre 1 y {len(df_temporadas)}.")
                except ValueError:
                    print("Error: Introduce un número válido o pulsa Enter.")
        else:
            seleccionada = df_temporadas.iloc[-1]

        return {
            "nombre": jugador_elegido["full_name"],
            "temporada": seleccionada["SEASON_ID"],
            "equipo": seleccionada["TEAM_ABBREVIATION"],
            "gp": int(seleccionada["GP"]),
            "min": float(seleccionada["MIN"]),
            "puntos": float(seleccionada["PTS"]),
            "rebotes": float(seleccionada["REB"]),
            "oreb": float(seleccionada["OREB"]),
            "dreb": float(seleccionada["DREB"]),
            "asistencias": float(seleccionada["AST"]),
            "robos": float(seleccionada["STL"]),
            "tapones": float(seleccionada["BLK"]),
            "perdidas": float(seleccionada["TOV"]),
            "faltas": float(seleccionada["PF"]),
            "fgm": float(seleccionada["FGM"]),
            "fga": float(seleccionada["FGA"]),
            "fg3m": float(seleccionada["FG3M"]),
            "fg3a": float(seleccionada["FG3A"]),
            "ftm": float(seleccionada["FTM"]),
            "fta": float(seleccionada["FTA"]),
        }

    except Exception as e:
        print(f"\nError al conectar con la API de la NBA: {e}")
        return None


def obtener_medias_nba(temporada=None):
    """Descarga los promedios de la NBA para una temporada dada (o la actual si es None)."""
    clave_cache = temporada if temporada else "actual"

    if clave_cache in _CACHE_MEDIAS_NBA:
        return _CACHE_MEDIAS_NBA[clave_cache]

    etiqueta = temporada if temporada else "actual"
    print(f"\nCalculando medias de la NBA para la temporada {etiqueta} (jugadores de rotación)...")

    try:
        if temporada:
            liga = leaguedashplayerstats.LeagueDashPlayerStats(
                season=temporada,
                per_mode_detailed="PerGame"
            )
        else:
            liga = leaguedashplayerstats.LeagueDashPlayerStats(
                per_mode_detailed="PerGame"
            )

        df = liga.get_data_frames()[0]

        if df.empty:
            print(f"\nAviso: La API oficial de la NBA no dispone de medias por jugador para {temporada} (disponibles desde 1996-97).")
            return None

        df_rotacion = df[(df["GP"] >= 10) & (df["MIN"] >= 10.0)].copy()

        if df_rotacion.empty:
            df_rotacion = df[df["MIN"] >= 10.0].copy()

        fga_seguro = df_rotacion["FGA"].replace(0, float("nan"))
        posesiones_tiro = (df_rotacion["FGA"] + 0.44 * df_rotacion["FTA"]).replace(0, float("nan"))

        df_rotacion["TS"] = (df_rotacion["PTS"] / (2 * posesiones_tiro)) * 100
        df_rotacion["EFG"] = ((df_rotacion["FGM"] + 0.5 * df_rotacion["FG3M"]) / fga_seguro) * 100
        df_rotacion["FTR"] = df_rotacion["FTA"] / fga_seguro
        df_rotacion["AST_TOV"] = df_rotacion["AST"] / df_rotacion["TOV"].replace(0, 1)
        df_rotacion["PRA"] = df_rotacion["PTS"] + df_rotacion["REB"] + df_rotacion["AST"]
        df_rotacion["GMSC"] = (
            df_rotacion["PTS"]
            + 0.4 * df_rotacion["FGM"]
            - 0.7 * df_rotacion["FGA"]
            - 0.4 * (df_rotacion["FTA"] - df_rotacion["FTM"])
            + 0.7 * df_rotacion["OREB"]
            + 0.3 * df_rotacion["DREB"]
            + df_rotacion["STL"]
            + 0.7 * df_rotacion["AST"]
            + 0.7 * df_rotacion["BLK"]
            - 0.4 * df_rotacion["PF"]
            - df_rotacion["TOV"]
        )

        medias = {
            "temporada_ref": temporada if temporada else "actual (2026-27)",
            "puntos": round(float(df_rotacion["PTS"].mean()), 2),
            "rebotes": round(float(df_rotacion["REB"].mean()), 2),
            "asistencias": round(float(df_rotacion["AST"].mean()), 2),
            "robos": round(float(df_rotacion["STL"].mean()), 2),
            "tapones": round(float(df_rotacion["BLK"].mean()), 2),
            "perdidas": round(float(df_rotacion["TOV"].mean()), 2),
            "pra": round(float(df_rotacion["PRA"].mean()), 2),
            "ts": round(float(df_rotacion["TS"].mean()), 2),
            "efg": round(float(df_rotacion["EFG"].mean()), 2),
            "ftr": round(float(df_rotacion["FTR"].mean()), 2),
            "ast_tov": round(float(df_rotacion["AST_TOV"].mean()), 2),
            "gmsc": round(float(df_rotacion["GMSC"].mean()), 2),
        }

        _CACHE_MEDIAS_NBA[clave_cache] = medias
        return medias

    except Exception as e:
        print(f"\nError al obtener las medias de la NBA: {e}")
        return None