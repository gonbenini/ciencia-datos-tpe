datasets = [
    "https://media.githubusercontent.com/media/StackExchange/Survey/6ae2209cd35a55e92739ba82f7887fb86807a069/packages/archive/2025/results.csv",
    "https://media.githubusercontent.com/media/StackExchange/Survey/refs/heads/main/packages/archive/2025/schema.csv"
]

def extract_if_zip(file_name, file_path):
    import zipfile

    if file_name.lower().endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(".") 

def descargar(urls=datasets, force=False):
    from urllib import request as req
    import os

    for url in urls:
        file_name = url.split('/')[-1]
        file_path = f"./{file_name}"
        
        if os.path.exists(file_path) and not force:
            continue
            
        req.urlretrieve(url, file_path)

        extract_if_zip(file_name, file_path)

def mostrar_archivo(archivo, lines=None):
    with open(archivo, "r", encoding="utf-8") as f:
        if lines:
            for _i in range(lines):
                # cuando el archivo sea tan grande que crashearia el navegador de jupyer, en vez de imprimirlo entero muestro solo tanta cantidad de lineas.
                descripcion = f.readline()
                if not descripcion:
                    break
                print(descripcion, end='')
        else:
            descripcion = f.read()
            print(descripcion)

# No lo meto en un `if __name__ == "__main__":` a proposito asi solo con hacer `import utils` ya se descarga
descargar()




#---------------------Graficos----------------------
import matplotlib.pyplot as plt
import math

'''
funcion especifica que se usa para, dado un conjunto de columnas, calcular el promedio de promedios de valores nulos
y expresarlo en un grafico de torta
'''
def graficar_nulos(df, cols, labels, title='Distribución de valores nulos', colors=('#e76f51', '#2a9d8f')):
    datos = df[cols]
    valores = [
        #Promedio de promedios de cada columna.
        datos.isna().mean().mean(),
        datos.notna().mean().mean()
    ]

    resultado = plt.pie(
        valores,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90
    )
    wangle=resultado[0]

    plt.legend(
        handles=wangle,
        labels=labels,
        loc='lower center',
        bbox_to_anchor=(0.5, 0.9),
        ncol=len(labels)
    )
    plt.title(title)
    plt.show()