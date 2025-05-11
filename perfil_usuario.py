from tkinter import BooleanVar
import tkinter as tk
from tkinter.ttk import Checkbutton, Combobox
from tkinter.ttk import Treeview
from librerias import * 
import librerias as lib
import funciones_generales
import panel_administracion
from tkcalendar import DateEntry
from datetime import datetime
vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]

#FUNCIONES=============================================================================

#====================================[PANTALLAS]

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
    btn_ini = Button(app_Inse,text="Continuar", font=(fuente, 12, "bold"), 
                     command=partial(bd_InicioSesion_Verificacion,ent_usu, ent_contra, app_Inse, app, fuente))
    btn_ini.place(relx=0.5, y=340, anchor="center", width=200, height=30)

    app.withdraw()
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
#--------------------Ocultar pagina
def ocultar_pagina(vector_paginas, paginaMostrar):
    for pagina in vector_paginas:
        if pagina != paginaMostrar:
            pagina.place_forget()
#--------------------Cargar opciones combobox
def cargar_opciones_combobox(campo, tabla):
    vector_opciones=["Todas"]
    try:
        conexion=iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        consulta = (f"SELECT {campo} FROM {tabla}")
        cursor.execute(consulta)
        resultados=cursor.fetchall()
        if resultados:
            for posicion in resultados:
                vector_opciones.append(str(posicion[0]))
        return (vector_opciones)
    
    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message="Ups! No se pudieron cargar los filtros")
        return vector_opciones
    finally:
        try:
            conexion.close()
        except:
            pass

#--------------------Busqueda por palabras clave de eventos (FALTA AGREGAR FILTRO FECHA TANTO A PARAMETROS COMO CONSULTAS)
def busquedaEvento(lista, ent_buscar, cmb_categorias, cmb_ubicaciones, dateEntry_fecha, estado_boton_fechas):

    lista.unbind("<<TreeviewSelect>>")

    for item in lista.get_children():
        lista.delete(item)
    
    try:
        entrada = ent_buscar.get().strip()
        entryget="%"+entrada+"%"

        categoria_seleccionada = cmb_categorias.get()

        ubicacion_seleccionada = cmb_ubicaciones.get()

        fecha_formateada = dateEntry_fecha.get_date()

        print(fecha_formateada)
        print(estado_boton_fechas.get())

        conexion=iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta_busqueda_vacia_sin_filtros = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                'FROM Evento '
                                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                'WHERE estado="activo"')
        
        consulta_busqueda_vacia_solo_categoria = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                  'FROM Evento '
                                                  'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                  'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                  'WHERE estado="activo" AND LOWER(Categoria.nombre) = LOWER(%s)')
        
        consulta_busqueda_vacia_solo_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                'FROM Evento '
                                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                'WHERE estado="activo" AND LOWER(Ubicacion.direccion) = LOWER(%s)')
        
        consulta_busqueda_vacia_solo_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                            'FROM Evento '
                                            'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                            'WHERE estado="activo" AND DATE(fecha_inicio) = %s')
        
        consulta_busqueda_vacia_categoria_y_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                        'FROM Evento '
                                                        'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                        'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                        'WHERE estado="activo" AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s)')
        
        consulta_busqueda_vacia_categoria_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                    'FROM Evento '
                                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                    'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                    'WHERE estado="activo" AND LOWER(Categoria.nombre) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_busqueda_vacia_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                    'FROM Evento '
                                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                    'WHERE estado="activo" AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_busqueda_vacia_categoria_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                            'FROM Evento '
                                                            'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                            'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                            'WHERE estado="activo" AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_sin_filtros = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                'FROM Evento '
                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s)')
        
        consulta_solo_categoria = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                    'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s)')
        
        consulta_solo_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s)')

        consulta_solo_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                'FROM Evento '
                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_categoria_y_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                        'FROM Evento '
                                        'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                        'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                        'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s)')
        
        consulta_categoria_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                    'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')

        consulta_categoria_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                'FROM Evento '
                                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                'WHERE estado="activo" AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')

        if (entrada == "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_busqueda_vacia_sin_filtros)
        elif (entrada == "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_busqueda_vacia_solo_categoria, (categoria_seleccionada,))
        elif (entrada == "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_busqueda_vacia_solo_ubicacion, (ubicacion_seleccionada,))
        elif (entrada == "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_busqueda_vacia_solo_fecha, (fecha_formateada,))
        elif (entrada == "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_busqueda_vacia_categoria_y_ubicacion, (categoria_seleccionada,ubicacion_seleccionada,))
        elif (entrada == "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_busqueda_vacia_categoria_y_fecha, (categoria_seleccionada, fecha_formateada,))
        elif (entrada == "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_busqueda_vacia_ubicacion_y_fecha, (ubicacion_seleccionada, fecha_formateada,))
        elif (entrada == "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_busqueda_vacia_categoria_ubicacion_y_fecha, (categoria_seleccionada, ubicacion_seleccionada, fecha_formateada,))
        elif (entrada != "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_sin_filtros, (entryget,))
        elif (entrada != "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_solo_categoria, (entryget, categoria_seleccionada,))
        elif (entrada != "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_solo_ubicacion, (entryget, ubicacion_seleccionada,))
        elif (entrada != "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_solo_fecha, (entryget, fecha_formateada,))
        elif (entrada != "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == False):
            cursor.execute(consulta_categoria_y_ubicacion, (entryget, categoria_seleccionada, ubicacion_seleccionada,))
        elif (entrada != "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada == "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_categoria_y_fecha, (entryget, categoria_seleccionada, fecha_formateada,))
        elif (entrada != "" and categoria_seleccionada == "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_ubicacion_y_fecha, (entryget, ubicacion_seleccionada, fecha_formateada,))
        elif (entrada != "" and categoria_seleccionada != "Todas" and ubicacion_seleccionada != "Todas" and estado_boton_fechas.get() == True):
            cursor.execute(consulta_categoria_ubicacion_y_fecha, (entryget, categoria_seleccionada, ubicacion_seleccionada, fecha_formateada,))
        
        print(cursor.statement)

        resultados=cursor.fetchall()
        if resultados:
            for idevento, titulo, ubicacion, fecha_inicio in resultados:
                lista.insert("", "end", values=(idevento, titulo, ubicacion, fecha_inicio))
        else:
            lista.insert("", "end", values=("", "", "No se encontraron eventos que coincidan", ""))
            def bloquear_click(event):
                return "break"

            lista.bind("<ButtonPress-1>", bloquear_click)


    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message="Ups! Parece que algo salió mal")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

#--------------------Mostrar pagina principal
def mostrar_pagina_principal(vector_paginas):
    pagina_principal = vector_paginas[0]
    pagina_principal.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_principal)
#-------------------Mostrar pagina buscar
def mostrar_pagina_buscar(vector_paginas):

    pagina_buscar = vector_paginas[1]
    pagina_buscar.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_buscar)

    lbl1=Label(pagina_buscar,text="Buscar eventos", background="gainsboro", font = (fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    #funciones locales de placeholder (texto de sugerencia del entry)
    def clickeado(event):
        if ent_buscar.get() == 'Busca un evento por su título...':
            ent_buscar.delete(0, 'end')  # Borra el texto
            ent_buscar.config(fg='black')  # Cambia el color
            btn_buscar.config(state="normal")

    def no_clickeado(event):
        if ent_buscar.get() == '':
            ent_buscar.insert(0, 'Busca un evento por su título...')
            ent_buscar.config(fg='gray')
            btn_buscar.config(state="disabled")

    ent_buscar=Entry(pagina_buscar, font=(fuente, 15), fg="gray")
    ent_buscar.insert(0,"Busca un evento por su título...")
    ent_buscar.bind('<FocusIn>', clickeado)
    ent_buscar.bind('<FocusOut>', no_clickeado)

    ent_buscar.place(x=200, y=50, height=30, width=350)

    lbl_filtros=Label(pagina_buscar, font=(fuente,12), text="Filtros:", background="gainsboro")
    lbl_filtros.place(x=200, y=100, height=30)

    lbl_categorias=Label(pagina_buscar, font=(fuente,10), text="Categoria:", background="gainsboro")
    lbl_categorias.place(x=270, y=85, height=20)

    cmb_categorias=Combobox(pagina_buscar, font=(fuente,12), state="readonly")
    cmb_categorias.place(x=268, y=105, height=20, width=70)

    vector_categorias = cargar_opciones_combobox("nombre","Categoria")
    cmb_categorias["values"] = vector_categorias
    cmb_categorias.current(0)

    lbl_ubicacion=Label(pagina_buscar, font=(fuente,10), text="Ubicacion:", background="gainsboro")
    lbl_ubicacion.place(x=370, y=85, height=20)

    cmb_ubicaciones=Combobox(pagina_buscar, font=(fuente,12), state="readonly")
    cmb_ubicaciones.place(x=350, y=105, height=20, width=110)

    vector_ubicaciones = cargar_opciones_combobox("direccion","Ubicacion")
    cmb_ubicaciones["values"]=vector_ubicaciones
    cmb_ubicaciones.current(0)

    lbl_fechas=Label(pagina_buscar,font=(fuente,10),background="gainsboro",text="Filtrar por fecha:")
    lbl_fechas.place(x=480, y=85,height=20)

    #FALTA FILTRO PARA FECHAS

    dateEntry_fecha = DateEntry(pagina_buscar,date_pattern='yyyy-mm-dd')
    dateEntry_fecha.config(state="readonly")

    def mostrar_filtro_fecha(dateEntry_fecha):
        if estado_boton_fechas.get():
            dateEntry_fecha.place(x=475, y=105, height=20, width=125)
        else:
            dateEntry_fecha.place_forget()
    
    estado_boton_fechas=BooleanVar()
    chk_fechas=tk.Checkbutton(pagina_buscar, variable=estado_boton_fechas, background="gainsboro",command=partial(mostrar_filtro_fecha,dateEntry_fecha))
    chk_fechas.place(x=580, y=86,height=20, width=20)

    lista = Treeview(pagina_buscar,columns=("ID", "Título", "Dirección", "Fecha"), show="headings")
    lista.place(relx=0.5, anchor="center", relwidth=0.5, height=300, y=300)
    lista.heading("ID", text="")
    lista.heading("Título", text="Título")
    lista.heading("Dirección", text="Dirección")
    lista.heading("Fecha", text="Fecha")
    lista.column("ID", width=0, stretch=False)
    lista.column("Título", width=100, anchor="center")
    lista.column("Dirección", width=150, anchor="center")
    lista.column("Fecha", width=150, anchor="center")

    try:
        conexion=iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        cursor.execute('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio FROM Evento INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion WHERE estado="activo"')
        resultados=cursor.fetchall()
        if resultados:
            for idevento, titulo, ubicacion, fecha_inicio in resultados:
                lista.insert("", "end", values=(idevento, titulo, ubicacion, fecha_inicio))
        else:
            lista.insert("", "end", values=("", "", "No hay eventos activos", ""))
            # Deshabilitar selección
            def bloquear_click(event):
                return "break"

            lista.bind("<ButtonPress-1>", bloquear_click)

    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message="Ups! Parece que algo salió mal")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

    btn_buscar = Button(pagina_buscar, text="🔍", font=(fuente,13), relief="flat", command=partial(busquedaEvento, lista, ent_buscar, cmb_categorias, cmb_ubicaciones, dateEntry_fecha, estado_boton_fechas))
    btn_buscar.config(state="disabled")
    btn_buscar.place(x=550, y=50, height=30, width=50)
    
    
#--------------------Mostrar pagina notificaciones
def mostrar_pagina_notificaciones(vector_paginas):
    pagina_notificaciones = vector_paginas[2]
    pagina_notificaciones.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_notificaciones)

    lbl1=Label(pagina_notificaciones,text="Notificaciones", background="gainsboro", font = (fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

#--------------------Pantalla Menu Usuario
def creacionPantalla_MenuUsuario(app,_fuente,nombreUsuario):
    global fuente
    fuente = _fuente
    app_MenuUs = Toplevel(app)
    centrarPantalla(1000,500,app_MenuUs)
    app_MenuUs.title("Sesion Usuario")
    #PANEL 1 (izquierda, el mas angosto)
    panel1 = Frame(app_MenuUs, bg="gray")
    panel1.place(x=0, width=200, height=500)
    #PANEL 2 (derecha, el mas ancho)
    panel2 = Frame(app_MenuUs, bg="gainsboro")
    panel2.place(x=200, width=800, height=500)

    #Pagina buscar eventos
    pagina_buscar = Frame(app_MenuUs, bg="gainsboro")
    pagina_buscar.place(x=200, width=800, height=500)

    #Pagina notificaciones
    pagina_notificaciones=Frame(app_MenuUs, bg="gainsboro")
    pagina_notificaciones.place(x=200, width=800, height=500)

    #Completar vector paginas
    vector_paginas=[panel2,pagina_buscar,pagina_notificaciones]

    for i in range(len(vector_paginas)):
        if vector_paginas[i] != panel2:
            vector_paginas[i].place_forget()

    #BOTON VOLVER
    btn_volver = Button(app_MenuUs, text="🡸", command=partial(cerrar_abrirVentanas,app_MenuUs,app))
    btn_volver.place(x=10,y=10)
    #COMPONENTES PARA EL PANEL 1

    btn_principal = Button(app_MenuUs, text="Menu Principal", relief="flat", command=partial(mostrar_pagina_principal,vector_paginas))
    btn_principal.place(x=20, y=70, width=160, height=30)
    
    btn_buscar = Button(app_MenuUs, text="Buscar Eventos", relief="flat", command=partial(mostrar_pagina_buscar, vector_paginas))
    btn_buscar.place(x=20, y=100, width=160, height=30)
    
    btn_notificaciones = Button(app_MenuUs, text="Notificaciones", relief="flat", command=partial(mostrar_pagina_notificaciones, vector_paginas))
    btn_notificaciones.place(x=20, y=130, width=160, height=30)

    #COMPONENTES PARA EL PANEL 2 (pagina principal) 
    
    lbl1 = Label(panel2, text=("¡Bienvenido/a "+nombreUsuario+"!"), bg = "gainsboro", font=(fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    
#====================================[BASE DE DATOS]
def iniciarConexion(vectorConexion):
    conexion = mysql.connector.connect(
        host= vectorConexion[0],
        user= vectorConexion[1],
        password= vectorConexion[2],
        database= vectorConexion[3]
    )
    return conexion
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
#--------------------INICIAR SESION
def bd_InicioSesion_Verificacion(ent_usu, ent_contra, app_Inse, app, fuente):
    if(len(ent_usu.get()) > 0 and len(ent_contra.get()) > 0):
        nombreUsuario = ent_usu.get()
        contrasena = ent_contra.get()
        try:
            conexion = iniciarConexion(vectorConexion)
            cursor = conexion.cursor()
            #CONSULTA PARA VERIFICAR QUE SEA UN ORGANIZADOR O NO-------------------------------------
            consulta1 = "SELECT * FROM Organizador WHERE nombreUsuario = %s"
            consulta2 = "SELECT * FROM Organizador WHERE nombreUsuario = %s AND contraseña = %s"
            #CONSULTA PARA VERIFICAR QUE SEA UN USUARIO O NO---------------------------------
            consulta3 = "SELECT * FROM Usuarios WHERE NombreUsuario = %s"
            consulta4 = "SELECT * FROM Usuarios WHERE NombreUsuario = %s AND Contrasena = %s"

            cursor.execute(consulta1,(nombreUsuario,))
            resultado = cursor.fetchone()  
            if(resultado):
                cursor.execute(consulta2,(nombreUsuario,contrasena,))
                resultado2 = cursor.fetchone()
                if(resultado2):
                    app_Inse.destroy()
                    id_organizador = resultado2[0]
                    panel_administracion.creacionPantalla_MenuOrganizador2(app,fuente, nombreUsuario, id_organizador)
                    print("Se encontró como ORGANIZADOR")
                else:
                    messagebox.showerror(title= "Credenciales no Coinciden", 
                                        message=("La contraseña no coincide con el nombre de usuario '"+nombreUsuario+ "' intente nuevamente"))
                    ent_contra.delete(0,END)
                    ent_contra.focus_set()
                    print("No se encontro como ORGANIZADOR")   
            else:
                cursor.execute(consulta3,(nombreUsuario,))
                resultado3 = cursor.fetchone()  
                if(resultado3):
                    cursor.execute(consulta4,(nombreUsuario,contrasena,))
                    resultado4 = cursor.fetchone()
                    if(resultado4):
                        app_Inse.destroy()
                        creacionPantalla_MenuUsuario(app,fuente, nombreUsuario)
                        print("Se encontro como USUARIO")
                    else:
                        messagebox.showerror(title= "Credenciales no Coinciden", 
                                            message=("La contraseña no coincide con el nombre de usuario '"+nombreUsuario+ "' intente nuevamente"))
                        ent_contra.delete(0,END)
                        ent_contra.focus_set()
                        print("No se encontró como USUARIO")   
                else:
                    messagebox.showerror(title= "Usuario No Encontrado", message=("No se encontró el usuario '"+nombreUsuario+ "' intente nuevamente"))
                    ent_usu.delete(0,END)
                    ent_contra.delete(0,END) 
                    ent_usu.focus_set()   
     
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
        finally:      
            cursor.close()
            conexion.close()
    else:
        messagebox.showerror(title="Valores Invalidos", message="Por favor llene los campos")
        ent_usu.delete(0,END)
        ent_contra.delete(0,END) 
        ent_usu.focus_set()  
