

import pandas as pd
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
ARCHIVO_LIMPIO = "datos/metro_limpio.csv"
CARPETA_SALIDA = "resultados_analisis_metro"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Alcaldías que conectan directamente con Edomex o reciben flujo migratorio
ZONA_NORTE_NORORIENTE = [
    "Gustavo A. Madero",    # Indios Verdes, Línea 3 y 6
    "Azcapotzalco",         # El Rosario, Línea 6 y 7
    "Venustiano Carranza",  # Línea B, Terminal Aérea
    "Estado de México",     # Estaciones Línea B y A en Edomex
    "Nezahualcóyotl (Edomex)",
]

ZONA_SUR_PONIENTE = [
    "Coyoacán",
    "Álvaro Obregón",
    "Magdalena Contreras",
    "Tláhuac",
    "Xochimilco",
]

# CARGA
print("Cargando datos limpios...")
df = pd.read_csv(ARCHIVO_LIMPIO, parse_dates=["fecha"])
print(f"  {len(df):,} registros | {df['anio'].min()}–{df['anio'].max()}")
print(f"  Alcaldías disponibles: {df['alcaldia'].nunique()}\n")

# ANÁLISIS 1 — Afluencia total por alcaldía
print("=" * 55)
print("ANÁLISIS 1: Afluencia total por alcaldía (histórico)")
print("=" * 55)

por_alcaldia = (
    df.groupby("alcaldia")["afluencia"]
    .agg(
        afluencia_total="sum",
        afluencia_promedio_diaria="mean",
        estaciones_unicas=lambda x: df.loc[x.index, "estacion"].nunique(),
        dias_con_datos="count",
    )
    .sort_values("afluencia_total", ascending=False)
    .reset_index()
)

por_alcaldia["afluencia_total_millones"] = (
    por_alcaldia["afluencia_total"] / 1_000_000
).round(2)
por_alcaldia["afluencia_promedio_diaria"] = por_alcaldia[
    "afluencia_promedio_diaria"
].round(0).astype(int)

# Marcar zona
por_alcaldia["zona"] = por_alcaldia["alcaldia"].apply(
    lambda a: "Norte/Nororiente (conexión Edomex)"
    if a in ZONA_NORTE_NORORIENTE
    else ("Sur/Poniente" if a in ZONA_SUR_PONIENTE else "Centro/Oriente")
)

print(por_alcaldia[
    ["alcaldia", "zona", "afluencia_total_millones", "afluencia_promedio_diaria", "estaciones_unicas"]
].to_string(index=False))

por_alcaldia.to_csv(f"{CARPETA_SALIDA}/01_afluencia_por_alcaldia.csv", index=False)
print(f"\n→ Guardado: {CARPETA_SALIDA}/01_afluencia_por_alcaldia.csv")


# ANÁLISIS 2 — Top 20 estaciones con más afluencia

print("\n" + "=" * 55)
print("ANÁLISIS 2: Top 20 estaciones por afluencia total")
print("=" * 55)

top_estaciones = (
    df.groupby(["estacion", "alcaldia", "linea"])["afluencia"]
    .sum()
    .reset_index()
    .sort_values("afluencia", ascending=False)
    .head(20)
    .reset_index(drop=True)
)
top_estaciones["afluencia_millones"] = (top_estaciones["afluencia"] / 1_000_000).round(2)
top_estaciones["es_norte"] = top_estaciones["alcaldia"].isin(ZONA_NORTE_NORORIENTE).map(
    {True: "⬆ Norte/Edomex", False: ""}
)

print(top_estaciones[["estacion", "linea", "alcaldia", "afluencia_millones", "es_norte"]].to_string(index=False))
top_estaciones.to_csv(f"{CARPETA_SALIDA}/02_top_estaciones.csv", index=False)
print(f"\n→ Guardado: {CARPETA_SALIDA}/02_top_estaciones.csv")


# ANÁLISIS 3 — Estaciones del Estado de México

print("\n" + "=" * 55)
print("ANÁLISIS 3: Estaciones en territorio Edomex")
print("(Evidencia directa de viajes intermunicipales)")
print("=" * 55)

edomex = df[df["alcaldia"].str.contains("México|Nezahualcóyotl", na=False)]
if len(edomex) > 0:
    est_edomex = (
        edomex.groupby(["estacion", "linea", "alcaldia"])["afluencia"]
        .agg(total="sum", promedio_diario="mean")
        .reset_index()
        .sort_values("total", ascending=False)
    )
    est_edomex["total_millones"] = (est_edomex["total"] / 1_000_000).round(2)
    est_edomex["promedio_diario"] = est_edomex["promedio_diario"].round(0).astype(int)
    print(est_edomex[["estacion", "linea", "alcaldia", "total_millones", "promedio_diario"]].to_string(index=False))
    est_edomex.to_csv(f"{CARPETA_SALIDA}/03_estaciones_edomex.csv", index=False)
    print(f"\n→ Guardado: {CARPETA_SALIDA}/03_estaciones_edomex.csv")
else:
    print("  (Sin estaciones de Edomex en el dataset — revisar mapeo)")


# ANÁLISIS 4 — Norte vs Sur por año (tendencia)

print("\n" + "=" * 55)
print("ANÁLISIS 4: Norte/Nororiente vs Sur/Poniente por año")
print("=" * 55)

df["zona"] = df["alcaldia"].apply(
    lambda a: "Norte/Nororiente"
    if a in ZONA_NORTE_NORORIENTE
    else ("Sur/Poniente" if a in ZONA_SUR_PONIENTE else "Centro/Oriente")
)

tendencia = (
    df.groupby(["anio", "zona"])["afluencia"]
    .sum()
    .reset_index()
    .pivot(index="anio", columns="zona", values="afluencia")
    .fillna(0)
    .astype(int)
)

# Ratio Norte vs Sur
if "Norte/Nororiente" in tendencia.columns and "Sur/Poniente" in tendencia.columns:
    tendencia["ratio_norte_sur"] = (
        tendencia["Norte/Nororiente"] / tendencia["Sur/Poniente"]
    ).round(2)

print(tendencia.to_string())
tendencia.to_csv(f"{CARPETA_SALIDA}/04_tendencia_norte_sur.csv")
print(f"\n→ Guardado: {CARPETA_SALIDA}/04_tendencia_norte_sur.csv")

# ANÁLISIS 5 — Patrón semanal (laboral vs fin de semana)

print("\n" + "=" * 55)
print("ANÁLISIS 5: Patrón de días laborales")
print("(Trabajadores usan más el metro entre semana)")
print("=" * 55)

df["dia_semana"] = df["fecha"].dt.dayofweek  # 0=Lunes, 6=Domingo
df["tipo_dia"] = df["dia_semana"].apply(
    lambda d: "Laboral (Lun-Vie)" if d < 5 else "Fin de semana"
)

patron_norte = (
    df[df["zona"] == "Norte/Nororiente"]
    .groupby(["tipo_dia", "dia_semana"])["afluencia"]
    .mean()
    .reset_index()
    .sort_values("dia_semana")
)
DIAS = {0:"Lunes", 1:"Martes", 2:"Miércoles", 3:"Jueves", 4:"Viernes", 5:"Sábado", 6:"Domingo"}
patron_norte["dia_nombre"] = patron_norte["dia_semana"].map(DIAS)
patron_norte["afluencia_promedio"] = patron_norte["afluencia"].round(0).astype(int)

print("  Zona Norte/Nororiente (conexión Edomex):")
print(patron_norte[["dia_nombre", "tipo_dia", "afluencia_promedio"]].to_string(index=False))
patron_norte.to_csv(f"{CARPETA_SALIDA}/05_patron_semanal_norte.csv", index=False)
print(f"\n→ Guardado: {CARPETA_SALIDA}/05_patron_semanal_norte.csv")


# ANÁLISIS 6 — Año más reciente completo (2024)

print("\n" + "=" * 55)
print("ANÁLISIS 6: Ranking de alcaldías — año 2024")
print("=" * 55)

df_2024 = df[df["anio"] == 2024]
ranking_2024 = (
    df_2024.groupby(["alcaldia", "zona"])["afluencia"]
    .sum()
    .reset_index()
    .sort_values("afluencia", ascending=False)
    .reset_index(drop=True)
)
ranking_2024.index += 1
ranking_2024["afluencia_millones"] = (ranking_2024["afluencia"] / 1_000_000).round(2)

print(ranking_2024[["alcaldia", "zona", "afluencia_millones"]].to_string())
ranking_2024.to_csv(f"{CARPETA_SALIDA}/06_ranking_2024.csv", index=False)
print(f"\n→ Guardado: {CARPETA_SALIDA}/06_ranking_2024.csv")

# ─────────────────────────────────────────────
# RESUMEN EJECUTIVO
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("RESUMEN EJECUTIVO — Hallazgos para la investigación")
print("=" * 55)

total_viajes = df["afluencia"].sum()
top1 = por_alcaldia.iloc[0]
norte_total = df[df["zona"] == "Norte/Nororiente"]["afluencia"].sum()
pct_norte = norte_total / total_viajes * 100

print(f"""
  Total de viajes registrados (2010-2025): {total_viajes/1e9:.2f} mil millones
  Alcaldía con más afluencia histórica:    {top1['alcaldia']} ({top1['afluencia_total_millones']:.0f} M viajes)
  Afluencia zona Norte/Nororiente:         {norte_total/1e9:.2f} mil millones ({pct_norte:.1f}% del total)

  Conclusión para la hipótesis:
  Las alcaldías limítrofes con el Estado de México concentran el
  {pct_norte:.0f}% de la afluencia histórica del Metro CDMX,
  lo que respalda que el flujo de trabajadores desde el Edomex
  hacia la ciudad genera una demanda desproporcionada en las
  estaciones terminales del norte y nororiente.
""")

resumen = {
    "total_viajes_historico": int(total_viajes),
    "alcaldia_top": top1["alcaldia"],
    "pct_zona_norte": round(pct_norte, 2),
    "anio_min": int(df["anio"].min()),
    "anio_max": int(df["anio"].max()),
}
pd.DataFrame([resumen]).to_csv(f"{CARPETA_SALIDA}/00_resumen.csv", index=False)
print(f"  → Todos los resultados guardados en: {CARPETA_SALIDA}/")