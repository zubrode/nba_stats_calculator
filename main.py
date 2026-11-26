from datetime import datetime
from api_client import obtener_stats_nba, obtener_medias_nba
from metrics import CATALOGO_STATS, obtener_metricas_avanzadas, obtener_veredicto_analisis


def obtener_temporada_actual():
    """Deduce la temporada NBA vigente (ej. '2026-27') a partir de la fecha del sistema."""
    hoy = datetime.now()
    anio_inicio = hoy.year if hoy.month >= 10 else hoy.year - 1
    anio_fin = str(anio_inicio + 1)[-2:]
    return f"{anio_inicio}-{anio_fin}"


def obtener_perfil_completo(datos):
    """Combina el Box Score base y las métricas avanzadas en un solo diccionario."""
    avanzadas = obtener_metricas_avanzadas(datos)
    perfil = dict(datos)
    perfil["pra"] = round(datos["puntos"] + datos["rebotes"] + datos["asistencias"], 1)
    perfil.update(avanzadas)
    return perfil


TEMPORADA_ACTUAL = obtener_temporada_actual()

print("=== NBA STATS EXPLORER v3.0 ===")
print("Bienvenido al analizador de estadísticas de la NBA!")

while True:
    print("\nModos disponibles:")
    print("1. Búsqueda de jugador (Box Score + Métricas Avanzadas)")
    print("2. Análisis comparativo (Jugador vs. Media de la NBA)")
    modo = input("Elige una opción (1/2): ").strip()

    if modo == "1":
        nombre_input = input("\nNombre del jugador a buscar: ").strip()
        if not nombre_input:
            print("Por favor, introduce el nombre de un jugador.")
            continue

        datos = obtener_stats_nba(nombre_input, elegir_temporada=True)
        if datos is None:
            continue

        perfil = obtener_perfil_completo(datos)
        titulo = f"{perfil['nombre']} ({perfil['temporada']} - {perfil['equipo']})"

        print(f"\n================ INFORME DE {titulo.upper()} ================")
        print(f"Partidos jugados: {perfil['gp']} GP | Minutos: {perfil['min']} MIN")

        print("\n[ BOX SCORE BASE ]")
        print(f"  PTS: {perfil['puntos']}  |  REB: {perfil['rebotes']}  |  AST: {perfil['asistencias']}  |  PRA: {perfil['pra']}")
        print(f"  STL: {perfil['robos']}  |  BLK: {perfil['tapones']}  |  TOV: {perfil['perdidas']}  |  PF: {perfil['faltas']}")
        print(f"  Tiros: {perfil['fgm']}/{perfil['fga']} FG | {perfil['fg3m']}/{perfil['fg3a']} 3PT | {perfil['ftm']}/{perfil['fta']} FT")

        print("\n[ MÉTRICAS AVANZADAS ]")
        print(f"  TS%: {perfil['ts']}%  |  eFG%: {perfil['efg']}%  |  FTr: {perfil['ftr']}")
        print(f"  AST/TOV: {perfil['ast_tov']}  |  Game Score (GmSc): {perfil['gmsc']}")
        print("=" * 64)

    elif modo == "2":
        nombre_input = input("\nNombre del jugador a analizar: ").strip()
        if not nombre_input:
            print("Por favor, introduce el nombre de un jugador.")
            continue

        datos = obtener_stats_nba(nombre_input, elegir_temporada=True)
        if datos is None:
            continue

        perfil = obtener_perfil_completo(datos)
        temp_jugador = perfil["temporada"]
        comparando_con_actual = False

        if temp_jugador != TEMPORADA_ACTUAL:
            print(f"\nHas seleccionado la temporada {temp_jugador} de {perfil['nombre']}.")
            print(f"1. Comparar contra la media de la NBA en {temp_jugador} (misma época)")
            print(f"2. Comparar contra la media de la NBA actual ({TEMPORADA_ACTUAL})")

            while True:
                ref = input("Elige referencia (1/2): ").strip()
                if ref in ("1", "2"):
                    break
                print("Opción no válida. Elige '1' o '2'.")

            if ref == "1":
                medias_nba = obtener_medias_nba(temporada=temp_jugador)
                if medias_nba is None:
                    print(f"Usando la temporada actual ({TEMPORADA_ACTUAL}) como referencia alternativa...")
                    medias_nba = obtener_medias_nba(temporada=None)
                    comparando_con_actual = True
            else:
                medias_nba = obtener_medias_nba(temporada=None)
                comparando_con_actual = True
        else:
            medias_nba = obtener_medias_nba(temporada=None)

        if medias_nba is None:
            continue

        # Bucle para evaluar múltiples estadísticas del mismo jugador sin repetir la búsqueda
        while True:
            print(f"\n¿Qué estadística de {perfil['nombre']} ({temp_jugador}) quieres comparar?")
            for clave, (_, etiqueta, _) in CATALOGO_STATS.items():
                print(f"  {clave}. {etiqueta}")

            while True:
                eleccion = input("Elige el número de la estadística: ").strip()
                if eleccion in CATALOGO_STATS:
                    break
                print("Opción de estadística no válida.")

            campo, nombre_stat, unidad = CATALOGO_STATS[eleccion]
            valor_jugador = perfil[campo]
            valor_nba = medias_nba[campo]
            diferencia = round(valor_jugador - valor_nba, 2)
            pct_diferencia = round((diferencia / valor_nba) * 100, 1) if valor_nba != 0 else 0.0
            signo = "+" if diferencia > 0 else ""

            veredicto = obtener_veredicto_analisis(campo, pct_diferencia)

            print(f"\n--- Análisis: {perfil['nombre']} ({temp_jugador}) en {nombre_stat} ---")
            print(f"  Valor de {perfil['nombre']}: {valor_jugador}{unidad}")
            print(f"  Media de la NBA [{medias_nba['temporada_ref']}]: {valor_nba}{unidad}")
            print(f"  Diferencia: {signo}{diferencia}{unidad} ({signo}{pct_diferencia}%)")
            print(f"  Veredicto: {veredicto}")

            if comparando_con_actual:
                print("\n  [Nota contextual]: Estás comparando una temporada histórica contra la NBA actual.")
                print("  Ten en cuenta las diferencias de ritmo de juego (pace), volumen de triples y reglas")
                print("  entre épocas al interpretar promedios absolutos y eficiencia.")

            while True:
                otra_stat = input(f"\n¿Quieres analizar otra estadística de {perfil['nombre']}? (s/n): ").strip().lower()
                if otra_stat in ("s", "n"):
                    break
                print("Por favor, introduce 's' para sí o 'n' para no.")

            if otra_stat == "n":
                break

    else:
        print("\nOpción no válida. Por favor, elige '1' o '2'.")
        continue

    while True:
        continuar = input("\n¿Quieres realizar otra consulta? (s/n): ").strip().lower()
        if continuar in ("s", "n"):
            break
        print("Por favor, introduce 's' para sí o 'n' para no.")

    if continuar == "n":
        print("¡Hasta la próxima!")
        break