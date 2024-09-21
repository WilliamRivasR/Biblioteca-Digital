from tkinter import Tk, Label
from PIL import Image, ImageTk
import mysql.connector

def mostrar_imagen(id_imagen):
    # Conectar a la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        database='biblioteca_escolar',
        user='root',
        password='1234'
    )
    cursor = conexion.cursor()

    # Recuperar la ruta de la imagen de la base de datos
    sql = "SELECT nombre_imagen, ruta_imagen FROM imagenes WHERE id = %s"
    cursor.execute(sql, (id_imagen,))
    resultado = cursor.fetchone()

    nombre_imagen, ruta_imagen = resultado

    # Cargar la imagen desde el sistema de archivos
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)

    # Mostrar la imagen en Tkinter
    ventana = Tk()
    etiqueta = Label(ventana, image=imagen)
    etiqueta.pack()

    ventana.mainloop()

    cursor.close()
    conexion.close()

# Ejemplo de uso
mostrar_imagen(1)  # Muestra la imagen con ID 1
