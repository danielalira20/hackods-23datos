# AI-LOG — Registro de uso de Inteligencia Artificial

Este archivo documenta el uso de herramientas de IA a lo largo del desarrollo del proyecto,
incluyendo los prompts utilizados y los resultados obtenidos.

**Herramientas principales:** Perplexity AI y Claude 
**Proyecto:** Trabajo Decente en la CDMX — HackODS UNAM 2026

---

| Fecha | Tarea | Prompt | Resultado |
| ----- | ----- | ------ | --------- |
| 09-04-26 | Creación de licencia | ¿Cómo obtengo con curl la licencia CC BY-SA desde la terminal? | Licencia CC descargada y añadida al repo |
| 13-04-26 | Corrección de error en Quarto | `TypeError: only 0-dimensional arrays can be converted to Python scalars` al hacer `float()` sobre `.values` | Se corrigió agregando `[0]` al indexar: `float(...values[0])` |
| 14-04-26 | Alineación de paleta de colores | Los colores del home se veían muy distintos a los del dashboard | Se unificó la paleta: `#14B8A6`, `#F59E0B`, `#8B5CF6`, `#3B82F6`, `#EC4899` en ambos archivos |
| 14-04-26 | Publicación en GitHub Pages | ¿Cómo publico el dashboard en una URL tipo `github.io`? | Se explicaron los 4 pasos: configurar `output-dir: docs` en `_quarto.yml`, renderizar, subir a GitHub y activar Pages |

---

*Todas las respuestas fueron revisadas y adaptadas por el equipo antes de implementarse.*