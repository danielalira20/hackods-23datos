import pandas as pd

df = pd.read_csv('../datos/ENOE_SDEMT425.csv', encoding='latin1', low_memory=False)
df['cve_ent'] = df['cve_ent'].astype(str).str.zfill(2)
df_cdmx = df[df['cve_ent'] == '09'].copy()

# Diagnóstico — ver los valores reales de cada columna clave
print("=== clase1 ===")
print(df_cdmx['clase1'].value_counts())

print("\n=== clase2 ===")
print(df_cdmx['clase2'].value_counts())

print("\n=== s_clasifi ===")
print(df_cdmx['s_clasifi'].value_counts())

print("\n=== seg_soc ===")
print(df_cdmx['seg_soc'].value_counts())