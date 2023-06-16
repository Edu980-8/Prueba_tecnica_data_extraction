import pandas as pd
from datetime import datetime


datos = pd.read_excel('consumo_prueba_2019.xls')
#print(datos)
df = pd.DataFrame(datos)

#AQUI SE OBTIENEN LOS TITULOS DE LAS COLUMNAS
new_header = df.iloc[7].dropna()
new_header=new_header[1:]
encabezado = new_header.reset_index(drop=True).tolist()
#AQUI SE ASIGNAN LOS TITULOS AL NUEVO DATAFRAME
df_nuevo = pd.DataFrame(columns=encabezado)
print(df_nuevo)


#Leer la cantidad de ventas fara hacer las lecturas en base a esos valores

index_ventas = [12,18,27]
ventas=[]

for i in index_ventas:
    fila = df.iloc[i].dropna()
    ventas.append(fila[0])
print(ventas)
     
ventas_sin_texto = [int(venta.replace("No. Ventas: ", "")) for venta in ventas]
print(f"Numero de ventas: {ventas_sin_texto}")

lim_up = [x - y for x, y in zip(index_ventas, ventas_sin_texto)]
print(f"Indice superior lectura: {lim_up}")
print(f"Indice inferior lectura:{index_ventas}")

lecturas = {}
filas=[]

for i in range(0,3):
    for j in range(lim_up[i],index_ventas[i]):
        fila = df.iloc[j].dropna()
        filas.append(fila)
    lectura_df = pd.concat(filas, axis=1).transpose()
    lecturas[i] = lectura_df



# Toca es renombrar las columnas con rename y los nuevos nombres...

nombres_actuales = lecturas[2].columns.tolist()
print(nombres_actuales)
nombres_nuevos = encabezado
print(encabezado)


if len(nombres_actuales) == len(nombres_nuevos):
    # Asignar los nuevos nombres de columnas al dataframe
    lecturas[2].columns = nombres_nuevos
    print("Nombres de columnas actualizados con éxito.")
    
    lecturas[2]['Factura'] = "COLS"
    lecturas[2]['Fecha'] = pd.to_datetime(lecturas[2]['Fecha'])
    lecturas[2]['Fecha'] = lecturas[2]['Fecha'].dt.strftime('%d/%m/%Y')
    
    data = {'Estacion': [''] * 13}
    df = pd.DataFrame(data)

    
    lecturas[2]['Estacion']=""
    
    # Asignar los valores correspondientes a los rangos específicos
    lecturas[2].loc[8:11, 'Estacion'] = 'SOL'
    lecturas[2].loc[15:17, 'Estacion'] = 'AIRES'
    lecturas[2].loc[21:26, 'Estacion'] = 'URT'

    print(lecturas[2].to_string())
    
    lecturas[2].to_csv("respuesta_reto_3.csv",sep=';',index = False, mode='a')
    

    
    
else:
    print("Error: El número de nombres actuales y nuevos no coincide.")

   



