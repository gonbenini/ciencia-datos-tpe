# Análisis de Stack Overflow Developer Survey 2025

Notebook de análisis de los resultados de la encuesta, junto con dos módulos de apoyo.

| Archivo            | ¿Qué hace?                                                                                      |
|--------------------|-------------------------------------------------------------------------------------------------|
| `entregable.ipynb` | Notebook principal: análisis exploratorio, limpieza, reducción de dimensionalidad e hipótesis.  |
| `utils.py`         | Descarga los datos y ofrece funciones de gráficos para explorar y limpiar.                      |
| `dashboard.py`     | Permite armar un tablero con varios gráficos juntos en una sola figura.                         |

## Dependencias

Se recomienda usar un entorno virtual para no mezclar las librerías con otros proyectos.

```bash
# Crear el entorno virtual
python3 -m venv venv_tpe            # Linux / macOS
python -m venv venv_tpe             # Windows 

# Activarlo
source venv_tpe/bin/activate        # Linux / macOS
venv_tpe\Scripts\activate           # Windows

# Instalar las dependencias
pip install -r requirements.txt
```

Para desactivar el entorno al terminar usar: `deactivate`.

## `entregable.ipynb`

Importa `utils` y `dashboard` y recorre el análisis en este orden:

1. **Análisis exploratorio:** Distribución de las variables con dashboards y matriz de correlación.
2. **Limpieza de datos:** Descarte de variables (respuesta libre, redundantes o con muchos nulos), duplicados y outliers.
3. **Reducción de dimensionalidad:** PCA, t-SNE y UMAP.
4. **Validación de hipótesis:** Pruebas univariadas, bivariadas y multivariadas.

## Datos

Los datos están incluidos en el repositorio:

| Archivo       | Contenido                                                                                       |
|---------------|-------------------------------------------------------------------------------------------------|
| `results.zip` | Respuestas de la encuesta (`results.csv` comprimido, ya que pesa ~140 MB y GitHub admite hasta 100 MB por archivo). |
| `schema.csv`  | Descripción de cada columna (metadatos).                                                        |

**No hace falta descomprimir `results.zip`**: el notebook lo lee directamente con `pd.read_csv('results.zip')`, ya que pandas detecta la compresión por la extensión.

## Ejecución

```bash
source venv_tpe/bin/activate        # Linux / macOS (venv_tpe\Scripts\activate en Windows)
jupyter notebook entregable.ipynb
```

Ejecutar el notebook desde la carpeta raíz del repositorio (donde están `results.zip` y `schema.csv`), de arriba hacia abajo (*Kernel → Restart & Run All*).

## `utils.py`

Al hacer `import utils` se descarga automáticamente `schema.csv` si no existe. `results.csv` solo se descarga si tampoco existe `results.zip`, por lo que con el repositorio completo no hace falta conexión a internet.

**Manejo de archivos**
- `descargar(urls, force)`: Descarga los archivos y descomprime los `.zip`.
- `mostrar_archivo(archivo, lines)`: Imprime un archivo de texto, o solo sus primeras líneas si es muy grande.

**Gráficos de exploración**
- `pie_chart`: Torta con porcentajes y leyenda.
- `get_ranges`: Separa outliers y valores normales de una columna usando el rango intercuartílico (IQR).
- `graph_nulls_outliers`: Dos tortas con la proporción de outliers y de nulos de una columna.
- `scatter`: Dispersión entre dos variables, con su correlación de Pearson.
- `box_plot_comparative`: Boxplot de una columna sin outliers vs. con los datos originales.

**Ejemplo** (basado en [`entregable.ipynb`](https://github.com/gonbenini/ciencia-datos-tpe/blob/3be3f18163b0a7e3dba0a19e40ed1da3ab4c010a/entregable.ipynb))
```python
import pandas as pd
import utils

df = pd.read_csv("results.zip", low_memory=False)

data = df.copy()
cols = ['ToolCountWork', 'ConvertedCompYearly']
for i in cols:
    utils.box_plot_comparative(data, i)
    utils.graph_nulls_outliers(data, i)
    out, _ = utils.get_ranges(data, i)

utils.scatter('WorkExp', 'YearsCode', df, alpha=1)
```
> _Este fragmento no aparece **exactamente así** en el notebook.<br>Es una recopilación de varias celdas, con las listas de columnas acortadas._

## `dashboard.py`

Se van agregando gráficos al dashboard y `show()` los dibuja todos juntos en una grilla.

- `Dashboard(columns, figsize)`: Guarda los gráficos y los muestra.
- `dash.add.bar(df, col, ...)`: Barras con la frecuencia de cada categoría. Agrupa las poco frecuentes en "Otros" (`min`, `max_cat`), permite acortar o renombrar etiquetas (`cut`) y soporta preguntas de respuesta múltiple separadas por `;` (`multiple_r=True`).
- `dash.add.multiple_hist(df, columnas, bins)`: Un histograma por cada columna numérica.
- `Chart(draw, title)` y `dash.addChart(chart)`: Permiten agregar un gráfico propio, pasando una función que dibuja sobre un eje de matplotlib.

**Ejemplo** (basado en [`entregable.ipynb`](https://github.com/gonbenini/ciencia-datos-tpe/blob/3be3f18163b0a7e3dba0a19e40ed1da3ab4c010a/entregable.ipynb))
```python
import dashboard as ds

dash1 = ds.Dashboard(columns=4, figsize=(20, 4))
dash1.add.bar(df, "Country", min=1000, cut=3)
dash1.add.bar(df, "Age", min=2000, cut=' ')
dash1.add.multiple_hist(df, ['JobSat', 'ToolCountWork', 'ConvertedCompYearly'], bins=10)
dash1.show()
```
> _Este fragmento no aparece **exactamente así** en el notebook.<br>Es una recopilación de varias celdas, con las listas de columnas acortadas._