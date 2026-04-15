# 2-3 Datos — HackODS

> *No lo decimos nosotros. Lo dicen los datos del propio gobierno.*

---

##Equipo

**2-3 Datos**

| Integrante | Rol |
|---|---|
| José David Chávez Tipa | Análisis de datos y scripts Python |
| Daniela Guadalupe Lira Huerta | Coordinación y limpieza de datos |
| Margarita Reyes Trujillo | Dashboard y visualizaciones |

---

##  ODS Elegido

**ODS 8 — Trabajo Decente y Crecimiento Económico**

Promover el crecimiento económico sostenido, inclusivo y sostenible, el empleo pleno y productivo, y el trabajo decente para todas las personas.

---

##  Descripción del Proyecto

Este proyecto analiza la brecha de desigualdad laboral en la Ciudad de México a través de tres dimensiones:

- **Disparidad de ingresos** entre el sector formal e informal
- **Uso del tiempo libre y los traslados** según condición laboral y género
- **Patrones de movilidad** en el Sistema de Transporte Colectivo Metro

Utilizando datos oficiales de la Encuesta Nacional de Ocupación y Empleo (ENOE T4 2025), la Encuesta Nacional sobre el Uso del Tiempo (ENUT 2024) y los registros de afluencia del Metro CDMX, buscamos demostrar que la informalidad laboral no es un fenómeno marginal, sino la condición de trabajo de más de la mitad de la fuerza laboral capitalina — con consecuencias medibles en el ingreso, el tiempo disponible y el acceso a la movilidad urbana.


---

##  Fuentes de datos

| Fuente | Dataset | Portal |
|---|---|---|
| INEGI | ENOE T4 2025 | [inegi.org.mx](https://www.inegi.org.mx/programas/enoe/15ymas/) |
| INEGI | ENUT 2024 | [inegi.org.mx](https://www.inegi.org.mx/programas/enut/2024/) |
| SEMOVI / ADIP | Afluencia diaria del Metro CDMX | [datos.cdmx.gob.mx](https://datos.cdmx.gob.mx/dataset/afluencia-diaria-del-metro-cdmx) |

## Cómo ejecutar el proyecto

**Requisitos:**
- Python 3.10+
- Quarto ([quarto.org](https://quarto.org/docs/get-started/))

**Instalar dependencias:**
```bash
pip install pandas plotly statsmodels jupyter
```

**Correr los scripts de limpieza:**
```bash
python scripts/01_limpieza.py
python scripts/03_enut.py
```

**Lanzar el dashboard:**
```bash
cd dashboard
quarto preview tablero.qmd
```

---

## Licencia 

Este proyecto está bajo la licencia **CC BY-SA 4.0**. Consulta el archivo [LICENSE](./LICENSE) para ver el texto legal completo.
