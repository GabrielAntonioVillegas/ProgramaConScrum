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
#VARIABLES GLOBALES===============================
vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]
#FUNCIONES========================================
def iniciarConexion(vectorConexion):
    conexion = mysql.connector.connect(
        host= vectorConexion[0],
        user= vectorConexion[1],
        password= vectorConexion[2],
        database= vectorConexion[3]
    )
    return conexion
#--------------------Centrar Pantalla
def centrarPantalla(ancho,alto,app):
    ancho_pantalla = app.winfo_screenwidth()
    alto_pantalla = app.winfo_screenheight()

    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)

    app.geometry(f"{ancho}x{alto}+{x}+{y}")
#--------------------Cerrar Ventana
def cerrar_abrirVentanas(app1,app2):
    app1.destroy()   #Ventana a Cerrar
    #app2.withdraw()  #Ocultar Ventana
    #Para poder usar deiconify, la ventana a reaparecer debe primero ser ocultada con .withdraw()
    app2.deiconify() #Reaparecer Ventana
#--------------------Pantalla Menu Principal
def creacionPantalla_Principal(app,fuente):
    #Bienvenidos
    lbl_1 = Label(app, text="Bienvenido", font=(fuente,20,"bold"))
    lbl_1.place(relx=0.5, y=100, anchor="center")
    #Iniciar Sesion
    btn_InSe = Button(app,text="Iniciar Sesion",font=(fuente,14,"bold"), 
                      command=partial(creacionPantalla_IniciarSesion,app,fuente))
    btn_InSe.place(relx=0.5, y= 200, anchor="center", width=200)
    #Registrarse
    btn_Regis = Button(app,text="Registrarse",font=(fuente,14,"bold"),
                       command=partial(creacionPantalla_Registrarse,app,fuente))
    btn_Regis.place(relx=0.5, y= 280, anchor="center", width=200)
    #Iniciar Sesion como Organizador
    btn_Inse_Org = Button(app,text="¿Es Organizador de Eventos? Inicie Sesion Aquí", font=(fuente,9), relief="ridge",
                          command=partial(creacionPantalla_IniciarSesionOrganizador,app,fuente))
    btn_Inse_Org.place(relx=0.5, y= 360, anchor="center")
#--------------------Pantalla Iniciar Sesion
def creacionPantalla_IniciarSesion(app,fuente):
    app_Inse= Toplevel(app)
    app_Inse.title("Iniciar Sesion") 
    centrarPantalla(500,500,app_Inse)

    btn_volver = Button(app_Inse, text="🡸", command=partial(cerrar_abrirVentanas,app_Inse,app))
    btn_volver.place(x=10,y=10)

    lbl = Label(app_Inse, text="Iniciar Sesión", font=(fuente,20,"bold"))
    lbl.place(relx=0.5, y=100, anchor="center")
    #Usuario
    lbl_usu = Label(app_Inse,text="Usuario", font=(fuente, 12))
    lbl_usu.place(x=180, y=170, anchor="center")
    ent_usu = Entry(app_Inse)
    ent_usu.place(relx=0.5, y=200, anchor="center", width=200,height=25)
    #Contraseña
    lbl_contra = Label(app_Inse,text="Contraseña", font=(fuente, 12))
    lbl_contra.place(x=190, y=240, anchor="center")
    ent_contra = Entry(app_Inse)
    ent_contra.place(relx=0.5, y=270, anchor="center", width=200,height=25)
    #Boton
    btn_ini = Button(app_Inse,text="Continuar", font=(fuente, 12, "bold"))
    btn_ini.place(relx=0.5, y=340, anchor="center", width=200, height=30)

    app.withdraw()
#--------------------Pantalla Iniciar Sesion como Organizador
def creacionPantalla_IniciarSesionOrganizador(app,fuente):
    app_Inse_Org = Toplevel(app)
    app_Inse_Org.title("Iniciar Sesion como Organizador") 
    centrarPantalla(500,500,app_Inse_Org)

    btn_volver = Button(app_Inse_Org, text="🡸", command=partial(cerrar_abrirVentanas,app_Inse_Org,app))
    btn_volver.place(x=10,y=10)

    lbl = Label(app_Inse_Org, text="Iniciar Sesión como\nOrganizador", font=(fuente,20,"bold"))
    lbl.place(relx=0.5, y=100, anchor="center")
    #Usuario
    lbl_usu = Label(app_Inse_Org,text="Usuario", font=(fuente, 12))
    lbl_usu.place(x=180, y=170, anchor="center")
    ent_usu = Entry(app_Inse_Org)
    ent_usu.place(relx=0.5, y=200, anchor="center", width=200,height=25)
    #Contraseña
    lbl_contra = Label(app_Inse_Org,text="Contraseña", font=(fuente, 12))
    lbl_contra.place(x=190, y=240, anchor="center")
    ent_contra = Entry(app_Inse_Org)
    ent_contra.place(relx=0.5, y=270, anchor="center", width=200,height=25)
    #Boton
    btn_ini = Button(app_Inse_Org,text="Continuar", font=(fuente, 12, "bold"),
                     command=partial(bd_InicioSesion_Organizador,ent_usu,ent_contra))
    btn_ini.place(relx=0.5, y=340, anchor="center", width=200, height=30)

    app.withdraw()
#--------------------INICIAR SESION COMO ORGANIZADOR
def bd_InicioSesion_Organizador(ent_usu, ent_contra):
    nombreUsuario = ent_usu.get()
    #ent_usu.delete(0,END)
    ent_usu.focus_set()

    contrasena = ent_contra.get()
    #ent_contra.delete(0,END)
    conexion = iniciarConexion(vectorConexion)

    cursor = conexion.cursor()
    consulta1 = "SELECT * FROM Organizador WHERE nombreUsuario = %s"
    cursor.execute(consulta1,(nombreUsuario,))

    resultado = cursor.fetchone()
    if(resultado):
        messagebox.showinfo(title= "Usuario Encontrado", message=("Se encontró el usuario "+nombreUsuario))
    else:
        messagebox.showerror(title= "Usuario No Encontrado", message=("No se encontró el usuario '"+nombreUsuario+ "' intente nuevamente"))

    cursor.close()
    conexion.close()
#--------------------Pantalla Registrarse
def creacionPantalla_Registrarse(app,fuente):
    app_Regis= Toplevel(app)
    app_Regis.title("Registrarse") 
    centrarPantalla(500,500,app_Regis)

    btn_volver = Button(app_Regis, text="🡸", command=partial(cerrar_abrirVentanas,app_Regis,app))
    btn_volver.place(x=10,y=10)

    lbl = Label(app_Regis, text="Registrarse", font=(fuente,20,"bold"))
    lbl.place(relx=0.5, y=30, anchor="center")
    #Usuario
    lbl_usu = Label(app_Regis,text="Usuario", font=(fuente, 12))
    lbl_usu.place(x=180, y=70, anchor="center")
    ent_usu = Entry(app_Regis)
    ent_usu.place(relx=0.5, y=100, anchor="center", width=200,height=25)
    #Contraseña
    lbl_contra = Label(app_Regis,text="Contraseña", font=(fuente, 12))
    lbl_contra.place(x=190, y=140, anchor="center")
    ent_contra = Entry(app_Regis)
    ent_contra.place(relx=0.5, y=170, anchor="center", width=200,height=25)
    #Nombre
    lbl_nombre = Label(app_Regis, text = "Nombre", font = (fuente, 12))
    lbl_nombre.place(x=180, y=200, anchor="center")
    ent_nombre = Entry(app_Regis)
    ent_nombre.place(relx=0.5, y=240, anchor="center", width=200,height=25)
    #Apellido
    lbl_ape = Label(app_Regis, text = "Apellido", font = (fuente, 12))
    lbl_ape.place(x=180, y=280, anchor="center")
    ent_ape = Entry(app_Regis)
    ent_ape.place(relx=0.5, y=310, anchor="center", width=200,height=25)
    #Mail
    lbl_mail = Label(app_Regis, text = "E-Mail", font = (fuente, 12))
    lbl_mail.place(x=175, y=350, anchor="center")
    ent_mail = Entry(app_Regis)
    ent_mail.place(relx=0.5, y=380, anchor="center", width=200,height=25)
    #Boton
    btn_ini = Button(app_Regis,text="Continuar", font=(fuente, 12, "bold"), 
                    command=partial(bd_registrarse_usuario,ent_nombre, ent_ape, ent_mail, ent_contra, ent_usu))
    btn_ini.place(relx=0.5, y=440, anchor="center", width=200, height=30)

    app.withdraw()
#--------------------REGISTRARSE
def bd_registrarse_usuario(ent_nombre, ent_ape, ent_mail, ent_contra, ent_usu):

    nombre = ent_nombre.get()
    apellido = ent_ape.get()
    mail = ent_mail.get()
    contra = ent_contra.get()
    usuario = ent_usu.get()

    # Validación de campos vacíos
    if not nombre or not apellido or not mail or not contra or not usuario:
        messagebox.showerror(title="Error", message="Por favor completa todos los campos antes de registrarte.")
        return

    # Validación de email básico
    if "@" not in mail or "." not in mail.split("@")[-1]:
        messagebox.showerror(title="Error", message="Por favor ingresa un correo electrónico válido.")
        return

    try:
        conexion = iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        # Verificar si el email ya está registrado
        consulta_mail = "SELECT COUNT(*) FROM Usuarios WHERE Email = %s"
        cursor.execute(consulta_mail, (mail,))
        resultado_mail = cursor.fetchone()[0]

        # Verificar si el nombre de usuario ya está registrado
        consulta_usuario = "SELECT COUNT(*) FROM Usuarios WHERE NombreUsuario = %s"
        cursor.execute(consulta_usuario, (usuario,))
        resultado_usuario = cursor.fetchone()[0]

        # Validaciones de existencia
        if resultado_mail > 0 and resultado_usuario > 0:
            messagebox.showerror(title="Error", message="Este nombre de usuario y este mail ya están tomados.")
        elif resultado_usuario > 0:
            messagebox.showerror(title="Error", message="Este nombre de usuario ya está tomado.")
        elif resultado_mail > 0:
            messagebox.showerror(title="Error", message="Este mail ya está registrado.")
        else:
            # Insertar nuevo usuario, fecha actual desde SQL
            consulta_insertar = """INSERT INTO Usuarios (Nombre, Apellido, Email, Contrasena, Fecha_Alta, NombreUsuario)
            VALUES (%s, %s, %s, %s, CURDATE(), %s)"""
            cursor.execute(consulta_insertar, (nombre, apellido, mail, contra, usuario))
            conexion.commit()
            messagebox.showinfo(title="Éxito", message="¡Usuario registrado correctamente!")
            ent_nombre.delete(0,END)
            ent_ape.delete(0,END)
            ent_contra.delete(0,END)
            ent_mail.delete(0,END)
            ent_usu.delete(0,END)

    except Exception as e:
        print(f"Error de conectividad: {e}")  # Para ti en consola
        messagebox.showerror(title="Error", message="Ocurrió un error de conectividad")

    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

#Programa Principal===============================
app = Tk() #Pantalla Principal
app.title("Menu Principal")
#--------------(ancho,alto,app)
centrarPantalla(500,500,app)
#--------------Definicion de Fuentes
fuente= ("Source Code Pro")
#--------------Conexion a la Base de Datos

 
creacionPantalla_Principal(app,fuente)

app.mainloop()