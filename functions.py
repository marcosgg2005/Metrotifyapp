import requests
import uuid
import re


class Usuario:
    def __init__(self, nombre, correo, tipo_usuario,id=None):
        self.nombre = nombre
        self.correo = correo
        self.tipo_usuario = tipo_usuario
        self.likes = []  # Lista de IDs de usuarios que dieron like
        self.like_count = 0  # Contador de likes

        if id is None:
            self.id = str(uuid.uuid4())  # Genera un ID único
        else:
            self.id = id

    def add_like(self, user_id):
        if user_id not in self.likes:
            self.likes.append(user_id)
            self.like_count += 1

    def remove_like(self, user_id):
        if user_id in self.likes:
            self.likes.remove(user_id)
            self.like_count -= 1

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
        self.likes = []  # Lista de IDs de usuarios que dieron like
        self.like_count = 0  # Contador de likes
    def to_string(self):
        return f"{self.nombre},{self.correo},{self.tipo_usuario},{self.like_count}"


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
        self.likes = []  # Lista de IDs de usuarios que dieron like
        self.like_count = 0  # Contador de likes

    def add_like(self, user_id):
        if user_id not in self.likes:
            self.likes.append(user_id)
            self.like_count += 1

    def remove_like(self, user_id):
        if user_id in self.likes:
            self.likes.remove(user_id)
            self.like_count -= 1

    def to_string(self):
        tracklist_string = "\n".join([track.to_string() for track in self.tracklist])
        return f"{self.id},{self.name},{self.description},{self.cover},{self.published},{self.genre},{self.artist}\n{tracklist_string}"


class Track:
    def __init__(self, id, name, duration, link):
        self.id = id
        self.name = name
        self.duration = duration
        self.link = link
        self.likes = []  # Lista de IDs de usuarios que dieron like
        self.like_count = 0  # Contador de likes

    def add_like(self, user_id):
        if user_id not in self.likes:
            self.likes.append(user_id)
            self.like_count += 1

    def remove_like(self, user_id):
        if user_id in self.likes:
            self.likes.remove(user_id)
            self.like_count -= 1

    def to_string(self):
        return f"{self.id},{self.name},{self.duration},{self.link},{self.like_count}"


class Playlist:
    def __init__(self, id, name, description, creator, tracks):
        self.id = id
        self.name = name
        self.description = description
        self.creator = creator
        self.tracks = tracks
        self.likes = []  # Lista de IDs de usuarios que dieron like
        self.like_count = 0  # Contador de likes

    def add_like(self, user_id):
        if user_id not in self.likes:
            self.likes.append(user_id)
            self.like_count += 1

    def remove_like(self, user_id):
        if user_id in self.likes:
            self.likes.remove(user_id)
            self.like_count -= 1

    def to_string(self):
        tracks_string = ",".join([track.id for track in self.tracks])
        return f"{self.id},{self.name},{self.description},{self.creator},{tracks_string},{self.like_count}"
        


# Mapeo de tipos de usuario
tipo_usuario_map = {
    "Escucha": "listener",
    "Músico": "musician"
}

# Mapeo inverso de tipos de usuario
tipo_usuario_map_inverso = {
    "listener": "Escucha",
    "musician": "Músico"
}
class Metrotify:
    def __init__(self):
        self.usuarios = []
        self.albums = []
        self.playlists = []

    def get_users(self):
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
                if not any(u.correo == usuario["email"] for u in self.usuarios):
                    self.usuarios.append(Usuario(usuario["id"], usuario["name"], usuario["email"], usuario["type"]))

    def get_albums(self):
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
                # Verificar si el álbum ya existe en la lista
                if not any(a.id == album["id"] for a in self.albums):
                    tracklist = [Track(**track) for track in album["tracklist"]]
                    self.albums.append(Album(album["id"], album["name"], album["description"], album["cover"], album["published"], album["genre"], album["artist"], tracklist))

    def get_playlists(self):
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
                # Verificar si la playlist ya existe en la lista
                if not any(p.id == playlist["id"] for p in self.playlists):
                    self.playlists.append(Playlist(playlist["id"], playlist["name"], playlist["description"], playlist["creator"], playlist["tracks"]))

    def guardar_objeto(self, objeto, archivo):
        # Guarda el objeto en el archivo correspondiente
        # Verificar el tipo de objeto y llamar al método to_string correspondiente
        if isinstance(objeto, Album):
            data = objeto.to_string()
            # Escribir los datos en el archivo
            with open(archivo, 'a', encoding='utf-8') as f:
                f.write(data + "\n")

                    
   
    
    def guardar_usuarios(self):
        with open('usuarios.txt', 'w', encoding='utf-8', errors='ignore') as f:
            for usuario in self.usuarios:
                f.write(f"{usuario.id},{usuario.nombre},{usuario.correo},{usuario.tipo_usuario}\n")

    def cargar_usuarios(self):
        try:
            with open('usuarios.txt', 'r', encoding='utf-8', errors='ignore') as f:
                for linea in f.readlines():
                    id, nombre, correo, tipo_usuario = linea.strip().split(',')
                    self.usuarios.append(Usuario(nombre, correo, tipo_usuario, id))
        except FileNotFoundError:   
            pass
    def guardar_albums(self):
        with open('albums.txt', 'w', encoding='utf-8', errors='ignore') as f:
            for album in self.albums:
                f.write(f"{album.id},{album.name},{album.description},{album.cover},{album.published},{album.genre},{album.artist}\n")
                for track in album.tracklist:
                    f.write(f"\t{track.id},{track.name},{track.duration},{track.link}\n")
                # Guardar los likes del álbum
                for like in album.likes:
                    f.write(f"\t\t{like}\n")

    def cargar_albums(self):
        try:
            with open('albums.txt', 'r', encoding='utf-8', errors='ignore') as f:
                album = None
                for linea in f.readlines():
                    datos = linea.strip().split(',')
                    if len(datos) == 7:
                        id, name, description, cover, published, genre, artist = datos
                        album = Album(id, name, description, cover, published, genre, artist, [])
                        self.albums.append(album)
                    elif len(datos) == 4 and album is not None:
                        id, name, duration, link = datos
                        album.tracklist.append(Track(id, name, duration, link))
                    elif len(datos) == 1 and album is not None:
                        # Cargar los likes del álbum
                        album.likes.append(datos[0])
                        album.like_count += 1
        except FileNotFoundError:   
            pass


    def guardar_playlists(self):
        with open('playlists.txt', 'w', encoding='utf-8', errors='ignore') as f:
            for playlist in self.playlists:
                tracks_string = ','.join(playlist.tracks)
                f.write(f"{playlist.id},{playlist.name},{playlist.description},{playlist.creator},{tracks_string}\n")

    def cargar_playlists(self):
        try:
            with open('playlists.txt', 'r', encoding='utf-8', errors='ignore') as f:
                for linea in f.readlines():
                    id, name, description, creator, tracks_string = linea.strip().split(',')
                    tracks = tracks_string.split(',')
                    self.playlists.append(Playlist(id, name, description, creator, tracks))
        except FileNotFoundError:   
            pass

    def registrar_usuario_interactivo(self):
        print("Por favor, llena los siguientes campos para registrarte:")
        nombre = input("Nombre (o Nombre artístico): ")
        correo = input("Correo electrónico: ")

        # Validación del correo electrónico
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            print("Correo electrónico no válido. Por favor, intenta de nuevo.")
            return None

        # Verificación de que el correo no esté ya registrado
        for usuario in self.usuarios:
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

        # Aquí usamos el mapeo para guardar el tipo de usuario correcto
        tipo_usuario_api = tipo_usuario_map[tipo_usuario]

        nuevo_usuario = Usuario(nombre, correo, tipo_usuario_api)
        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return nuevo_usuario

    def iniciar_sesion(self):
            correo = input("Por favor, introduce tu correo electrónico: ")
            for usuario in self.usuarios:
                if usuario.correo == correo:
                    print(f"Bienvenido de nuevo, {usuario.nombre}!")
                    return usuario
            print("Usuario no encontrado. Por favor, intentalo de nuevo.")
            return None

    def menu_usuario(self, usuario):
        while True:
            print("Bienvenido a METROTIFY, " + usuario.nombre)
            print("1. Ver perfil")
            
            # Aquí usamos el mapeo inverso para hacer la comparación correcta
            if tipo_usuario_map_inverso[usuario.tipo_usuario] == "Músico":
                print("2. Crear álbum")
            elif tipo_usuario_map_inverso[usuario.tipo_usuario] == "Escucha":
                print("2. Crear playlist")
            print("3. Buscar")
            print("4. Salir")
            opcion = input("Por favor, selecciona una opción: ")
        
            if opcion == "1":
                self.ver_perfil(usuario)
            elif opcion == "2":
                if tipo_usuario_map_inverso[usuario.tipo_usuario] == "Músico":
                    self.crear_album(usuario)
                elif tipo_usuario_map_inverso[usuario.tipo_usuario] == "Escucha":
                    self.crear_playlist(usuario)
            elif opcion == "3":
                tipo_busqueda = input("Introduce el tipo de búsqueda (usuario, album, cancion, playlist): ")
                termino_busqueda = input("Introduce el término de búsqueda: ")
                resultados = self.buscar(tipo_busqueda, termino_busqueda)
                if resultados:
                    print(f"{tipo_busqueda} encontrado:")
                    if tipo_busqueda == "album":
                        for i, album in enumerate(resultados, 1):
                            print(f"{i}. {album.name}")
                        indice = int(input("Selecciona el número del álbum que quieres ver: ")) - 1
                        album_seleccionado = resultados[indice]
                        print("Canciones en el álbum seleccionado:")
                        for track in album_seleccionado.tracklist:
                            print((track.name, track.link))
                        # Agregar opción para dar like o dislike al álbum
                        if usuario.id in album_seleccionado.likes:
                            opcion_like = input("¿Quieres quitar tu 'like' a este álbum? (s/n): ")
                            if opcion_like.lower() == 's':
                                album_seleccionado.remove_like(usuario.id)  # Aquí se llama a remove_like
                                print("Has quitado tu 'like' a este álbum.")
                                self.guardar_albums()  # Guardar los álbumes después de modificar los 'likes'
                        else:
                            opcion_like = input("¿Quieres dar 'like' a este álbum? (s/n): ")
                            if opcion_like.lower() == 's':
                                album_seleccionado.add_like(usuario.id)  # Aquí se llama a add_like
                                print("Has dado 'like' a este álbum.")
                                self.guardar_albums()  # Guardar los álbumes después de modificar los 'likes'
                    else:
                        for i, resultado in enumerate(resultados, 1):
                            print(f"{i}. {resultado.nombre if hasattr(resultado, 'nombre') else resultado[0]}")
                        indice = int(input("Selecciona el número del objeto que quieres ver: ")) - 1
                        objeto_seleccionado = resultados[indice]
                        # Agregar opción para dar like o dislike al objeto
                        if usuario.id in objeto_seleccionado.likes:
                            opcion_like = input("¿Quieres quitar tu 'like' a este objeto? (s/n): ")
                            if opcion_like.lower() == 's':
                                objeto_seleccionado.remove_like(usuario.id)
                                print("Has quitado tu 'like' a este objeto.")
                                self.guardar_albums()  # Guardar los álbumes después de modificar los 'likes'
                        else:
                            opcion_like = input("¿Quieres dar 'like' a este objeto? (s/n): ")
                            if opcion_like.lower() == 's':
                                objeto_seleccionado.add_like(usuario.id)
                                print("Has dado 'like' a este objeto.")
                                self.guardar_albums()  # Guardar los álbumes después de modificar los 'likes'
                else:
                    print(f"{tipo_busqueda} no encontrado.")
            elif opcion == "4":
                print("Has cerrado tu sesión. ¡Hasta luego!")



    def dar_like(self, usuario, objeto):
        if usuario.id not in objeto.likes:
            objeto.add_like(usuario.id)
            print("Has dado 'like' a este objeto.")
            self.guardar_objeto(objeto, 'albums.txt')  # Guardar el objeto después de dar/quitar "like"

    def quitar_like(self, usuario, objeto):
        if usuario.id in objeto.likes:
            objeto.remove_like(usuario.id)
            print("Has quitado tu 'like' a este objeto.")
            self.guardar_objeto(objeto, 'albums.txt')  # Guardar el objeto después de dar/quitar "like"


    def buscar(self, tipo, termino):
            resultados = []
            if tipo == "usuario":
                for usuario in self.usuarios:
                    if termino.lower() in usuario.nombre.lower():
                        # Agregamos el usuario a la lista de resultados
                        resultados.append((usuario.nombre, tipo_usuario_map_inverso[usuario.tipo_usuario]))

            elif tipo == "album":
                for album in self.albums:
                    if termino.lower() in album.name.lower():
                        resultados.append(album)
                        
            elif tipo == "cancion":
                for album in self.albums:
                    for track in album.tracklist:
                        if termino.lower() in track.name.lower():
                            resultados.append((track.name, track.link))

            elif tipo == "playlist":
                for playlist in self.playlists:
                    if termino.lower() in playlist.name.lower():
                        # Creamos una lista para guardar los nombres de las canciones
                        nombres_canciones = []
                        for id_cancion in playlist.tracks:
                            nombre_cancion = self.buscar_cancion_por_id(id_cancion)
                            if nombre_cancion is not None:
                                nombres_canciones.append(nombre_cancion)
                        # Agregamos la playlist y los nombres de las canciones a los resultados
                        resultados.append((playlist.name, nombres_canciones))

            else:
                print("Tipo de búsqueda no válido. Los tipos válidos son 'usuario', 'album', 'cancion' y 'playlist'.")
                return None

            if not resultados:
                print(f"No se encontró {tipo} con el nombre '{termino}'.")
                return None

            return resultados

            
    def crear_playlist(self, usuario):
        print("Por favor, introduce los detalles de la playlist:")
        name = input("Nombre: ")
        description = input("Descripción: ")
        creator = usuario.nombre

        tracks = []
        while True:
            print("1. Añadir canción por nombre")
            print("2. Añadir canciones de un artista")
            print("3. Terminar y guardar playlist")
            opcion = input("Por favor, selecciona una opción: ")

            if opcion == "1":
                termino_busqueda = input("Introduce el nombre de la canción: ")
                resultados = self.buscador_playlist("cancion", termino_busqueda)
                if resultados:
                    print("Canciones encontradas:")
                    for i, (nombre, id) in enumerate(resultados, 1):
                        print(f"{i}. {nombre}")
                    indice = int(input("Selecciona el número de la canción que quieres añadir: ")) - 1
                    tracks.append(resultados[indice][1])  # Añadimos el id de la canción
                else:
                    print("No se encontró ninguna canción con ese nombre.")
            elif opcion == "2":
                termino_busqueda = input("Introduce el nombre del artista: ")
                resultados = self.buscador_playlist("artista", termino_busqueda)
                if resultados:
                    print("Canciones encontradas:")
                    for i, (nombre, id) in enumerate(resultados, 1):
                        print(f"{i}. {nombre}")
                    indices = input("Selecciona los números de las canciones que quieres añadir (separados por comas): ").split(',')
                    for indice in indices:
                        tracks.append(resultados[int(indice) - 1][1])  # Añadimos el id de la canción
                else:
                    print("No se encontró ninguna canción de ese artista.")
            elif opcion == "3":
                break
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")

        playlist = Playlist(str(uuid.uuid4()), name, description, creator, tracks)
        self.playlists.append(playlist)
        self.guardar_playlists()  # Guardar las playlists después de crear una nueva
        print("Playlist creada y guardada exitosamente!")

    def buscador_playlist(self, tipo, termino):
        resultados = []
        if tipo == "cancion":
            for album in self.albums:
                for track in album.tracklist:
                    if termino.lower() in track.name.lower():
                        # Agregamos el nombre y el id de la canción a los resultados
                        resultados.append((track.name, track.id))
        elif tipo == "artista":
            for album in self.albums:
                if termino.lower() in album.artist.lower():
                    for track in album.tracklist:
                        # Agregamos el nombre y el id de la canción a los resultados
                        resultados.append((track.name, track.id))
        else:
            print("Tipo de búsqueda no válido. Los tipos válidos son 'cancion' y 'artista'.")
            return None

        if not resultados:
            print(f"No se encontró {tipo} con el nombre '{termino}'.")
            return None

        return resultados

    def crear_album(self, usuario):
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
        self.albums.append(album)
        self.guardar_albums()  # Guardar los álbumes después de crear uno nuevo
        print("Álbum creado y guardado exitosamente!")

    def cambiar_informacion(self, usuario):
        print("Por favor, llena los siguientes campos para actualizar tu información:")
        nombre = input("Nombre (o Nombre artístico): ")
        correo = input("Correo electrónico: ")

        # Validación del correo electrónico
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            print("Correo electrónico no válido. Por favor, intenta de nuevo.")
            return

        # Verificación de que el correo no esté ya registrado
        for u in self.usuarios:
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

        # Aquí usamos el mapeo para guardar el tipo de usuario correcto
        tipo_usuario_api = tipo_usuario_map[tipo_usuario]

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.tipo_usuario = tipo_usuario_api
        self.guardar_usuarios()

    def borrar_datos(self, usuario):
        self.usuarios.remove(usuario)
        self.guardar_usuarios()
        print("Tus datos han sido borrados. ¡Hasta luego!")
        return None

    def ver_perfil(self, usuario):
        while True:
            print(f"Nombre: {usuario.nombre}")
            print(f"Correo: {usuario.correo}")
            print(f"Tipo de usuario: {usuario.tipo_usuario}")

            print("1. Cambiar la información personal de la cuenta")
            print("2. Borrar los datos de la cuenta")
            print("3. Regresar")
            opcion = input("Por favor, selecciona una opción (1, 2 o 3): ")

            if opcion == "1":
                self.cambiar_informacion(usuario)
            elif opcion == "2":
                usuario = self.borrar_datos(usuario)
                if usuario is None:
                    return
            elif opcion == "3":
                # No hacer nada, simplemente regresar al menú anterior
                return
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")

    def buscar_cancion_por_id(self, id):
        for album in self.albums:
            for track in album.tracklist:
                if track.id == id:
                    return track.name, track.link
        return None
            
    def guardar_tracks(self):
     with open('tracks.txt', 'w') as f:
        for track in self.tracks:
            likes_string = ','.join(track.likes)
            f.write(f"{track.id},{track.name},{track.duration},{track.link},{likes_string}\n")
            
    def cargar_tracks(self):
        try:
            with open('tracks.txt', 'r') as f:
                for linea in f.readlines():
                    id, name, duration, link, likes_string = linea.strip().split(',')
                    likes = likes_string.split(',')
                    self.tracks.append(Track(id, name, duration, link, likes))
        except FileNotFoundError:   
            pass



if __name__ == "__main__":

        app = Metrotify()
        app.cargar_usuarios()
        app.cargar_albums()
        app.cargar_playlists()
        app.get_users()
        app.get_albums()
        app.get_playlists()

        usuario = None  # Variable para rastrear el usuario actual

        while True:
            if usuario is None:  # Si no hay un usuario actual, mostrar el menú de inicio de sesión/registro
                print("Bienvenido a METROTIFY")
                print("1. Iniciar sesión")
                print("2. Registrarse")
                print("3. Salir")
                opcion = input("Por favor, selecciona una opción (1, 2 o 3): ")

                if opcion == "1":
                    usuario = app.iniciar_sesion()

                elif opcion == "2":
                    usuario = app.registrar_usuario_interactivo()

                elif opcion == "3":
                    print("Gracias por usar METROTIFY. ¡Hasta luego!")
                    break
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            else:  # Si hay un usuario actual, mostrar el menú de usuario
                app.menu_usuario(usuario)
                usuario = None