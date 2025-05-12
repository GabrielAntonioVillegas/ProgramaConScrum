from librerias import * 
import librerias as lib
import funciones_generales
from tkcalendar import DateEntry
from datetime import datetime
vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]
COLOR_NORMAL = "#f0f0f0"
COLOR_ACTIVO = "gainsboro"

def enviar_notificacion(combo_evento, ent_desc_noti, dictEventos):
    # VALIDACIÓN DE CAMPOS VACÍOS
    if len(combo_evento.get()) > 0 and len(ent_desc_noti.get()) > 0:
        try:
            id_evento = dictEventos[combo_evento.get()]
            descripcion_noti = ent_desc_noti.get()

            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            # INSERTAR NOTIFICACIÓN
            consulta = "INSERT INTO Notificacion (id_evento, descripcion_noti, fecha) VALUES (%s, %s, NOW())"
            cursor.execute(consulta, (id_evento, descripcion_noti))
            conexion.commit()

            messagebox.showinfo(title="Éxito", message="¡Notificación enviada correctamente!")

            # LIMPIAR CAMPOS
            combo_evento.set("")
            ent_desc_noti.delete(0, "end")

        except Exception as e:
            messagebox.showerror(title="Error de Conexión", message="¡Ups! Hubo un error al conectar con la base de datos.")
            print(e)

        finally:
            try:
                cursor.close()
                conexion.close()
            except:
                pass
    else:
        messagebox.showerror(title="Campos vacíos", message="Por favor complete todos los campos antes de enviar la notificación.")
#-------------------------------------------
def mostrar_eventosNotificacion(combo_eventos, id_organizador):
    vectorEventos = []
    dictEventos = {}

    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = "SELECT id_evento, titulo FROM Evento WHERE estado = 'activo' AND id_organizador = %s ORDER BY id_evento ASC"
        
        cursor.execute(consulta, (id_organizador,))
        resultado = cursor.fetchall()

        if resultado:
            for id_evento, titulo in resultado:
                vectorEventos.append(titulo)
                dictEventos[titulo] = id_evento

            combo_eventos["values"] = vectorEventos

    except Exception as e:
        messagebox.showerror(title="Error de Conexión", message="¡Ups! Hubo un error al conectar con la Base de Datos")
        print(e)
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

    return dictEventos
#-------------------------------------------
def mostrar_pagina_notificaciones(vector_paginas, app_MenuOrg, botones, btn_seleccionado, fuente, id_organizador):
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)

    pagina_notificaciones = vector_paginas[7]
    pagina_notificaciones.place(x=200, width=800, height=500)
    funciones_generales.ocultar_pagina(vector_paginas, pagina_notificaciones)

    lbl1 = Label(pagina_notificaciones, text="Notificaciones", font=(fuente, 16, "bold"), background="gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    parte1 = Frame(pagina_notificaciones)
    parte1.place(x=10, y=30, width=780, height=460)

    lbl_personaliz = Label(parte1, text="Notificación Personalizada", font=(fuente, 14, "bold"))
    lbl_personaliz.place(relx=0.5, anchor="center", y=50)

    # Nombre del evento
    lbl_evento = Label(parte1, text="Nombre del Evento", font=(fuente, 10))
    lbl_evento.place(relx=0.5, y=100, anchor="center")

    combo_eventos = ttk.Combobox(parte1, state="readonly", font=(fuente, 10))
    combo_eventos.place(relx=0.5, y=130, anchor="center", width=300)
    dict_eventos = mostrar_eventosNotificacion(combo_eventos, id_organizador)

    # Descripción de la notificación
    lbl_desc = Label(parte1, text="Descripción de Notificación", font=(fuente, 10))
    lbl_desc.place(relx=0.5, y=180, anchor="center")

    ent_desc = Entry(parte1)
    ent_desc.place(relx=0.5, y=260, anchor="center", width=500, height=100)

    # Botón para enviar notificación
    btn_enviar = Button(parte1, text="Enviar Notificación", font=(fuente, 10, "bold"), 
                        command=partial(enviar_notificacion,combo_eventos, ent_desc, dict_eventos))
    btn_enviar.place(relx=0.5, y=380, anchor="center", width=200, height=30)
    
