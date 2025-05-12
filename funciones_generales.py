from librerias import * 
import librerias as lib

#OCULTAR PAGINA------------------------------------------
def ocultar_pagina(vector_paginas, paginaMostrar):
    for pagina in vector_paginas:
        if pagina != paginaMostrar:
            pagina.place_forget()
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
#-------------------Click Boton
def click_boton(indice, botones, COLOR_NORMAL, COLOR_ACTIVO):

    for btn in botones:
        btn.config(bg=COLOR_NORMAL)

    botones[indice].config(bg = COLOR_ACTIVO)
#-------------------Limpiar contenido treeview
def limpiar_treeview(treeview):
    """Elimina todos los elementos de un Treeview."""
    for item in treeview.get_children():
        treeview.delete(item)
#-------------------ACTUALIZA ESTADO DE EVENTOS
def actualizar_estados_eventos(vectorConexion):
    try:
        conexion = iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = "UPDATE Evento SET estado = 'finalizado' WHERE fecha_fin < NOW() AND estado = 'activo'"
        cursor.execute(consulta)
        conexion.commit()
    except Exception as e:
        print("Error al actualizar estados automáticamente:", e)
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass
#-------------------CONEXION BASE DE DATOS
def iniciarConexion(vectorConexion):
    conexion = mysql.connector.connect(
        host= vectorConexion[0],
        user= vectorConexion[1],
        password= vectorConexion[2],
        database= vectorConexion[3],
        time_zone= "-03:00"
    )
    return conexion