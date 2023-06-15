import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Define las especificaciones de las columnas de ancho fijo
colspecs = [(0, 20), (20, 43), (43, 71), (71, 76)]  # Ejemplo: cuatro columnas de ancho fijo

# Lee el archivo de texto con columnas de ancho fijo
datos = pd.read_fwf('prueba_txt.txt', colspecs=colspecs, header=None)

# for index, row in datos.iterrows():
#     print(' '.join(map(str, row)))

titulos = ['Marca', 'Tipo', 'Ubicacion', 'Placa']

df = pd.DataFrame(datos)   

df.rename(columns={0:titulos[0],
                   1:titulos[1],
                   2:titulos[2],
                   3:titulos[3]},
                   inplace=True)

    
def completar_numero(num):
    x = num.zfill(4)
    return x

df.insert(0, 'consecutivo', range(1, len(df) + 1))
df['fecha']='06/07/2019'
df['Placa']= df['Placa'].astype(str).apply(completar_numero)
print(df)  

nombre_archivo='csv_final.csv'
df.to_csv(nombre_archivo, index=False)  
