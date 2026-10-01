datasets = [
    "https://media.githubusercontent.com/media/StackExchange/Survey/6ae2209cd35a55e92739ba82f7887fb86807a069/packages/archive/2025/results.csv"
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