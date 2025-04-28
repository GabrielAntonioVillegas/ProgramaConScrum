from   tkinter   import *
from   tkinter   import ttk
from   tkinter   import messagebox
from   functools import partial
from   tkinter   import PhotoImage
from   tkinter   import font
import random
import time
import mysql.connector 
from mysql.connector import Error
#FUNCIONES========================================
#--------------------Centrar Pantalla
def centrarPantalla(ancho,alto,app):
    ancho_pantalla = app.winfo_screenwidth()
    alto_pantalla = app.winfo_screenheight()

    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)

    app.geometry(f"{ancho}x{alto}+{x}+{y}")
#--------------------Conexion a Base de Datos
def conexionBaseDatos():
    try:
        conexion = mysql.connector.connect(
            host="boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com",          
            user="u1s6xofortb1nhmx",                                              
            password="TIjcUe5NAXwsr8Rtu8U8",                                      
            database="boznowy5qzijb8uhhqoj"                                       
        )     
        cursor = conexion.cursor()

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    finally:
        cursor.close()
        conexion.close()
        print("Se cerró la conexion con exito")
#--------------------Menu Principal
def creacionPantalla_Principal(app,fuente):
    #------Bienvenidos
    lbl_1 = Label(app, text="Bienvenido", font=(fuente,20,"bold"))
    lbl_1.place(relx=0.5, y=100, anchor="center")
    #------Iniciar Sesion
    btn_InSe = Button(app,text="Iniciar Sesion",font=(fuente,14,"bold"))
    btn_InSe.place(relx=0.5, y= 200, anchor="center", width=200)
    #------Registrarse
    btn_Regis = Button(app,text="Registrarse",font=(fuente,14,"bold"))
    btn_Regis.place(relx=0.5, y= 280, anchor="center", width=200)
#Programa Principal===============================
app = Tk()
app.title("Menu Principal")
#--------------(ancho,alto,app)
centrarPantalla(500,500,app)
#--------------Definicion de Fuentes
fuente= ("Source Code Pro")

creacionPantalla_Principal(app,fuente)

app.mainloop()