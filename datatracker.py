import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys
import pandas as pd

# Datos para poderme conectar a la API y generar el token de conexion.
cid = '91ad16bbfc67418e981a13c2b4db7381'
secret = 'd06a769ae55047158663a5253cb24e00'
username = 'eort98'
redirect_uri = 'http://localhost:3000'


# Como conectarse a la spotify app?

# 1. Definir privilegios para poder leer las diferentes funciones de la api

scope = 'user-top-read'
token = util.prompt_for_user_token(username,scope,cid,secret,redirect_uri)
sp = spotipy.Spotify(auth=token)

# 2. Adquirir la informacion que deseamos para este caso en especifico el top de canciones de Colombia separados por genero...
#Para este fin definire un array con algunos de los generos mas relevantes de Colombia
categories = sp.categories(country='CO', limit=50)['categories']['items']

#Estas son las diferentes categorias de Colombia
for category in categories:
    category_name = category['name']
    # print(f"ID:{category['id']}, category_name: {category_name}")


pais = 'CO'
# Aqui se obtinen  el top 10 de las canciones de cada categoria de Colombia


categories = sp.categories(country=pais, limit=50)['categories']['items']

diccionario={}

print("Espera mientras leemos el API ...")
for category in categories:
    category_id = category['id']
    try:
        playlists = sp.category_playlists(category_id=category_id, country=pais, limit=1)['playlists']['items']
        if playlists:
            playlist_id = playlists[0]['id']
            playlist_tracks = sp.playlist_tracks(playlist_id, limit=10)['items']
            categoria = category['name']
            canciones=[]
            for track in playlist_tracks:
                nombre_cancion = track['track']['name']
                artistas = ", ".join([artist['name'] for artist in track['track']['artists']])
                canciones.append((nombre_cancion, artistas))
            diccionario[categoria] = canciones
        else:
            print(f"No existe top para esta categoría en el país.")
    except Exception as excepcion:
        print(f"No se pudo obtener el top de canciones para la categoría {category['name']}: {str(excepcion)}")


for categoria, canciones in diccionario.items():
    print(f"\nCategoría: {categoria}")
    print(f"Top de Canciones en {pais}:")
    for cancion in canciones:
        nombre_cancion = cancion[0].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        artistas = cancion[1].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        print(f"{nombre_cancion} - {artistas}")

# Convertir el diccionario en un DataFrame
df = pd.DataFrame([(categoria, cancion[0], cancion[1]) for categoria, canciones in diccionario.items() for cancion in canciones],
                  columns=['Categoria', 'Cancion', 'Artista'])

grupos = df.groupby('Categoria')

try:
    for categoria, grupo in grupos:
        if categoria== "Dance/Electronic":
            categoria=" Dance Electronic"
        nombre_archivo = f"{categoria}.csv"
        grupo.to_csv(nombre_archivo, index=False)
except Exception as excepcion:
    print(f"No se pudo crear el archivo ya que no existe info para cargar en este: {str(excepcion)}")




