import requests
import uuid
import re
class Usuario:
    def __init__(self, nombre, correo, tipo_usuario):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.correo = correo
        self.tipo_usuario = tipo_usuario

import uuid

class Track:
    def __init__(self, id, name, duration, link):
        self.id = id
        self.name = name
        self.duration = duration
        self.link = link
        self.likes = 0 
        
            
    def like(self):
        self.likes += 1  # Incrementa el número de likes en 1

class Album:
    def __init__(self, id, name, description, cover, published, genre, artist, tracklist):
        self.id = id
        self.name = name
        self.description = description
        self.cover = cover
        self.published = published
        self.genre = genre
        self.artist = artist
        self.tracklist = tracklist

class Playlist:
    def __init__(self, id, name, description, creator, tracks):
        self.id = id
        self.name = name
        self.description = description
        self.creator = creator
        self.tracks = tracks


usuarios = []

def get_users():
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as err:
        print(f"Ocurrió un error: {err}")
    else:
        usuarios_json = response.json()
        for usuario in usuarios_json:
            usuarios.append(Usuario(usuario["name"], usuario["email"], usuario["type"]))
            


albums = []

def get_albums():
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/albums.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as err:
        print(f"Ocurrió un error: {err}")
    else:
        albums_json = response.json()
        for album in albums_json:
            tracklist = [Track(**track) for track in album["tracklist"]]
            albums.append(Album(album["id"], album["name"], album["description"], album["cover"], album["published"], album["genre"], album["artist"], tracklist))


playlists = []

def get_playlists():
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/playlists.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as err:
        print(f"Ocurrió un error: {err}")
    else:
        playlists_json = response.json()
        for playlist in playlists_json:
            playlists.append(Playlist(playlist["id"], playlist["name"], playlist["description"], playlist["creator"], playlist["tracks"]))



def guardar_usuarios():
    with open('usuarios.txt', 'w') as f:
        for usuario in usuarios:
            f.write(f"{usuario.nombre},{usuario.correo},{usuario.tipo_usuario}\n")

def guardar_albums():
    with open('albums.txt', 'w') as f:
        for album in albums:
            f.write(f"{album.id},{album.name},{album.description},{album.cover},{album.published},{album.genre},{album.artist}\n")
            for track in album.tracklist:
                f.write(f"\t{track.id},{track.name},{track.duration},{track.link}\n")

def cargar_albums():
    try:
        with open('albums.txt', 'r') as f:
            album = None
            for linea in f.readlines():
                datos = linea.strip().split(',')
                if len(datos) == 7:
                    # This is an album line
                    id, name, description, cover, published, genre, artist = datos
                    album = Album(id, name, description, cover, published, genre, artist, [])
                    albums.append(album)
                elif len(datos) == 4 and album is not None:
                    # This is a track line
                    id, name, duration, link = datos
                    album.tracklist.append(Track(id, name, duration, link))
    except FileNotFoundError:
        pass


def guardar_playlists():
    with open('playlists.txt', 'w') as f:
        for playlist in playlists:
            f.write(f"{playlist.id},{playlist.name},{playlist.description},{playlist.creator}\n")
            for track_id in playlist.tracks:
                f.write(f"\t{track_id}\n")

def cargar_playlists():
    try:
        with open('playlists.txt', 'r') as f:
            playlist = None
            for linea in f.readlines():
                datos = linea.strip().split(',')
                if len(datos) == 4:
                    # This is a playlist line
                    id, name, description, creator = datos
                    playlist = Playlist(id, name, description, creator, [])
                    playlists.append(playlist)
                elif len(datos) == 1 and playlist is not None:
                    # This is a track line
                    track_id = datos[0]
                    playlist.tracks.append(track_id)
    except FileNotFoundError:
        pass


def crear_playlist(usuario):
    print("Por favor, introduce los detalles de la playlist:")
    name = input("Nombre: ")
    description = input("Descripción: ")
    creator = usuario.nombre
    tracks = input("Pistas (separadas por comas): ").split(',')
    playlist = Playlist(str(uuid.uuid4()), name, description, creator, tracks)
    playlists.append(playlist)
    guardar_playlists()  # Guardar las playlists después de crear una nueva
    print("Playlist creada y guardada exitosamente!")


def cargar_usuarios():
    try:
        with open('usuarios.txt', 'r') as f:
            for linea in f.readlines():
                nombre, correo, tipo_usuario = linea.strip().split(',')
                usuarios.append(Usuario(nombre, correo, tipo_usuario))
    except FileNotFoundError:
        pass



def crear_album(usuario):
    print("Por favor, introduce los detalles del álbum:")
    name = input("Nombre: ")
    description = input("Descripción: ")
    cover = input("Portada del álbum [link]: ")
    published = input("Fecha de publicación: ")
    genre = input("Género predominante: ")
    artist = usuario.nombre
    tracklist = []
    while True:
        track_name = input("Nombre de la canción (pon los nombes de las canciones uno por uno, cuando termines deja en blanco y press enter): ")
        if track_name == "":
            break
        track_duration = input("Duración en minutos: ")
        track_link = input("Link de la canción: ")
        tracklist.append(Track(str(uuid.uuid4()), track_name, track_duration, track_link))
    album = Album(str(uuid.uuid4()), name, description, cover, published, genre, artist, tracklist)
    albums.append(album)
    guardar_albums()  # Guardar los álbumes después de crear uno nuevo
    print("Álbum creado y guardado exitosamente!")



def registrar_usuario_interactivo():
    print("Por favor, llena los siguientes campos para registrarte:")
    nombre = input("Nombre (o Nombre artístico): ")
    correo = input("Correo electrónico: ")

    # Validación del correo electrónico
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        print("Correo electrónico no válido. Por favor, intenta de nuevo.")
        return None

    # Verificación de que el correo no esté ya registrado
    for usuario in usuarios:
        if usuario.correo == correo:
            print("Este correo electrónico ya está registrado. Por favor, intenta con otro.")
            return None

    print("Tipo de Usuario: ")
    print("1. Músico")
    print("2. Escucha")
    tipo_usuario = input("Por favor, selecciona una opción (1 o 2): ")
    if tipo_usuario == "1":
        tipo_usuario = "Músico"
    elif tipo_usuario == "2":
        tipo_usuario = "Escucha"
    else:
        print("Opción no válida. Por favor, intenta de nuevo.")
        return None

    nuevo_usuario = Usuario(nombre, correo, tipo_usuario)
    usuarios.append(nuevo_usuario)
    guardar_usuarios()
    return nuevo_usuario

def iniciar_sesion():
    correo = input("Por favor, introduce tu correo electrónico: ")
    for usuario in usuarios:
        if usuario.correo == correo:
            print(f"Bienvenido de nuevo, {usuario.nombre}!")
            return usuario
    print("Usuario no encontrado. Por favor, intentalo de nuevo.")
    return None


def buscar_usuario(nombre):
    for usuario in usuarios:
        if usuario.nombre == nombre:
            return usuario
    return None

def cambiar_informacion(usuario):
    print("Por favor, llena los siguientes campos para actualizar tu información:")
    nombre = input("Nombre (o Nombre artístico): ")
    correo = input("Correo electrónico: ")

    # Validación del correo electrónico
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        print("Correo electrónico no válido. Por favor, intenta de nuevo.")
        return

    # Verificación de que el correo no esté ya registrado
    for u in usuarios:
        if u.correo == correo and u.id != usuario.id:
            print("Este correo electrónico ya está registrado. Por favor, intenta con otro.")
            return

    print("Tipo de Usuario: ")
    print("1. Músico")
    print("2. Escucha")
    tipo_usuario = input("Por favor, selecciona una opción (1 o 2): ")
    if tipo_usuario == "1":
        tipo_usuario = "Músico"
    elif tipo_usuario == "2":
        tipo_usuario = "Escucha"
    else:
        print("Opción no válida. Por favor, intenta de nuevo.")
        return

    usuario.nombre = nombre
    usuario.correo = correo
    usuario.tipo_usuario = tipo_usuario
    guardar_usuarios()

def borrar_datos(usuario):
    usuarios.remove(usuario)
    guardar_usuarios()
    print("Tus datos han sido borrados. ¡Hasta luego!")
    return None

def ver_perfil(usuario):
    while True:
        print(f"Nombre: {usuario.nombre}")
        print(f"Correo: {usuario.correo}")
        print(f"Tipo de usuario: {usuario.tipo_usuario}")

        print("1. Cambiar la información personal de la cuenta")
        print("2. Borrar los datos de la cuenta")
        print("3. Regresar")
        opcion = input("Por favor, selecciona una opción (1, 2 o 3): ")

        if opcion == "1":
            cambiar_informacion(usuario)
        elif opcion == "2":
            usuario = borrar_datos(usuario)
            if usuario is None:
                return
        elif opcion == "3":
            # No hacer nada, simplemente regresar al menú anterior
            return
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
        
def buscar(tipo, termino):
    if tipo == "musico":
        for usuario in usuarios:
            if usuario.nombre.lower() == termino.lower() and usuario.tipo_usuario == "Músico":
                return usuario
    elif tipo == "album":
        for album in albums:
            if album.name.lower() == termino.lower():
                return album
    elif tipo == "cancion":
        for album in albums:
            for track in album.tracklist:
                if track.name.lower() == termino.lower():
                    return track
    elif tipo == "playlist":
        for playlist in playlists:
            if playlist.name.lower() == termino.lower():
                return playlist
    else:
        print("Tipo de búsqueda no válido. Los tipos válidos son 'musico', 'album', 'cancion' y 'playlist'.")
        return None

    print(f"No se encontró {tipo} con el nombre '{termino}'.")
    return None


def menu_usuario(usuario):
    while True:
        print("Bienvenido a METROTIFY, " + usuario.nombre)
        print("1. Buscar usuario")
        print("2. Ver perfil")
        if usuario.tipo_usuario == "Músico":
            print("3. Crear álbum")
        elif usuario.tipo_usuario == "Escucha":
            print("3. Crear playlist")
        print("4. Buscar")
        print("5. Salir")
        opcion = input("Por favor, selecciona una opción: ")

        if opcion == "1":
            nombre = input("Introduce el nombre del usuario que quieres buscar: ")
            usuario_buscado = buscar_usuario(nombre)
            if usuario_buscado:
                print("Usuario encontrado:")
                print(usuario_buscado)
            else:
                print("Usuario no encontrado.")
        elif opcion == "2":
            ver_perfil(usuario)
        elif opcion == "3":
            if usuario.tipo_usuario == "Músico":
                crear_album(usuario)
            elif usuario.tipo_usuario == "Escucha":
                crear_playlist(usuario)
        elif opcion == "4":
            tipo_busqueda = input("Introduce el tipo de búsqueda (musico, album, cancion, playlist): ")
            termino_busqueda = input("Introduce el término de búsqueda: ")
            resultado = buscar(tipo_busqueda, termino_busqueda)
            if resultado:
                print(f"{tipo_busqueda} encontrado:")
                print(resultado)
            else:
                print(f"{tipo_busqueda} no encontrado.")
        elif opcion == "5":
            print("Has cerrado tu sesión. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def main():
    cargar_usuarios()
    cargar_albums()
    get_users()
    get_albums()
    usuario = None  # Variable para rastrear el usuario actual

    while True:
        if usuario is None:  # Si no hay un usuario actual, mostrar el menú de inicio de sesión/registro
            print("Bienvenido a METROTIFY")
            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Por favor, selecciona una opción (1, 2 o 3): ")

            if opcion == "1":
                usuario = iniciar_sesion()
                print(usuario)
            elif opcion == "2":
                usuario = registrar_usuario_interactivo()
                print(usuario)
            elif opcion == "3":
                print("Gracias por usar METROTIFY. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")
        else:  # Si hay un usuario actual, mostrar el menú de usuario
            menu_usuario(usuario)
            usuario = None  # Restablecer el usuario a None después de cerrar la sesión

if __name__ == "__main__":
    main()

