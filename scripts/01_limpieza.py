import pandas as pd

df = pd.read_csv('../datos/ENOE_SDEMT425.csv', encoding='latin1', low_memory=False)
print("Columnas disponibles:", df.columns.tolist())
print("Total de registros:", len(df))

df['cve_ent'] = df['cve_ent'].astype(str).str.zfill(2)
df_cdmx = df[df['cve_ent'] == '09'].copy()
print(f"Registros CDMX: {len(df_cdmx)}")

df_cdmx['sector'] = pd.to_numeric(df_cdmx['clase2'], errors='coerce')
df_cdmx['sector'] = df_cdmx['sector'].map({1: 'Formal', 2: 'Informal'})
df_cdmx['horas_semana']    = pd.to_numeric(df_cdmx['hrsocup'], errors='coerce')
df_cdmx['ingreso_mensual'] = pd.to_numeric(df_cdmx['ingocup'], errors='coerce')
df_cdmx['sexo']            = pd.to_numeric(df_cdmx['sex'], errors='coerce').map({1: 'Hombre', 2: 'Mujer'})

df_cdmx['clase1'] = pd.to_numeric(df_cdmx['clase1'], errors='coerce')
df_ocu = df_cdmx[df_cdmx['clase1'] == 1].copy()
df_ocu['seg_soc'] = pd.to_numeric(df_ocu['seg_soc'], errors='coerce')
df_ocu['sector'] = df_ocu['seg_soc'].map({1: 'Formal', 2: 'Informal'})

df_ocu['horas_semana']    = pd.to_numeric(df_ocu['hrsocup'], errors='coerce')
df_ocu['ingreso_mensual'] = pd.to_numeric(df_ocu['ingocup'], errors='coerce')
df_ocu['sexo']            = pd.to_numeric(df_ocu['sex'], errors='coerce').map({1: 'Hombre', 2: 'Mujer'})

df_limpio = df_ocu[
    df_ocu['sector'].notna() &
    df_ocu['horas_semana'].notna() &
    df_ocu['ingreso_mensual'].notna() &
    (df_ocu['horas_semana'] > 0) &
    (df_ocu['ingreso_mensual'] > 0)
].copy()

df_limpio['ingreso_por_hora'] = (
    df_limpio['ingreso_mensual'] / (df_limpio['horas_semana'] * 4.3)
).round(2)

df_limpio[['sector', 'sexo', 'horas_semana', 'ingreso_mensual', 'ingreso_por_hora']]\
    .to_csv('../datos/enoe_cdmx_limpio.csv', index=False)

print(f"Dataset limpio: {len(df_limpio)} registros")
print("\nConteo por sector:")
print(df_limpio['sector'].value_counts())
print("\nResumen por sector:")
print(df_limpio.groupby('sector')[
    ['horas_semana', 'ingreso_mensual', 'ingreso_por_hora']
].mean().round(1))