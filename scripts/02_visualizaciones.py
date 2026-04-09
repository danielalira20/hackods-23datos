import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('../datos/enoe_cdmx_limpio.csv')

resumen = df.groupby('sector').agg(
    horas=('horas_semana', 'mean'),
    ingreso=('ingreso_mensual', 'mean'),
    pago_hora=('ingreso_por_hora', 'mean'),
    conteo=('sector', 'count')
).reset_index().round(1)

print("Resumen:")
print(resumen.to_string())

#Grafica para el ingreso mensual por sector
fig1 = px.bar(
    resumen,
    x='sector', y='ingreso',
    color='sector',
    color_discrete_map={'Formal': '#14B8A6', 'Informal': '#F59E0B'},
    text='ingreso',
    title='La brecha de ingreso: Formal vs Informal · CDMX (ENOE T4 2025)'
)
fig1.update_traces(
    texttemplate='$%{text:,.0f}', 
    textposition='outside'
)
fig1.update_layout(
    showlegend=False,
    yaxis_title='Ingreso mensual promedio (MXN)',
    xaxis_title='',
    yaxis_tickprefix='$',
    yaxis_tickformat=','
)
fig1.show()

#grafica para distribucion de trabajadores
fig2 = px.bar(
    resumen,
    x='sector', y='conteo',
    color='sector',
    color_discrete_map={'Formal': '#14B8A6', 'Informal': '#F59E0B'},
    text='conteo',
    title='Más trabajadores en informalidad que en formalidad · CDMX'
)
fig2.update_traces(
    texttemplate='%{text} personas',
    textposition='outside'
)
fig2.update_layout(
    showlegend=False,
    yaxis_title='Número de trabajadores',
    xaxis_title=''
)
fig2.show()

#grafica de igrreso por hora
fig3 = px.scatter(
    df,
    x='horas_semana', y='ingreso_por_hora',
    color='sector',
    color_discrete_map={'Formal': '#14B8A6', 'Informal': '#F59E0B'},
    opacity=0.4,
    trendline='ols',
    title='Horas trabajadas vs ingreso por hora · CDMX'
)
fig3.update_layout(
    xaxis_title='Horas por semana',
    yaxis_title='Ingreso por hora (MXN)'
)
fig3.show()

print("visuales listoss")