

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
def graficar_nulos(df, frecuencias, labels, title='Distribución de valores nulos', colors=('#e76f51', '#2a9d8f'), axe=None):

    if axe:
        tool = axe
    else:
        tool = plt
        
    resultado = tool.pie(
        frecuencias,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90
    )
    wangle=resultado[0]

    tool.legend(
        handles=wangle,
        labels=labels,
        loc='lower center',
        bbox_to_anchor=(0.5, 0.9),
        ncol=len(labels)
    )
    if not axe:
        plt.title(title)
        plt.show()
    else:
        tool.set_title(title)


import numpy as  np
'''funcion especifica que se usa para, dado un dataset y una columna, calcular los limites inferiores y superiores para outliers'''
def get_rangos(df, col):
    q1 = np.nanpercentile(df[col], 25)
    q3 = np.nanpercentile(df[col], 75)
    iqr = q3 - q1

    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr

    out = df[(df[col] > lim_sup) | (df[col] < lim_inf)][col]
    norm = df[(df[col] <= lim_sup) & (df[col] >= lim_inf)]

    return out, norm


'''funcion especifica que se usa para, dado un dataset y una columna, graficar el porcentaje de nulos y outliers
en base a un grafico de torta'''
def graficar_nulos_outliers(df, col):
    
    out, norm = get_rangos(df, col)
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))

    #Grafico de proporcion de outliers
    frecuencias = [out.value_counts().sum(), norm[col].value_counts().sum()]
    labels = [f'outliers: {frecuencias[0]}', f'normales: {frecuencias[1]}']
    graficar_nulos(df, frecuencias, labels, f'Distribucion de outliers para {col}', ["#474f4a", '#1e984f'], axes[0])

    #Grafico de proporcion de nulos
    validos = frecuencias[0]+frecuencias[1]
    nulos = df[col].isna().sum()
    labels = [f'nulos: {nulos}', f'validos: {validos}']
    graficar_nulos(df, [nulos, validos], labels, f'Distribucion de outliers para {col}', ["#474f4a", '#1e984f'], axes[1])

    plt.show()
