import tkinter as tk
from tkinter import simpledialog, messagebox
from pytubefix import Playlist
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os


# Función para descargar el video en formato MP3
def descargar_video_en_mp3(url, formato):
    try:
        # Crear objeto YouTube
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)

        if formato == "HIGH":
            ys = yt.streams.get_highest_resolution()
        elif formato == "LOW":
            ys = yt.streams.get_lowest_resolution()
        elif formato == "AUDIO":
            ys = yt.streams.get_audio_only()
        else:
            print("FORMATO INCORRECTO")
            return None
        archivo_descargado = ys.download()

        if formato == "AUDIO":
            base, ext = os.path.splitext(archivo_descargado)
            nuevo_archivo = base + '.mp3'
            os.rename(archivo_descargado, nuevo_archivo)

        print(f"Descargado: {yt.title}")
        return yt.title
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return None


# Función para manejar la URL ingresada
def manejar_url(url, formato):
    if 'playlist' in url:
        # Si es una lista de reproducción
        try:
            playlist = Playlist(url)
            messagebox.showinfo("Información",
                                f"Descargando {len(playlist.video_urls)} videos de la lista de reproducción")
            for video_url in playlist.video_urls:
                descargar_video_en_mp3(video_url, formato)
            messagebox.showinfo("Completado", "Descarga de la lista completada")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la lista de reproducción: {e}")
    else:
        # Si es un video individual
        video_title = descargar_video_en_mp3(url, formato)
        if video_title:
            messagebox.showinfo("Completado", f"Descargado: {video_title}")
        else:
            messagebox.showerror("Error", "Error al descargar el video")


def elegir_formato(root):
    # Variable para almacenar el formato seleccionado
    formato_seleccionado = tk.StringVar()

    # Crear una nueva ventana
    ventana_formato = tk.Toplevel(root)
    ventana_formato.title("Elija el formato")

    # Etiqueta de instrucción
    etiqueta = tk.Label(ventana_formato, text="Elija el formato:")
    etiqueta.pack(pady=10)

    # Función para manejar la selección del formato
    def seleccionar_formato(formato):
        formato_seleccionado.set(formato)
        ventana_formato.destroy()  # Cerrar la ventana después de seleccionar el formato

    # Botones para los formatos
    boton_audio = tk.Button(ventana_formato, text="AUDIO", command=lambda: seleccionar_formato("AUDIO"))
    boton_audio.pack(pady=5)

    boton_high = tk.Button(ventana_formato, text="HIGH RESOLUTION", command=lambda: seleccionar_formato("HIGH"))
    boton_high.pack(pady=5)

    boton_low = tk.Button(ventana_formato, text="LOW RESOLUTION", command=lambda: seleccionar_formato("LOW"))
    boton_low.pack(pady=5)

    # Mantener la ventana abierta hasta que se elija un formato
    ventana_formato.wait_window(ventana_formato)

    # Devolver el formato seleccionado
    return formato_seleccionado.get()


# Crear ventana emergente para ingresar la URL
def pedir_url():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    url = simpledialog.askstring("URL de YouTube", "Ingresa la URL del video o lista de reproducción:")
    if url:
        formato = elegir_formato(root)
        manejar_url(url,formato)
    else:
        messagebox.showwarning("Advertencia", "No se ingresó ninguna URL")


# Ejecutar el programa
if __name__ == "__main__":
    pedir_url()
