import pandas as pd
import plotly.express as px

act = pd.read_csv('../datos/tvar_crea.csv', low_memory=False)
cdmx = act[act['CVE_ENT'] == 9].copy()

cdmx['condicion'] = cdmx['COND_AEE'].map({
    1: 'Ocupada/o',
    2: 'Con vínculo laboral',
    3: 'Desocupada/o',
    4: 'Estudiante',
    5: 'Quehaceres del hogar',
    6: 'Otro inactivo'
})
cdmx['sexo'] = cdmx['SEXO'].map({1: 'Hombre', 2: 'Mujer'})

traslado_sexo = cdmx.groupby('sexo')['TRAS_TRAB'].mean().reset_index()
traslado_sexo.columns = ['Sexo', 'Horas_traslado']
traslado_sexo['Horas_traslado'] = traslado_sexo['Horas_traslado'].round(2)

fig1 = px.bar(
    traslado_sexo,
    x='Sexo', y='Horas_traslado',
    color='Sexo',
    color_discrete_map={'Hombre': '#3B82F6', 'Mujer': '#EC4899'},
    text='Horas_traslado',
    title='Horas semanales de traslado al trabajo por sexo · CDMX (ENUT 2024)'
)
fig1.update_traces(texttemplate='%{text} hrs', textposition='outside')
fig1.update_layout(showlegend=False, yaxis_title='Horas por semana', xaxis_title='')
fig1.show()


tlibre = cdmx.groupby('condicion')['ACTIV_CONVIV'].mean().reset_index()
tlibre.columns = ['Condicion', 'Tiempo_libre']
tlibre = tlibre.sort_values('Tiempo_libre')

fig2 = px.bar(
    tlibre,
    x='Tiempo_libre', y='Condicion',
    orientation='h',
    color='Tiempo_libre',
    color_continuous_scale='Teal',
    text='Tiempo_libre',
    title='Tiempo libre semanal por condición de actividad · CDMX (ENUT 2024)'
)
fig2.update_traces(texttemplate='%{text:.1f} hrs', textposition='outside')
fig2.update_layout(coloraxis_showscale=False, xaxis_title='Horas de convivencia/semana', yaxis_title='')
fig2.show()


resumen = cdmx.groupby('condicion').agg(
    traslado=('TRAS_TRAB', 'mean'),
    trabajo=('ACTIV_MERC', 'mean'),
    tiempo_libre=('ACTIV_CONVIV', 'mean'),
    n=('COND_AEE', 'count')
).round(2).reset_index()

resumen.to_csv('../datos/enut_cdmx_resumen.csv', index=False)
print("Guardado: datos/enut_cdmx_resumen.csv")
print(resumen.to_string())