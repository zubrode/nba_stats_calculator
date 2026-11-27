CATALOGO_STATS = {
    "1": ("puntos", "Puntos por partido (PTS)", ""),
    "2": ("rebotes", "Rebotes por partido (REB)", ""),
    "3": ("asistencias", "Asistencias por partido (AST)", ""),
    "4": ("robos", "Robos por partido (STL)", ""),
    "5": ("tapones", "Tapones por partido (BLK)", ""),
    "6": ("pra", "Puntos + Rebotes + Asistencias (PRA)", ""),
    "7": ("ts", "True Shooting Percentage (TS%)", "%"),
    "8": ("efg", "Effective Field Goal Percentage (eFG%)", "%"),
    "9": ("ftr", "Free Throw Rate (FTr)", ""),
    "10": ("ast_tov", "Ratio Asistencias / Pérdidas (AST/TOV)", ""),
    "11": ("gmsc", "Game Score promedio (GmSc)", ""),
}


def calcular_ts(puntos, fga, fta):
    """Calcula el True Shooting Percentage (TS%)."""
    posesiones_tiro = fga + 0.44 * fta
    if posesiones_tiro == 0:
        return 0.0
    return round((puntos / (2 * posesiones_tiro)) * 100, 2)


def calcular_efg(fgm, fg3m, fga):
    """Calcula el Effective Field Goal Percentage (eFG%)."""
    if fga == 0:
        return 0.0
    return round(((fgm + 0.5 * fg3m) / fga) * 100, 2)


def calcular_ftr(fta, fga):
    """Calcula el Free Throw Rate (FTr = FTA / FGA)."""
    if fga == 0:
        return 0.0
    return round(fta / fga, 2)


def calcular_ast_tov(asistencias, perdidas):
    """Calcula el ratio Asistencias / Pérdidas (AST/TOV)."""
    if perdidas == 0:
        return round(asistencias, 2)
    return round(asistencias / perdidas, 2)


def calcular_game_score(datos):
    """Calcula el Game Score promedio de John Hollinger."""
    gmsc = (
        datos["puntos"]
        + 0.4 * datos["fgm"]
        - 0.7 * datos["fga"]
        - 0.4 * (datos["fta"] - datos["ftm"])
        + 0.7 * datos["oreb"]
        + 0.3 * datos["dreb"]
        + datos["robos"]
        + 0.7 * datos["asistencias"]
        + 0.7 * datos["tapones"]
        - 0.4 * datos["faltas"]
        - datos["perdidas"]
    )
    return round(gmsc, 1)


def obtener_metricas_avanzadas(datos):
    """Calcula y agrupa todas las métricas avanzadas a partir del Box Score."""
    return {
        "ts": calcular_ts(datos["puntos"], datos["fga"], datos["fta"]),
        "efg": calcular_efg(datos["fgm"], datos["fg3m"], datos["fga"]),
        "ftr": calcular_ftr(datos["fta"], datos["fga"]),
        "ast_tov": calcular_ast_tov(datos["asistencias"], datos["perdidas"]),
        "gmsc": calcular_game_score(datos),
    }


def obtener_veredicto_analisis(campo, pct_diferencia):
    """Clasifica el rendimiento relativo del jugador en 5 niveles según el tipo de estadística."""
    if campo in ("ts", "efg"):
        if pct_diferencia >= 8.0:
            return "Élite en esta categoría estadística."
        elif pct_diferencia >= 2.5:
            return "Por encima de la media NBA."
        elif pct_diferencia >= -2.5:
            return "Alrededor de la media NBA."
        elif pct_diferencia >= -8.0:
            return "Por debajo de la media NBA."
        else:
            return "No es su fuerte."
    else:
        if pct_diferencia >= 40.0:
            return "Élite en esta categoría estadística."
        elif pct_diferencia >= 10.0:
            return "Por encima de la media NBA."
        elif pct_diferencia >= -10.0:
            return "Alrededor de la media NBA."
        elif pct_diferencia >= -35.0:
            return "Por debajo de la media NBA."
        else:
            return "No es su fuerte."
        

STATS_INVERSAS = ("perdidas", "faltas")

def comparar_jugadores(perfil_1, perfil_2):
    """Compara dos perfiles completos en todas las estadísticas del catálogo y devuelve resultados y marcador."""
    resultados = []
    victorias_1 = 0
    victorias_2 = 0
    empates = 0

    for _, (campo, etiqueta, unidad) in CATALOGO_STATS.items():
        val_1 = perfil_1[campo]
        val_2 = perfil_2[campo]
        diferencia = round(abs(val_1 - val_2), 2)

        # En pérdidas o faltas gana el valor más bajo
        if campo in STATS_INVERSAS:
            gana_1 = val_1 < val_2
            gana_2 = val_2 < val_1
        else:
            gana_1 = val_1 > val_2
            gana_2 = val_2 > val_1

        if gana_1:
            ganador = perfil_1["nombre"]
            victorias_1 += 1
        elif gana_2:
            ganador = perfil_2["nombre"]
            victorias_2 += 1
        else:
            ganador = "Empate"
            empates += 1

        resultados.append({
            "etiqueta": etiqueta,
            "unidad": unidad,
            "val_1": val_1,
            "val_2": val_2,
            "diferencia": diferencia,
            "ganador": ganador,
        })

    return {
        "filas": resultados,
        "victorias_1": victorias_1,
        "victorias_2": victorias_2,
        "empates": empates,
    }