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
import pagina_cuenta
vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]
asiento_seleccionado = None
boton_seleccionado = None
#FUNCIONES=============================================================================

#====================================[PANTALLAS]
def abrirPantallaRegistrarse(app, fuente, app_Inse):
    app_Inse.destroy()
    creacionPantalla_Registrarse(app, fuente)
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
    app2.unbind_all("<Button-1>")
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
        consulta = (f"SELECT {campo} FROM {tabla} WHERE activo = 1")
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
            cursor.close()
            conexion.close()
        except:
            pass
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
    ent_contra = Entry(app_Inse,show="✱")
    ent_contra.place(relx=0.5, y=270, anchor="center", width=200,height=25)
    #Boton en caso de no estar registrado
    btn_res = Button(app_Inse, text="¿No tiene un Usuario?\nPresione aquí para Registrarse", 
                     font=(fuente, 10), relief="groove", activeforeground="blue", command=partial(abrirPantallaRegistrarse,app, fuente, app_Inse))
    #Boton Continuar
    btn_ini = Button(app_Inse,text="Continuar", font=(fuente, 12, "bold"), 
                     command=partial(bd_InicioSesion_Verificacion,ent_usu, ent_contra, app_Inse, app, fuente, btn_res))
    btn_ini.place(relx=0.5, y=330, anchor="center", width=200, height=30)


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
#--------------------Pantalla Principal de Usuario
def mostrar_pagina_principal(vector_paginas):
    pagina_principal = vector_paginas[0]
    pagina_principal.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_principal)

    # Crear un Treeview
    treeview_frame = tk.Frame(pagina_principal)
    treeview_frame.place(relx=0.5, rely=0.5, anchor="center")

    tree = ttk.Treeview(treeview_frame, columns=("Fecha", "Descripción"), show="headings")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Descripción", text="Descripción")
    tree.column("Fecha",width=120)
    tree.column("Descripción", width=500)
    tree.pack(fill=tk.BOTH, expand=True)

    # Obtener las notificaciones de la base de datos
    notificaciones = obtener_notificaciones()

    if notificaciones:
        # Insertar los resultados en el Treeview
        for noti in notificaciones:
            # Aquí no es necesario usar strptime porque noti[0] ya es un objeto datetime
            fecha_formateada = noti[0].strftime('%d-%m-%Y %H:%M:%S')
            tree.insert("", "end", values=(fecha_formateada, noti[1]))
    else:
        messagebox.showinfo("Sin notificaciones", "No hay notificaciones para mostrar.")
#--------------------Pantalla Menu Usuario
def creacionPantalla_MenuUsuario(app,_fuente,nombreUsuario):

    try:
        conexion=iniciarConexion(vectorConexion)
        cursor=conexion.cursor()
        consulta=("SELECT UsuarioID FROM Usuarios WHERE NombreUsuario = %s")
        cursor.execute(consulta, (nombreUsuario,))
        resultado = cursor.fetchone()

        id_usuario=resultado[0]

    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message="Ups! Parece que algo salió mal")
    
    finally:
        try:
            conexion.close()
            cursor.close()
        except:
            pass

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

    #Pagina favoritos
    pagina_favoritos=Frame(app_MenuUs, bg="gainsboro")
    pagina_favoritos.place(x=200, width=800, height=500)

    #Pagina carrito
    pagina_carrito=Frame(app_MenuUs, bg="gainsboro")
    pagina_carrito.place(x=200, width=800, height=500)

    #Pagina cuenta
    pagina_cuenta=Frame(app_MenuUs, bg="gainsboro")
    pagina_carrito.place(x=200, width=800, height=500)

    #Completar vector paginas
    vector_paginas=[panel2,pagina_buscar,pagina_favoritos, pagina_carrito, pagina_cuenta]

    for i in range(len(vector_paginas)):
        if vector_paginas[i] != panel2:
            vector_paginas[i].place_forget()

    #BOTON VOLVER
    btn_volver = Button(app_MenuUs, text="🡸", command=partial(cerrar_abrirVentanas,app_MenuUs,app))
    btn_volver.place(x=10,y=10)

    #COMPONENTES PARA EL PANEL 1

    btn_principal = Button(app_MenuUs, text="MENU PRINCIPAL", relief="flat", command=partial(mostrar_pagina_principal,vector_paginas))
    btn_principal.place(x=20, y=70, width=160, height=30)

    btn_cuenta = Button(app_MenuUs, text="CUENTA", relief="flat", command=partial(pagina_cuenta.mostrar_pagina_cuenta,app,vector_paginas,id_usuario))
    btn_cuenta.place(x=20, y=100, width=160, height=30)
    
    btn_buscar = Button(app_MenuUs, text="BUSCAR EVENTOS", relief="flat", command=partial(mostrar_pagina_buscar, app, vector_paginas, id_usuario))
    btn_buscar.place(x=20, y=130, width=160, height=30)
    
    btn_favoritos = Button(app_MenuUs, text="FAVORITOS", relief="flat", command=partial(mostrar_pagina_favoritos, app, vector_paginas, id_usuario))
    btn_favoritos.place(x=20, y=160, width=160, height=30)

    btn_carrito = Button(app_MenuUs, text="CARRITO", relief="flat", command=partial(mostrar_pagina_carrito, vector_paginas))
    btn_carrito.place(x=20, y=190, width=160, height=30)

    #COMPONENTES PARA EL PANEL 2 (pagina principal) 
    
    lbl1 = Label(panel2, text=("¡Bienvenido/a "+nombreUsuario+"!"), bg = "gainsboro", font=(fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
#--------------------Mostrar pagina buscar
def mostrar_pagina_buscar(app,vector_paginas, id_usuario):

    pagina_buscar = vector_paginas[1]
    pagina_buscar.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_buscar)

    lbl1=Label(pagina_buscar,text="Buscar eventos", background="gainsboro", font = (fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    def limpiar_seleccion_lista(event):
        widget_actual = event.widget
        if not str(widget_actual).startswith(str(lista)):
            lista.selection_remove(lista.selection())
    
    app.bind_all("<Button-1>", limpiar_seleccion_lista)         #Esta linea junto a la funcion de arriba hacen que
                                                                #Cuando se clickee cualquier parte que no sea
                                                                #un evento del treeview, se desenfoque
                                                                #el seleccionado anteriormente
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

    def doble_click(event):
        seleccion = lista.selection()
        if not seleccion:
            return  # No hacer nada si no hay selección
        item_id = lista.selection()[0]
        valores = lista.item(item_id, "values")
        id_evento = valores[0]
        ver_detalles_evento(app, fuente, id_evento, lista, id_usuario)

    lista.bind("<Double-1>", doble_click)
    try:
        conexion=iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        cursor.execute('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio FROM Evento INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion WHERE (estado="activo" OR estado="cancelado")')
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

    btn_buscar = Button(pagina_buscar, text="🔍", font=(fuente,13), relief="flat", command=partial(busquedaEvento, app, lista, ent_buscar, cmb_categorias, cmb_ubicaciones, dateEntry_fecha, estado_boton_fechas))
    btn_buscar.config(state="disabled")
    btn_buscar.place(x=550, y=50, height=30, width=50)
#--------------------Mostrar pagina notificaciones
def mostrar_pagina_favoritos(app,vector_paginas,id_usuario):
    pagina_favoritos = vector_paginas[2]
    pagina_favoritos.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_favoritos)

    lbl1=Label(pagina_favoritos,text="Favoritos", background="gainsboro", font = (fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
    def limpiar_seleccion_lista(event):
        widget_actual = event.widget
        if not str(widget_actual).startswith(str(lista)):
            lista.selection_remove(lista.selection())
    
    app.bind_all("<Button-1>", limpiar_seleccion_lista)         #Esta linea junto a la funcion de arriba hacen que
                                                                #Cuando se clickee cualquier parte que no sea
                                                                #un evento del treeview, se desenfoque
                                                                #el seleccionado anteriormente

    lista = Treeview(pagina_favoritos,columns=("Categorias:"), show="headings")
    lista.place(relx=0.5, anchor="center", relwidth=0.5, height=300, y=200)
    lista.heading("Categorias:", text="Categorias:")
    lista.column("Categorias:", width=400, anchor="center")

    try:
        conexion=iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        consulta=('SELECT id_categoria FROM PreferenciaCategoria WHERE UsuarioID = %s AND activo=1')
        cursor.execute(consulta,(id_usuario,))
        resultados=cursor.fetchall()
        if resultados:
            # Extraer solo los ids de cada tupla
            ids = [fila[0] for fila in resultados]
            placeholders = ", ".join(['%s'] * len(ids))
            consulta = f'SELECT nombre FROM Categoria WHERE id_categoria IN ({placeholders})'
            cursor.execute(consulta, ids)
            resultados2 = cursor.fetchall()
            for categoria in resultados2:
                lista.insert("", "end", values=categoria)
        else:
            lista.insert("", "end", values=("No tenes favoritos"))
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

    btn_eliminar = Button(pagina_favoritos, text="Eliminar de favoritos", wraplength=100,command=partial(eliminar_favoritos, lista, id_usuario, app, vector_paginas))
    btn_eliminar.place(relx=0.5, y=400, anchor = "center")
#--------------------Mostrar pagina carrito
def mostrar_pagina_carrito(vector_paginas):
    pagina_carrito = vector_paginas[3]
    pagina_carrito.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_carrito)

    lbl1=Label(pagina_carrito,text="Carrito de compras", background="gainsboro", font = (fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)


#====================================[EVENTOS Y FAVORITOS]
#--------------------Crear Ventana Detalles Evento
def ver_detalles_evento(app, fuente, id_evento, lista, id_usuario):

    lista.unbind("<Double-1>") #Deshabilitar abrir detalles con dobleclick
    
    def cerrar_ventana_detalle():
        ventanaDetalles.destroy()

        def doble_click(event):

            seleccion = lista.selection()
            if not seleccion:
                return  # No hacer nada si no hay selección
            
            item_id = lista.selection()[0]
            valores = lista.item(item_id, "values")
            id_evento = valores[0]
            ver_detalles_evento(app, fuente, id_evento, lista, id_usuario)
        
        lista.bind("<Double-1>", doble_click) #volver a habilitar abrir detalles
    
    ventanaDetalles = tk.Toplevel(app)
    ventanaDetalles.title("Detalles del evento")
    ventanaDetalles.protocol("WM_DELETE_WINDOW", cerrar_ventana_detalle) #que hacer cuando se cierra la ventana manualmente
    centrarPantalla(1000,1000,ventanaDetalles)
    ventanaDetalles.resizable(False,False)

    try:
        conexion = iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = ("SELECT * FROM Evento WHERE id_evento = %s")

        cursor.execute(consulta, (id_evento,))
        resultado = cursor.fetchone()

        #VARIABLES
        
        titulo = resultado[2]
        descripcion = resultado[3]
        id_categoria = resultado[4]
        fecha_inicio = resultado[5].strftime("%d-%m-%Y %H:%M")
        fecha_fin = resultado[6].strftime("%d-%m-%Y %H:%M")
        estado = resultado[7]
        #OBTENER FECHA DEL TREEVIEW
        item_id = lista.selection()[0]
        valores = lista.item(item_id, "values")

        direccion = valores[2]

        lbl_titulo = Label(ventanaDetalles, text=("Titulo del evento: "+titulo), font = (fuente, 10))
        lbl_titulo.place(relx=0.5, y=20, anchor="center")

        lbl_descripcion = Label(ventanaDetalles, text=("Descripcion: "+descripcion), wraplength=400, font = (fuente,10))
        lbl_descripcion.place(relx=0.5, y=40, anchor="center")
        
        #OBTENER NOMBRE DE LA CATEGORIA
        consulta = ("SELECT nombre FROM Categoria WHERE id_categoria = %s")
        cursor.execute(consulta, (id_categoria,))

        resultado = cursor.fetchone()

        categoria = resultado[0]

        lbl_categoria = Label(ventanaDetalles, text=("Categoria: "+categoria), font=(fuente, 10))
        lbl_categoria.place(relx=0.5, y=130, anchor="center")

        lbl_fecha = Label(ventanaDetalles, font=(fuente,10))
        lbl_año = Label(ventanaDetalles, text=("Año: "+fecha_inicio[6:10]), font=(fuente,10))
        lbl_año.place(relx=0.5, y=150, anchor="center")

        if (fecha_inicio == fecha_fin):
            lbl_fecha.configure(text=("Fecha: "+fecha_inicio[0:5]+" a las "+fecha_inicio[11:]+"hs"))
        elif (fecha_inicio[0:10] == fecha_fin[0:10] and fecha_inicio[11:] != fecha_fin[11:]):
            lbl_fecha.configure(text=("Fecha: "+fecha_inicio[0:5]+" desde las "+fecha_inicio[11:]+"hs hasta las "+fecha_fin[11:]+"hs"))
        elif (fecha_inicio != fecha_fin):
            lbl_fecha.configure(text=("Fecha: Desde el "+fecha_inicio[0:5]+" a las "+fecha_inicio[11:]+"hs hasta el "+fecha_fin[0:5]+" a las "+fecha_fin[11:]+"hs"))

        lbl_fecha.place(relx=0.5, y=170, anchor="center")

        lbl_direccion = Label(ventanaDetalles, text="Direccion: "+direccion, font=(fuente,10))
        lbl_direccion.place(relx=0.5, y=190, anchor="center")


        btn_favorito = Button(ventanaDetalles, text="Agregar categoria a favoritos", wraplength=120, font=(fuente,10), command=partial(agregar_favorito, id_categoria, id_usuario))
        btn_favorito.place(relx=0.5, y=240, anchor="center")

        def cargar_entradas(id_evento):
            try:
                conexion = iniciarConexion(vectorConexion)
                cursor = conexion.cursor()
                consulta = "SELECT tipo FROM Entrada WHERE Evento_id = %s"
                cursor.execute(consulta, (id_evento,))
                resultados=cursor.fetchall()
                vector_opciones=[]
                if resultados:
                    for posicion in resultados:
                        vector_opciones.append(str(posicion[0]))
                return (vector_opciones)
                    

            except Exception as e:
                print(e)
                messagebox.showerror("Error", "No se pudieron cargar los tipos de entrada")

            finally:
                try:
                    cursor.close()
                    conexion.close()
                except:
                    pass
        
        lbl_estado = Label(ventanaDetalles, text="Estado: "+estado, font=(fuente,10))
        lbl_estado.place(relx=0.5, y=290, anchor="center")
        if estado=="activo":
            lbl_entradas = Label(ventanaDetalles, text="Entradas: ", font = (fuente, 10))
            lbl_entradas.place(relx=0.5, y=330, anchor="center")
            cmb_entradas = Combobox(ventanaDetalles,font=(fuente,12), state="readonly")
            cmb_entradas.place(relx=0.5, y=360, anchor="center")
            vector_entradas = cargar_entradas(id_evento)
            if vector_entradas:
                cmb_entradas["values"]=vector_entradas
                cmb_entradas.current(0)
                frame_grilla = Frame(ventanaDetalles)
                frame_grilla.place(relx=0.5, y=550,anchor="center")
                def cargar_asientos_cb():
                    tipo_entrada = cmb_entradas.get()
                    if not tipo_entrada:
                        messagebox.showerror("Error", "Seleccioná un tipo de entrada")
                        return

                    try:
                        conexion = iniciarConexion(vectorConexion)
                        cursor = conexion.cursor()
                        consulta = "SELECT id_entrada, asiento FROM Entrada WHERE tipo = %s AND Evento_id = %s"
                        cursor.execute(consulta, (tipo_entrada, id_evento,))
                        resultado = cursor.fetchone()

                        for widget in frame_grilla.winfo_children():
                            widget.destroy()

                        if resultado:
                            id_entrada, tiene_asientos = resultado
                            if tiene_asientos:
                                cargar_grilla_asientos(frame_grilla, id_entrada)
                            else:
                                frame_grilla.place_forget()
                                #ACA VA SI NO TIENE ASIENTOS
                                consulta=("SELECT cupo_disponible FROM Entrada WHERE id_entrada = %s")
                                cursor.execute(consulta, (id_entrada,))
                                cupo = cursor.fetchone()
                                lbl_cupo=Label(ventanaDetalles, text=("Disponibles: "+str(cupo[0])))
                                lbl_cupo.place(relx=0.5, y=550, anchor="center")
                        else:
                            messagebox.showerror("Error", "Entrada no encontrada")

                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error", "Error al buscar la entrada")
                    finally:
                        try:
                            cursor.close()
                            conexion.close()
                        except:
                            pass

                btn_cargar = Button(ventanaDetalles, text="Cargar entradas", command=cargar_asientos_cb)
                btn_cargar.place(relx=0.5, y=400, anchor="center")
                
            else:
                cmb_entradas.place_forget()
                lbl_entradas.place_forget()
                lbl_entradas.configure(text="No hay entradas disponibles para este evento")
                lbl_entradas.place(relx=0.5, y=320, anchor="center")
    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message="Ups! Parece que algo salió mal")

    finally:
        try:
            conexion.close()
            cursor.close()
        except:
            pass
#--------------------Busqueda por palabras clave de eventos
def busquedaEvento(app,lista, ent_buscar, cmb_categorias, cmb_ubicaciones, dateEntry_fecha, estado_boton_fechas):

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
                                                'WHERE (estado="activo" OR estado="cancelado")')
        
        consulta_busqueda_vacia_solo_categoria = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                  'FROM Evento '
                                                  'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                  'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                  'WHERE (estado="activo" OR estado="cancelado") AND LOWER(Categoria.nombre) = LOWER(%s)')
        
        consulta_busqueda_vacia_solo_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                'FROM Evento '
                                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                'WHERE (estado="activo" OR estado="cancelado") AND LOWER(Ubicacion.direccion) = LOWER(%s)')
        
        consulta_busqueda_vacia_solo_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                            'FROM Evento '
                                            'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                            'WHERE (estado="activo" OR estado="cancelado") AND DATE(fecha_inicio) = %s')
        
        consulta_busqueda_vacia_categoria_y_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                        'FROM Evento '
                                                        'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                        'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                        'WHERE (estado="activo" OR estado="cancelado") AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s)')
        
        consulta_busqueda_vacia_categoria_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                    'FROM Evento '
                                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                    'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                    'WHERE (estado="activo" OR estado="cancelado") AND LOWER(Categoria.nombre) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_busqueda_vacia_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                    'FROM Evento '
                                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                    'WHERE (estado="activo" OR estado="cancelado") AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_busqueda_vacia_categoria_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                            'FROM Evento '
                                                            'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                            'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                            'WHERE (estado="activo" OR estado="cancelado") AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_sin_filtros = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                'FROM Evento '
                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s)')
        
        consulta_solo_categoria = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                    'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s)')
        
        consulta_solo_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s)')

        consulta_solo_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                'FROM Evento '
                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_categoria_y_ubicacion = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                        'FROM Evento '
                                        'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                        'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                        'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s)')
        
        consulta_categoria_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                    'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s) AND DATE(fecha_inicio) = %s')
        
        consulta_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                    'FROM Evento '
                                    'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                    'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')

        consulta_categoria_ubicacion_y_fecha = ('SELECT id_evento, titulo, Ubicacion.direccion, fecha_inicio '
                                                'FROM Evento '
                                                'INNER JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion '
                                                'INNER JOIN Categoria ON Categoria.id_categoria = Evento.id_categoria '
                                                'WHERE (estado="activo" OR estado="cancelado") AND LOWER(titulo) LIKE LOWER(%s) AND LOWER(Categoria.nombre) = LOWER(%s) AND LOWER(Ubicacion.direccion) = LOWER(%s) AND DATE(fecha_inicio) = %s')

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

            lista.unbind("<ButtonPress-1>") #Desbloquear seleccion

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
#--------------------Agregar categoria a favoritos
def agregar_favorito(id_categoria, id_usuario):
    try:
        conexion = iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        consulta = ("SELECT * FROM PreferenciaCategoria WHERE UsuarioID = %s AND id_categoria = %s")
        cursor.execute(consulta, (id_usuario, id_categoria,))

        resultado = cursor.fetchone()
        if resultado:
            messagebox.showerror(title="Error", message="Ya tienes esta categoria en favoritos")
        else:
            consulta = ("INSERT INTO PreferenciaCategoria (UsuarioID, id_categoria, activo) VALUES (%s,%s,1)")
            cursor.execute(consulta, (id_usuario, id_categoria,))
            conexion.commit()
            messagebox.showinfo(title="Éxito", message="La categoria fue guardada como favorita con exito")
        
        print(cursor.statement)
    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message="Ups! Parece que algo salió mal")
    
    finally:
        try:
            conexion.close()
            cursor.close()
        except:
            pass
#--------------------Eliminar categoria de favoritos
def eliminar_favoritos(lista, id_usuario, app,vector_paginas):
    selected_item = lista.focus()
    values = lista.item(selected_item, 'values') 
    if not values:
        messagebox.showerror(title="Error", message="No seleccionaste ninguna categoria")
        return "break"
    else:

        try:
            conexion=iniciarConexion(vectorConexion)
            cursor = conexion.cursor()
            consulta = ("SELECT id_categoria FROM Categoria WHERE nombre = %s")
            cursor.execute(consulta, (values[0],))
            resultado=cursor.fetchone()[0]

            consulta=("DELETE FROM PreferenciaCategoria WHERE id_categoria = %s AND UsuarioID = %s")
            cursor.execute(consulta, (resultado,id_usuario,))
            conexion.commit()
            messagebox.showinfo(title="Exito", message="Eliminaste esta categoria de favoritos con exito")
            mostrar_pagina_favoritos(app,vector_paginas,id_usuario)
        
        except Exception as e:
            print(e)
            messagebox.showerror(title="Error", message="Ups! Parece que ocurrio un error")
        
        finally:
            try:
                conexion.close()
                cursor.close()
            except:
                pass
#--------------------Mostrar pagina principal (notificaciones)
def obtener_notificaciones():
    try:
        # Establecer conexión con la base de datos
        conexion=iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        # Consulta SQL para obtener notificaciones
        consulta = """
        SELECT n.fecha, n.descripcion_noti
        FROM Notificacion n
        INNER JOIN Evento e ON n.id_evento = e.id_evento
        INNER JOIN PreferenciaCategoria pc ON e.id_categoria = pc.id_categoria
        WHERE n.fecha <= NOW() AND e.id_categoria = pc.id_categoria;
        """
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        return resultados

    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"Error al obtener las notificaciones")
        return []
    finally:
        try:
            # Cerrar la conexión
            cursor.close()
            conexion.close()
        except:
            pass

#====================================[SELECCION DE ASIENTOS]
#--------------------Seleccion de asiento
def seleccionar_asiento(id_asiento, boton):
    global asiento_seleccionado, boton_seleccionado

    # Restaurar el color del botón anterior si lo había
    if boton_seleccionado:
        boton_seleccionado.configure(bg="green")

    # Marcar nuevo asiento
    asiento_seleccionado = id_asiento
    boton_seleccionado = boton
    boton.configure(bg="yellow")

    print(f"Asiento seleccionado: {id_asiento}")
#--------------------CARGAR GRILLA ASIENTOS
def cargar_grilla_asientos(frame, entrada_id):
    global asiento_seleccionado, boton_seleccionado

    for widget in frame.winfo_children():
        widget.destroy()

    try:
        conexion = iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        # Obtener asientos por Entrada_id
        consulta = "SELECT id_asiento, fila, columna, disponible FROM Asiento WHERE Entrada_id = %s"
        cursor.execute(consulta, (entrada_id,))
        asientos = cursor.fetchall()

        if not asientos:
            messagebox.showinfo("Info", "No hay asientos para esta entrada")
            return

        # Obtener límites para crear la grilla
        max_fila = max(a[1] for a in asientos)
        max_columna = max(a[2] for a in asientos)

        matriz = [[None for _ in range(max_columna)] for _ in range(max_fila)]

        for asiento in asientos:
            id_asiento, fila, columna, disponible = asiento
            color = "green" if disponible else "red"
            state = "normal" if disponible else "disabled"

            btn = Button(frame, text=f"{fila},{columna}", bg=color, width=5, state=state)
            btn.config(command=lambda a=id_asiento, b=btn: seleccionar_asiento(a, b))
            btn.grid(row=fila - 1, column=columna - 1, padx=2, pady=2)
            matriz[fila - 1][columna - 1] = btn

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error al cargar los asientos")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass


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
def bd_InicioSesion_Verificacion(ent_usu, ent_contra, app_Inse, app, fuente, btn_res):
    if(len(ent_usu.get()) > 0 and len(ent_contra.get()) > 0):
        nombreUsuario = ent_usu.get()
        contrasena = ent_contra.get()
        try:
            conexion = iniciarConexion(vectorConexion)
            print("se abrio una conexion")
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
                    btn_res.place(relx=0.5, y=380, anchor="center", width=200, height=40)
     
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
        finally:
            try:      
                cursor.close()
                conexion.close()
                print("se cerro la conexion")
            except Exception as e:
                print("Error al cerrar la conexión:", e)
    else:
        messagebox.showerror(title="Valores Invalidos", message="Por favor llene los campos")
        ent_usu.delete(0,END)
        ent_contra.delete(0,END) 
        ent_usu.focus_set()  
