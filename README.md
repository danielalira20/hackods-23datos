# 2-3 Datos — HackODS

> *No lo decimos nosotros. Lo dicen los datos del propio gobierno.*

## Resumen

Tablero de datos para analizar la brecha laboral en la Ciudad de México con foco en:

- **Ingresos** entre sector formal e informal
- **Uso del tiempo** y traslados según condición laboral y género
- **Movilidad** y concentración de afluencia en el Metro CDMX

El tablero principal vive en `dashboard/index.qmd` y el sitio publicado se genera en `docs/`.

---

## Equipo

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

## Estructura del proyecto

- `dashboard/index.qmd`: tablero principal del proyecto.
- `dashboard/tablero.qmd`: borrador / versión alternativa del dashboard.
- `datos/`: archivos fuente y salidas procesadas.
- `scripts/`: limpieza, análisis y generación de resultados.
- `docs/`: HTML renderizado para publicación.

##  Fuentes de datos

| Fuente | Dataset | Portal |
|---|---|---|
| INEGI | ENOE T4 2025 | [inegi.org.mx](https://www.inegi.org.mx/programas/enoe/15ymas/) |
| INEGI | ENUT 2024 | [inegi.org.mx](https://www.inegi.org.mx/programas/enut/2024/) |
| SEMOVI / ADIP | Afluencia diaria del Metro CDMX | [datos.cdmx.gob.mx](https://datos.cdmx.gob.mx/dataset/afluencia-diaria-del-metro-cdmx) |

## Cómo ejecutar el proyecto

**Requisitos:**
- Python 3.10+
- `uv`
- Quarto ([quarto.org](https://quarto.org/docs/get-started/))

**Crear el entorno con `uv`:**
```bash
uv venv
source .venv/bin/activate
```

**Instalar dependencias del proyecto:**
```bash
uv sync
```

**Instalar Quarto si hace falta:**
```bash
quarto --version
```

**Correr los scripts de preparación de datos:**
```bash
uv run python scripts/01_limpieza.py
uv run python scripts/03_enut.py
uv run python scripts/04_limpieza_metro.py
uv run python scripts/05_analisis_metro.py
```

**Alternativa sin activar el entorno:**
```bash
uv run python scripts/01_limpieza.py
uv run quarto render dashboard/index.qmd
```

**Renderizar el dashboard principal:**
```bash
uv run quarto render dashboard/index.qmd
```

**Previsualizar en local:**
```bash
cd dashboard
uv run quarto preview index.qmd
```

> Nota: el render genera el sitio en `docs/` según la configuración de `dashboard/_quarto.yml`.

---

## Archivos de salida

- `datos/enoe_cdmx_limpio.csv`
- `datos/enut_cdmx_resumen.csv`
- `datos/metro_limpio.csv`
- `datos/resultados_analisis_metro/*.csv`
- `docs/index.html`

## Licencia 

Este proyecto está bajo la licencia **CC BY-SA 4.0**. Consulta el archivo [LICENSE](./LICENSE) para ver el texto legal completo.

## Declaración de IA

El repositorio incluye `DECLARATORIA_IA.md` para documentar el uso de herramientas de IA durante el desarrollo.
