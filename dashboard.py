import math
import matplotlib.pyplot as plt

#un chart es un grafico que contiene una funcion dibujo.
class Chart:
    def __init__(self, draw, title=None):
        self.draw = draw
        self.title = title

    def render(self, ax):
        self.draw(ax)

        if self.title:
            ax.set_title(self.title)

#contiene los graficos posibles por defecto
class Graph:
    def __init__(self, dashboard):
        self.dashboard = dashboard
    def bar(self, df, col, min=500, cut=None, rot=0, multiple_r=False, max_cat=5):
        def draw(ax):
            if not multiple_r:
                frecuencias = df[col].value_counts()
            else:
                frecuencias = (
                    df[col]
                    .dropna()
                    .str.split(';')
                    .explode()
                    .str.strip()
                    .value_counts()
                ) 
            if cut and isinstance(cut, int):
                frecuencias.index = frecuencias.index.str[:cut]
            elif cut and isinstance(cut, dict):
                frecuencias.index = frecuencias.index.map(lambda x: cut.get(x, x))
            elif cut:
                frecuencias.index = frecuencias.index.str.split(cut).str[0]

            #frecuencias = frecuencias.groupby(level=0).sum()

            agrupadas = frecuencias[frecuencias >= min].copy()
            otros = frecuencias[frecuencias < min].sum()

            top = agrupadas.iloc[:max_cat]
            otros += agrupadas.iloc[max_cat:].sum()
            agrupadas = top

            if otros > 0:
                agrupadas["Otros"] = otros

            agrupadas.plot(
                kind="bar",
                edgecolor="black",
                ax=ax
            )

            ax.set_xlabel("")
            ax.tick_params(axis="x", rotation=rot)

        chart = Chart(draw=draw, title=col)
        self.dashboard.addChart(chart)
    
    def multiple_hist(self, df, columnas, bins=15):
        datos = df[columnas].select_dtypes(include="number")

        for columna in datos.columns:
            def draw(ax, columna=columna):
                ax.hist(
                    datos[columna].dropna(),
                    bins=bins,
                    edgecolor="black"
                )
                ax.set_xlabel("")
                ax.grid(False)

            chart = Chart(draw=draw, title=columna)
            self.dashboard.addChart(chart)

#el dashboard almacena los graficos que le vamos anadiendo para luego imprimir todos juntos.
class Dashboard:
    def __init__(self, columns=2, figsize=(16, 10)):
        self.columns = columns
        self.figsize = figsize
        self.charts = []
        self.add = Graph(self)

    def addChart(self, chart):
        if not isinstance(chart, Chart):
            raise TypeError("Se esperaba un objeto Chart")

        self.charts.append(chart)

    def show(self):
        if not self.charts:
            raise ValueError("El dashboard no tiene gráficos")

        n = len(self.charts)
        rows = math.ceil(n / self.columns)

        width, height = self.figsize
        fig, axes = plt.subplots(
            rows,
            self.columns,
            figsize=(width, max(height, 3.5 * rows)),
            squeeze=False
        )

        for i, chart in enumerate(self.charts):
            ax = axes.flat[i]
            chart.render(ax)


        for i in range(n, rows * self.columns):
            axes.flat[i].set_visible(False)

        fig.subplots_adjust(
            hspace=0.3,
            wspace=0.2
        )

        plt.show()
