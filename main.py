from datetime import datetime
from api_client import obtener_stats_nba, obtener_medias_nba
from metrics import (
    CATALOGO_STATS,
    comparar_jugadores,
    obtener_metricas_avanzadas,
    obtener_veredicto_analisis,
)


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


def pedir_perfil_jugador(prompt_texto):
    """Solicita el nombre de un jugador, lo busca en la API y devuelve su perfil completo."""
    nombre_input = input(prompt_texto).strip()
    if not nombre_input:
        print("Por favor, introduce el nombre de un jugador.")
        return None

    datos = obtener_stats_nba(nombre_input, elegir_temporada=True)
    if datos is None:
        return None

    return obtener_perfil_completo(datos)


def confirmar_accion(pregunta):
    """Pide una confirmación 's' o 'n' al usuario y devuelve True o False."""
    while True:
        resp = input(pregunta).strip().lower()
        if resp in ("s", "n"):
            return resp == "s"
        print("Por favor, introduce 's' para sí o 'n' para no.")


TEMPORADA_ACTUAL = obtener_temporada_actual()

print("=== NBA STATS EXPLORER v3.1 ===")
print("Bienvenido al analizador de estadísticas de la NBA!")

while True:
    print("\nModos disponibles:")
    print("1. Búsqueda de jugador (Box Score + Métricas Avanzadas)")
    print("2. Análisis comparativo (Jugador vs. Media de la NBA)")
    print("3. Comparador 1 vs 1 (Duelo directo entre dos jugadores/temporadas)")
    modo = input("Elige una opción (1/2/3): ").strip()

    if modo == "1":
        perfil = pedir_perfil_jugador("\nNombre del jugador a buscar: ")
        if perfil is None:
            continue

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
        perfil = pedir_perfil_jugador("\nNombre del jugador a analizar: ")
        if perfil is None:
            continue

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

            if not confirmar_accion(f"\n¿Quieres analizar otra estadística de {perfil['nombre']}? (s/n): "):
                break

    elif modo == "3":
        perfil_1 = pedir_perfil_jugador("\nNombre del Jugador 1: ")
        if perfil_1 is None:
            continue

        perfil_2 = pedir_perfil_jugador("\nNombre del Jugador 2: ")
        if perfil_2 is None:
            continue

        etiqueta_1 = f"{perfil_1['nombre']} ({perfil_1['temporada']})"
        etiqueta_2 = f"{perfil_2['nombre']} ({perfil_2['temporada']})"

        # Usamos etiquetas con temporada en los perfiles para distinguir duelos del mismo jugador
        p1_etiquetado = dict(perfil_1, nombre=etiqueta_1)
        p2_etiquetado = dict(perfil_2, nombre=etiqueta_2)

        duelo = comparar_jugadores(p1_etiquetado, p2_etiquetado)

        print("\n" + "=" * 96)
        print(f"DUELO 1 VS 1: {etiqueta_1.upper()}  VS  {etiqueta_2.upper()}")
        print(f"Contexto: {perfil_1['gp']} GP ({perfil_1['min']} MIN)  vs  {perfil_2['gp']} GP ({perfil_2['min']} MIN)")
        print("=" * 96)
        print(f"{'ESTADÍSTICA':<42} | {'JUGADOR 1':^12} | {'JUGADOR 2':^12} | {'GANADOR'}")
        print("-" * 96)

        for fila in duelo["filas"]:
            v1_str = f"{fila['val_1']}{fila['unidad']}"
            v2_str = f"{fila['val_2']}{fila['unidad']}"
            print(f"{fila['etiqueta']:<42} | {v1_str:^12} | {v2_str:^12} | {fila['ganador']}")

        print("=" * 96)
        print(
            f"MARCADOR FINAL: {etiqueta_1} [{duelo['victorias_1']}] - "
            f"[{duelo['victorias_2']}] {etiqueta_2} (Empates: {duelo['empates']})"
        )
        print("=" * 96)

        if perfil_1["temporada"] != perfil_2["temporada"]:
            print("\n  [Nota contextual]: Estás comparando temporadas de distintos años.")
            print("  Ten en cuenta las diferencias de ritmo de juego (pace) y reglas entre épocas.")

    else:
        print("\nOpción no válida. Por favor, elige '1', '2' o '3'.")
        continue

    if not confirmar_accion("\n¿Quieres realizar otra consulta? (s/n): "):
        print("¡Hasta la próxima!")
        break