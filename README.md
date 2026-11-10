# Análisis de Stack Overflow Developer Survey 2025

Notebook de análisis de los resultados de la encuesta, junto con dos módulos de apoyo.

| Archivo            | ¿Qué hace?                                                                                      |
|--------------------|-------------------------------------------------------------------------------------------------|
| `entregable.ipynb` | Notebook principal: análisis exploratorio, limpieza, reducción de dimensionalidad e hipótesis.  |
| `utils.py`         | Descarga los datos y ofrece funciones de gráficos para explorar y limpiar.                      |
| `dashboard.py`     | Permite armar un tablero con varios gráficos juntos en una sola figura.                         |

## Dependencias

```bash
pip install -r requirements.txt
```

## `entregable.ipynb`

Importa `utils` y `dashboard` y recorre el análisis en este orden:

1. **Análisis exploratorio:** distribución de las variables con dashboards y matriz de correlación.
2. **Limpieza de datos:** descarte de variables (respuesta libre, redundantes o con muchos nulos), duplicados y outliers.
3. **Reducción de dimensionalidad:** PCA, t-SNE y UMAP.
4. **Validación de hipótesis:** pruebas univariadas y bivariadas.

Debe ejecutarse desde la carpeta donde estén (o se descarguen) `results.csv` y `schema.csv`.

## `utils.py`

Al hacer `import utils` se descargan automáticamente `results.csv` (respuestas) y `schema.csv` (descripción de las columnas), salvo que ya existan. La primera vez necesita conexión a internet.

**Manejo de archivos**
- `descargar(urls, force)`: descarga los archivos y descomprime los `.zip`.
- `mostrar_archivo(archivo, lines)`: imprime un archivo de texto, o solo sus primeras líneas si es muy grande.

**Gráficos de exploración**
- `pie_chart`: torta con porcentajes y leyenda.
- `get_ranges`: separa outliers y valores normales de una columna usando el rango intercuartílico (IQR).
- `graph_nulls_outliers`: dos tortas con la proporción de outliers y de nulos de una columna.
- `scatter`: dispersión entre dos variables, con su correlación de Pearson.
- `box_plot_comparative`: boxplot de una columna sin outliers vs. con los datos originales.

**Ejemplo**
```python
import pandas as pd
import utils

df = pd.read_csv("results.csv")
utils.graph_nulls_outliers(df, "ConvertedCompYearly")
utils.scatter("WorkExp", "YearsCode", df)
```

## `dashboard.py`

Se van agregando gráficos al dashboard y `show()` los dibuja todos juntos en una grilla.

- `Dashboard(columns, figsize)`: guarda los gráficos y los muestra.
- `dash.add.bar(df, col, ...)`: barras con la frecuencia de cada categoría. Agrupa las poco frecuentes en "Otros" (`min`, `max_cat`), permite acortar o renombrar etiquetas (`cut`) y soporta preguntas de respuesta múltiple separadas por `;` (`multiple_r=True`).
- `dash.add.multiple_hist(df, columnas, bins)`: un histograma por cada columna numérica.
- `Chart(draw, title)` y `dash.addChart(chart)`: permiten agregar un gráfico propio, pasando una función que dibuja sobre un eje de matplotlib.

**Ejemplo**
```python
from dashboard import Dashboard

dash = Dashboard(columns=2)
dash.add.bar(df, "Country", max_cat=6, rot=45)
dash.add.bar(df, "LanguageHaveWorkedWith", multiple_r=True, rot=45)
dash.add.multiple_hist(df, ["YearsCode", "WorkExp"])
dash.show()
```