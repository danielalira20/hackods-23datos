import pandas as pd
import folium

# 1. Cargar tus datos
df_top = pd.read_csv('../resultados_analisis_metro/02_top_estaciones.csv')  # Ajusta el nombre del archivo si es necesario

# 2. Diccionario de coordenadas para tu TOP (ajustado a tus nombres exactos)
coords = {
    'Indios Verdes': [19.4954, -99.1195],
    'Cuatro Caminos': [19.4596, -99.2158],
    'Constitución de 1917': [19.3460, -99.0639],
    'Tasqueña': [19.3437, -99.1395],
    'Pantitlán': [19.4151, -99.0743],
    'Universidad': [19.3243, -99.1739],
    'Zócalo/Tenochtitlan': [19.4325, -99.1322],
    'Observatorio': [19.3982, -99.2004],
    'Ciudad Azteca': [19.5341, -99.0272],
    'Buenavista': [19.4468, -99.1531],
    'Tacubaya': [19.4032, -99.1871],
    'Chapultepec': [19.4204, -99.1763],
    'Insurgentes': [19.4233, -99.1628],
    'Zaragoza': [19.4121, -99.0823],
    'Merced': [19.4255, -99.1245],
    'Chilpancingo': [19.4060, -99.1687],
    'Barranca del Muerto': [19.3591, -99.1895]
}

# 3. Mapear coordenadas al DF
df_top['lat'] = df_top['estacion'].map(lambda x: coords.get(x, [None, None])[0])
df_top['lon'] = df_top['estacion'].map(lambda x: coords.get(x, [None, None])[1])
df_top = df_top.dropna(subset=['lat'])
# 4. Crear el mapa
m = folium.Map(location=[19.4326, -99.1332], zoom_start=11, tiles="cartodbpositron")
estaciones_unicas = df_top['estacion'].unique()
colores = [
    'red', 'blue', 'green', 'purple', 'orange', 'darkred', 
    'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 
    'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray'
]
# Mapeamos cada estación a un color
mapa_colores = {estacion: colores[i % len(colores)] for i, estacion in enumerate(estaciones_unicas)}
for _, row in df_top.iterrows():
    if pd.notnull(row['lat']):
        # CAMBIO AQUÍ: Usamos el diccionario de colores que creaste arriba
        color_estacion = mapa_colores[row['estacion']]
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            # El radio ahora es más pequeño (/40 en lugar de /20)
            radius=row['afluencia_millones'] / 40, 
            popup=f"<b>{row['estacion']}</b><br>{row['linea']}<br>{row['afluencia_millones']}M viajes",
            color=color_estacion, # Color único por estación
            fill=True,
            fill_color=color_estacion, # Rellenamos con el mismo color
            fill_opacity=0.8,
            weight=1
        ).add_to(m)

# Guardar
m.save('mapa_afluencia2.html')
print("Mapa generado con colores únicos y círculos pequeños.")