
import pandas as pd
import unicodedata
import re
df = pd.read_csv(
    "datos/afluencia-diaria-del-metro-cdmx.csv",
    encoding="latin1",       # encoding original del archivo
    dtype={"afluencia": "Int64"}
)
print(f"  Filas cargadas: {len(df):,}")

# 2. CORRECCIÓN DE ENCODING (doble-encodificado)

def fix_encoding(text: str) -> str:
    """
    Corrige texto con doble encoding (UTF-8 codificado dos veces como latin1).
    Aplica la corrección hasta 3 veces o hasta que no queden caracteres rotos.
    """
    if not isinstance(text, str):
        return text
    for _ in range(3):
        if "Ã" not in text and "\x83" not in text:
            break
        try:
            text = text.encode("latin1").decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            break
    return text

print("Corrigiendo encoding en estaciones y líneas...")
df["estacion"] = df["estacion"].apply(fix_encoding)
df["linea"]    = df["linea"].apply(fix_encoding)

# 3. NORMALIZACIÓN DE NOMBRES

def normalizar(texto: str) -> str:
    if not isinstance(texto, str):
        return texto
    texto = unicodedata.normalize("NFC", texto)
    return texto.strip()

df["linea"]    = df["linea"].apply(normalizar)
df["estacion"] = df["estacion"].apply(normalizar)
df["mes"]      = df["mes"].apply(normalizar)
# Unificar variantes de línea: "Linea X" → "Línea X"
df["linea"] = df["linea"].str.replace(r"^Linea\s+", "Línea ", regex=True)

# Unificar variantes de estación con nombres levemente distintos
CORRECCIONES_ESTACION = {
    "Gómez Farias":                      "Gómez Farías",
    "Peñón viejo":                        "Peñón Viejo",
    "Villa de Cortés":                   "Villa de Cortés",
    "Olímpica":                          "Olímpica",
    "Miguel Ángel de Quevedo":           "Miguel Ángel de Quevedo",
}
df["estacion"] = df["estacion"].replace(CORRECCIONES_ESTACION)


# 4. TIPOS DE DATO

df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
df["anio"]  = df["fecha"].dt.year          # re-derivar del campo fecha 

# 5. MAPEO DE ESTACIÓN → ALCALDÍA
# Mapa completo de las 195 estaciones del STC Metro
# Fuente: STC Metro / SEMOVI / datos.cdmx.gob.mx
# Nota: Ciudad Azteca, Ecatepec, La Paz, Los Reyes, Impulsora,
#       Río de los Remedios, Múzquiz, Olivos, Norte 45, Calle 11
#       están en Edomex → se etiquetan como "Estado de México"
ESTACION_ALCALDIA = {
    # ── Línea 1 ──
    "Observatorio":            "Álvaro Obregón",
    "Tacubaya":                "Miguel Hidalgo",
    "Juanacatlán":             "Miguel Hidalgo",
    "Chapultepec":             "Miguel Hidalgo",
    "Sevilla":                 "Cuauhtémoc",
    "Insurgentes":             "Cuauhtémoc",
    "Cuauhtémoc":              "Cuauhtémoc",
    "Balderas":                "Cuauhtémoc",
    "Salto del Agua":          "Cuauhtémoc",
    "Isabel la Católica":      "Cuauhtémoc",
    "Pino Suárez":             "Cuauhtémoc",
    "Merced":                  "Cuauhtémoc",
    "Candelaria":              "Venustiano Carranza",
    "San Lázaro":              "Venustiano Carranza",
    "Moctezuma":               "Venustiano Carranza",
    "Balbuena":                "Venustiano Carranza",
    "Boulevard Puerto Aéreo":  "Venustiano Carranza",
    "Gómez Farías":            "Venustiano Carranza",
    "Zaragoza":                "Venustiano Carranza",
    "Pantitlán":               "Iztacalco",

    # ── Línea 2 ──
    "Cuatro Caminos":          "Naucalpan",           # Edomex
    "Panteones":               "Azcapotzalco",
    "Tacuba":                  "Miguel Hidalgo",
    "Cuitláhuac":              "Azcapotzalco",
    "Popotla":                 "Miguel Hidalgo",
    "Colegio Militar":         "Miguel Hidalgo",
    "Normal":                  "Cuauhtémoc",
    "San Cosme":               "Cuauhtémoc",
    "Revolución":              "Cuauhtémoc",
    "Hidalgo":                 "Cuauhtémoc",
    "Bellas Artes":            "Cuauhtémoc",
    "Allende":                 "Cuauhtémoc",
    "Zócalo/Tenochtitlan":     "Cuauhtémoc",
    "Pino Suárez":             "Cuauhtémoc",
    "San Antonio Abad":        "Cuauhtémoc",
    "Chilpancingo":            "Benito Juárez",
    "General Anaya":           "Benito Juárez",
    "Ermita":                  "Iztapalapa",
    "Portales":                "Benito Juárez",
    "Nativitas":               "Benito Juárez",
    "Villa de Cortés":         "Benito Juárez",
    "Xola":                    "Benito Juárez",
    "Viaducto":                "Benito Juárez",
    "Etiopía/Plaza de la Transparencia": "Benito Juárez",
    "División del Norte":      "Benito Juárez",
    "Zapata":                  "Benito Juárez",
    "Mixcoac":                 "Benito Juárez",
    "Barranca del Muerto":     "Álvaro Obregón",

    # ── Línea 3 ──
    "Indios Verdes":           "Gustavo A. Madero",
    "Deportivo 18 de Marzo":   "Gustavo A. Madero",
    "Potrero":                 "Gustavo A. Madero",
    "La Raza":                 "Gustavo A. Madero",
    "Tlatelolco":              "Cuauhtémoc",
    "Guerrero":                "Cuauhtémoc",
    "Juárez":                  "Cuauhtémoc",
    "Balderas":                "Cuauhtémoc",
    "Niños Héroes":            "Cuauhtémoc",
    "Hospital General":        "Cuauhtémoc",
    "Centro Médico":           "Cuauhtémoc",
    "Eugenia":                 "Benito Juárez",
    "Etiopía/Plaza de la Transparencia": "Benito Juárez",
    "Viveros/Derechos Humanos":"Coyoacán",
    "Miguel Ángel de Quevedo": "Coyoacán",
    "Copilco":                 "Coyoacán",
    "Universidad":             "Coyoacán",

    # ── Línea 4 ──
    "Martín Carrera":          "Gustavo A. Madero",
    "Talismán":                "Gustavo A. Madero",
    "Bondojito":               "Gustavo A. Madero",
    "Consulado":               "Gustavo A. Madero",
    "Canal del Norte":         "Cuauhtémoc",
    "Morelos":                 "Cuauhtémoc",
    "Candelaria":              "Venustiano Carranza",
    "Fray Servando":           "Venustiano Carranza",
    "Jamaica":                 "Venustiano Carranza",
    "Santa Anita":             "Iztacalco",

    # ── Línea 5 ──
    "Politécnico":             "Gustavo A. Madero",
    "Instituto del Petróleo":  "Gustavo A. Madero",
    "Autobuses del Norte":     "Gustavo A. Madero",
    "Misterios":               "Gustavo A. Madero",
    "Valle Gómez":             "Cuauhtémoc",
    "Eduardoo Molina":         "Gustavo A. Madero",
    "Eduardo Molina":          "Gustavo A. Madero",
    "Aragón":                  "Gustavo A. Madero",
    "Oceanía":                 "Venustiano Carranza",
    "Terminal Aérea":          "Venustiano Carranza",
    "Hangares":                "Venustiano Carranza",
    "Pantitlán":               "Iztacalco",

    # ── Línea 6 ──
    "El Rosario":              "Azcapotzalco",
    "Tezozómoc":               "Azcapotzalco",
    "UAM-Azcapotzalco":        "Azcapotzalco",
    "Ferrería/Arena Ciudad de México": "Azcapotzalco",
    "Norte 45":                "Estado de México",
    "Vallejo":                 "Azcapotzalco",
    "Instituto del Petróleo":  "Gustavo A. Madero",
    "Lindavista":              "Gustavo A. Madero",
    "Deportivo 18 de Marzo":   "Gustavo A. Madero",
    "La Villa/Basílica":       "Gustavo A. Madero",
    "Martín Carrera":          "Gustavo A. Madero",

    # ── Línea 7 ──
    "El Rosario":              "Azcapotzalco",
    "Aquiles Serdán":          "Azcapotzalco",
    "Camarones":               "Azcapotzalco",
    "Refinería":               "Azcapotzalco",
    "Tacuba":                  "Miguel Hidalgo",
    "San Joaquín":             "Miguel Hidalgo",
    "Polanco":                 "Miguel Hidalgo",
    "Auditorio":               "Miguel Hidalgo",
    "Constituyentes":          "Miguel Hidalgo",
    "Tacubaya":                "Miguel Hidalgo",
    "San Pedro de los Pinos":  "Álvaro Obregón",
    "San Antonio":             "Álvaro Obregón",
    "Mixcoac":                 "Benito Juárez",
    "Insurgentes Sur":         "Benito Juárez",
    "Barranca del Muerto":     "Álvaro Obregón",

    # ── Línea 8 ──
    "Garibaldi/Lagunilla":     "Cuauhtémoc",
    "Lagunilla":               "Cuauhtémoc",
    "Tepito":                  "Cuauhtémoc",
    "Obrera":                  "Cuauhtémoc",
    "Doctores":                "Cuauhtémoc",
    "Salto del Agua":          "Cuauhtémoc",
    "San Juan de Letrán":      "Cuauhtémoc",
    "Balderas":                "Cuauhtémoc",
    "Escuadrón 201":           "Iztacalco",
    "Atlalilco":               "Iztapalapa",
    "Iztapalapa":              "Iztapalapa",
    "Cerro de la Estrella":    "Iztapalapa",
    "UAM-I":                   "Iztapalapa",
    "Constitución de 1917":    "Iztapalapa",

    # ── Línea 9 ──
    "Tacubaya":                "Miguel Hidalgo",
    "Patriotismo":             "Benito Juárez",
    "Chilpancingo":            "Benito Juárez",
    "Centro Médico":           "Cuauhtémoc",
    "Lázaro Cárdenas":         "Cuauhtémoc",
    "Chabacano":               "Cuauhtémoc",
    "Jamaica":                 "Venustiano Carranza",
    "Mixiuhca":                "Iztacalco",
    "Velódromo":               "Iztacalco",
    "Ciudad Deportiva":        "Iztacalco",
    "Puebla":                  "Iztacalco",
    "Pantitlán":               "Iztacalco",

    # ── Línea A ──
    "Pantitlán":               "Iztacalco",
    "Agrícola Oriental":       "Iztacalco",
    "Canal de San Juan":       "Iztacalco",
    "Tepalcates":              "Iztapalapa",
    "Guelatao":                "Iztapalapa",
    "Peñón Viejo":             "Iztapalapa",
    "Acatitla":                "Iztapalapa",
    "Santa Marta":             "Iztapalapa",
    "Los Reyes":               "Estado de México",
    "La Paz":                  "Estado de México",

    # ── Línea B ──
    "Buenavista":              "Cuauhtémoc",
    "Guerrero":                "Cuauhtémoc",
    "Garibaldi/Lagunilla":     "Cuauhtémoc",
    "Lagunilla":               "Cuauhtémoc",
    "Tepito":                  "Cuauhtémoc",
    "Morelos":                 "Cuauhtémoc",
    "San Lázaro":              "Venustiano Carranza",
    "Romero Rubio":            "Venustiano Carranza",
    "Oceanía":                 "Venustiano Carranza",
    "Deportivo Oceanía":       "Venustiano Carranza",
    "Bosque de Aragón":        "Nezahualcóyotl (Edomex)",
    "Villa de Aragón":         "Gustavo A. Madero",
    "Nezahualcóyotl":          "Nezahualcóyotl (Edomex)",
    "Impulsora":               "Estado de México",
    "Río de los Remedios":     "Estado de México",
    "Múzquiz":                 "Estado de México",
    "Ecatepec":                "Estado de México",
    "Olivos":                  "Estado de México",
    "Plaza Aragón":            "Estado de México",
    "Ciudad Azteca":           "Estado de México",
    "Calle 11":                "Estado de México",

    # ── Línea 12 ──
    "Mixcoac":                 "Benito Juárez",
    "Insurgentes Sur":         "Benito Juárez",
    "Hospital 20 de Noviembre":"Benito Juárez",
    "Parque de los Venados":   "Benito Juárez",
    "Eje Central":             "Iztapalapa",
    "Zapata":                  "Benito Juárez",
    "Chabacano":               "Cuauhtémoc",
    "Lázaro Cárdenas":         "Cuauhtémoc",
    "Mexicaltzingo":           "Iztapalapa",
    "Ermita":                  "Iztapalapa",
    "General Anaya":           "Benito Juárez",
    "Atlalilco":               "Iztapalapa",
    "Nopalera":                "Iztapalapa",
    "Zapotitlán":              "Iztapalapa",
    "Tlaltenco":               "Tláhuac",
    "Tláhuac":                 "Tláhuac",
    "Tezonco":                 "Iztapalapa",
    "Olímpica":                "Iztapalapa",
    "San Andrés Tomatlan":     "Iztapalapa",
    "Culhuacán":               "Iztapalapa",
    "San Andrés Tomatlan":     "Iztapalapa",
    "San Andrés Tomatlán":     "Iztapalapa",
    "Tasqueña":                "Coyoacán",
    "Coyoacán":                "Coyoacán",
    "Ricardo Flores Magón":    "Venustiano Carranza",
    "Periférico Oriente":      "Iztapalapa",
    "Lomas Estrella":          "Iztapalapa",
    "Calle 11":                "Estado de México",
    "La Viga":                 "Iztacalco",
    "Santa Anita":             "Iztacalco",
    "Iztacalco":               "Iztacalco",
    "Apatlaco":                "Iztapalapa",
    "Aculco":                  "Iztapalapa",
    "Mexicaltzingo":           "Iztapalapa",
    "Coyuya":                  "Iztacalco",
    "Chilpancingo":            "Benito Juárez",
    "Viaducto":                "Benito Juárez",
    "Xola":                    "Benito Juárez",
    "Villa de Cortés":         "Benito Juárez",
    "Nativitas":               "Benito Juárez",
    "Portales":                "Benito Juárez",
    "Hospital 20 de Noviembre":"Benito Juárez",
    "Insurgentes Sur":         "Benito Juárez",
}

print("Mapeando estaciones a alcaldías...")
df["alcaldia"] = df["estacion"].map(ESTACION_ALCALDIA)

sin_alcaldia = df["alcaldia"].isna().sum()
estaciones_sin = df[df["alcaldia"].isna()]["estacion"].unique()
print(f"  Estaciones sin alcaldía asignada: {len(estaciones_sin)}")
if len(estaciones_sin) > 0:
    print(f"  → {list(estaciones_sin)}")


# 6. FILTROS DE CALIDAD

n_antes = len(df)

# Remover fechas inválidas
df = df.dropna(subset=["fecha"])

# Remover afluencia = 0 (estaciones cerradas, días sin servicio)
df = df[df["afluencia"] > 0]

n_despues = len(df)
print(f"\nFiltros aplicados:")
print(f"  Filas originales:  {n_antes:,}")
print(f"  Filas conservadas: {n_despues:,}")
print(f"  Filas removidas:   {n_antes - n_despues:,} ({(n_antes-n_despues)/n_antes*100:.1f}%)")


# 7. COLUMNAS FINALES Y ORDEN

df = df[["fecha", "anio", "mes", "linea", "estacion", "alcaldia", "afluencia"]]
df = df.sort_values(["fecha", "linea", "estacion"]).reset_index(drop=True)


# 8. GUARDAR
output = "metro_limpio.csv"
df.to_csv(output, index=False, encoding="utf-8")
print(f"\nArchivo guardado: {output}")
print(f"Shape final: {df.shape}")
print(f"\nVista previa:")
print(df.head(10).to_string(index=False))
print(f"\nAlcaldías encontradas:")
print(df["alcaldia"].value_counts().head(20).to_string())
