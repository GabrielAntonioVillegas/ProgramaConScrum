from librerias import * 
import librerias as lib
import funciones_generales
vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]
#FUNCIONES==============================================================================================

#OCULTAR PAGINA------------------------------------------
def ocultar_pagina(vector_paginas, paginaMostrar):
    for pagina in vector_paginas:
        if pagina != paginaMostrar:
            pagina.place_forget()
#PAGINA MENU PRINCIPAL-----------------------------------
def mostrar_pagina_menuPrincipal(vector_paginas, app_MenuOrg):
    panel2 = vector_paginas[0]
    panel2.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, panel2)
#PAGINA CUENTA-------------------------------------------
def mostrar_pagina_cuenta(vector_paginas, app_MenuOrg):
    pagina_cuenta = vector_paginas[1]
    pagina_cuenta.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_cuenta)

    lbl1 = Label(pagina_cuenta, text="Cuenta", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
#PAGINA EVENTO-------------------------------------------
def mostrar_pagina_evento(vector_paginas, app_MenuOrg):
    pagina_evento = vector_paginas[2]
    pagina_evento.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_evento)

    lbl1 = Label(pagina_evento, text="Crear Evento", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
#PAGINA CATEGORIAS---------------------------------------
def mostrar_pagina_categorias(vector_paginas, app_MenuOrg):
    pagina_categoria = vector_paginas[3]
    pagina_categoria.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_categoria)

    lbl1 = Label(pagina_categoria, text="Categorias", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    #Añadir Categoria
    parte1 = Frame(pagina_categoria)
    parte1.place(x=10, y=30, width=385, height=460)

    lbl_titulo1 = Label(parte1, text="Crear / Modificar Categoria", font=(fuente, 14, "bold"))
    lbl_titulo1.place(relx=0.5, anchor="center", y=30)
    #----------------------------------------------
    lbl_id= Label(parte1, text= "Id")
    lbl_id.place(x=115, y=100)
    ent_id = Entry(parte1)
    ent_id.place(relx=0.5, anchor="center", y=130, width=150)
    ent_id.config(state='readonly')
    #----------------------------------------------
    lbl_nom = Label(parte1, text= "Nombre")
    lbl_nom.place(x=115, y=170)
    ent_nom = Entry(parte1)
    ent_nom.place(relx=0.5, anchor="center", y=200, width=150)
    
    #Mostrar Categorías
    parte2 = Frame(pagina_categoria)
    parte2.place(x=405, y=30, width=385, height=460)

    lbl_titulo2 = Label(parte2, text="Categorias Existentes", font=(fuente, 14, "bold"))
    lbl_titulo2.place(relx=0.5, anchor="center", y=30)

    trv_categorias = ttk.Treeview(parte2, columns=(1, 2), show="headings", height="15")
    trv_categorias.place(x=10,y=100, width=370)

    trv_categorias.heading(1, text="Id")
    trv_categorias.heading(2, text="Nombre Categoria")

    trv_categorias.column(1, width=20)

    mostrar_categoriasArbol(trv_categorias)
    #----------------------------------------------
    btn_guardar = Button(parte1, text="Guardar Cambios", command=partial(guardar_categorias,ent_nom, trv_categorias))
    btn_guardar.place(relx=0.5, anchor="center", y=260, width=150, height=30)

    btn_eliminar = Button(parte1, text="Eliminar Categoria")
    btn_eliminar.place(relx=0.5, anchor="center", y=320, width=150, height=30)
    btn_eliminar.config(state="disable")

    trv_categorias.bind('<ButtonRelease-1>', lambda event:tomar_datos_categoriasArbol(event, trv_categorias, ent_id, ent_nom, btn_guardar,btn_eliminar))
    app_MenuOrg.bind_all("<Button-1>", lambda event:deseleccionar(event, trv_categorias, ent_id, ent_nom, btn_guardar, btn_eliminar))
#PAGINA UBICACIONES--------------------------------------
def mostrar_pagina_ubicaciones(vector_paginas, app_MenuOrg):
    pagina_ubicaciones = vector_paginas[4]
    pagina_ubicaciones.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_ubicaciones)

    lbl1 = Label(pagina_ubicaciones, text="Ubicaciones", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
#TOMAR DATOS TREEVIEW------------------------------------
def tomar_datos_categoriasArbol(event,trv_categorias, ent_id, ent_nom, btn_guardar, btn_eliminar):
    btn_guardar.config(state="disable")
    btn_eliminar.config(state="normal")

    ent_id.config(state='normal')
    ent_nom.config(state="normal")
    ent_id.delete(0, END)
    ent_nom.delete(0, END)

    fila = trv_categorias.focus()
    valores= trv_categorias.item(fila, 'values')

    if valores:    
        ent_id.insert(0,valores[0])
        ent_nom.insert(0,valores[1])
        ent_id.config(state="readonly")
        ent_nom.config(state="readonly")
#DESELECCIONAR FILA--------------------------------------
def deseleccionar(event, trv_categorias, ent_id, ent_nom, btn_guardar, btn_eliminar):
    widget = event.widget

    if widget not in (ent_id, ent_nom, btn_guardar, btn_eliminar):
        trv_categorias.selection_remove(trv_categorias.selection())

        ent_id.config(state='normal')
        ent_nom.config(state="normal")
        ent_id.delete(0, END)
        ent_nom.delete(0, END)
        ent_id.config(state="readonly")
        
        btn_guardar.config(state="normal")
        btn_eliminar.config(state="disable")
#MOSTRAR TREEVIEW CATEGORIAS-----------------------------
def mostrar_categoriasArbol(arbol_categorias):
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Categoria")
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            arbol_categorias.insert("","end", values=("-","Ninguna categoría por ahora"))
        else:
            cursor.execute("SELECT id_categoria, nombre FROM Categoria ORDER BY id_categoria ASC")
            resultado = cursor.fetchall()

            arbol_categorias.delete(*arbol_categorias.get_children())

            for fila in resultado:
                arbol_categorias.insert("", "end", values=fila)

    except Exception as e:
        messagebox.showerror(title="Error de Conexión", message="¡Ups! Hubo un error al conectar con la Base de Datos")
        print("Error al mostrar categorías:", e)
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass
#GUARDAR CATEGORIA---------------------------------------
def guardar_categorias(ent_nom, arbol_categorias):
    if(len(ent_nom.get()) > 0):
        nombre = ent_nom.get()
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta_mail = "SELECT COUNT(*) FROM Categoria WHERE nombre = %s"
            cursor.execute(consulta_mail, (nombre,))
            resultado_categoria = cursor.fetchone()[0]
            if(resultado_categoria > 0):
                messagebox.showerror(title="Error", message="Este nombre de categoria ya está registrado.")
            else:
                consulta = "INSERT INTO Categoria (nombre) VALUES (%s)"
                cursor.execute(consulta, (nombre, ))
                conexion.commit()
                messagebox.showinfo(title="Éxito", message="¡Categoria Registrada Correctamente!")
                ent_nom.delete(0,END)
                mostrar_categoriasArbol(arbol_categorias)
        except:
            pass
        finally:
            try:
                cursor.close()
                conexion.close()
            except:
                pass
    else:
        ent_nom.delete(0,END)
        ent_nom.focus()
        messagebox.showerror(title="Campos vacios", message="Por favor llene los campos")


#FUNCION PRINCIPAL=====================================================================================
def creacionPantalla_MenuOrganizador2(app, _fuente, nombreUsuario):
    global fuente
    fuente = _fuente
    app_MenuOrg = Toplevel(app)
    app_MenuOrg.title("Sesion Organizador")
    funciones_generales.centrarPantalla(1000, 500, app_MenuOrg)

    #PANEL 1 (izquierda, el mas angosto)
    panel1 = Frame(app_MenuOrg, bg="gray")
    panel1.place(x=0, width=200, height=500)

    #PANEL 2 (derecha, el mas ancho)
    panel2 = Frame(app_MenuOrg)
    panel2.place(x=200, width=800, height=500)

    #COMPONENTES PARA EL PANEL 1--------------------
    lbl1 = Label(panel2, text=("¡Bienvenido/a " + nombreUsuario + "!"), font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    #PAGINA CUENTA
    pagina_cuenta = Frame(app_MenuOrg, background="gainsboro")
    pagina_cuenta.place(x=200, width=800, height=500)

    #PAGINA EVENTO
    pagina_evento = Frame(app_MenuOrg, background="gainsboro")
    pagina_evento.place(x=200, width=800, height=500)

    #PAGINA CATEGORIAS
    pagina_categoria = Frame(app_MenuOrg, background="gainsboro")
    pagina_categoria.place(x=200, width=800, height=500)

    #PAGINA UBICACIONES
    pagina_ubicaciones = Frame(app_MenuOrg, background="gainsboro")
    pagina_ubicaciones.place(x=200, width=800, height=500)

    #VECTOR CON TODOS LAS PAGINAS
    vector_paginas = [panel2, pagina_cuenta, pagina_evento, pagina_categoria, pagina_ubicaciones]

    for i in range(len(vector_paginas)):
        if vector_paginas[i] != panel2:
            vector_paginas[i].place_forget()

    #COMPONENTES PARA EL PANEL 2--------------------
    #BOTON VOLVER
    btn_volver = Button(app_MenuOrg, text="🡸", command=partial(funciones_generales.cerrar_abrirVentanas, app_MenuOrg, app))
    btn_volver.place(x=10, y=10)

    #BOTON MENU PRINCIPAL
    btn_principal = Button(app_MenuOrg, text="MENU PRINCIPAL", relief="flat", command=partial(mostrar_pagina_menuPrincipal,vector_paginas, app_MenuOrg))
    btn_principal.place(x=20, y=70, width=160, height=30)

    #BOTON CUENTA 
    btn_cuenta = Button(app_MenuOrg, text="CUENTA", relief="flat", command=partial(mostrar_pagina_cuenta, vector_paginas, app_MenuOrg))
    btn_cuenta.place(x=20, y=100, width=160, height=30)

    #BOTON AÑADIR CATEGORIAS
    btn_categorias = Button(app_MenuOrg, text="CATEGORIAS", relief="flat", command=partial(mostrar_pagina_categorias, vector_paginas, app_MenuOrg))
    btn_categorias.place(x=20, y=130, width=160, height=30)

    #BOTON AÑADIR UBICACIONES
    btn_ubicaciones = Button(app_MenuOrg, text="UBICACIONES", relief="flat", command=partial(mostrar_pagina_ubicaciones, vector_paginas, app_MenuOrg))
    btn_ubicaciones.place(x=20, y=160, width=160, height=30)

    #BOTON CREAR EVENTO
    btn_evento = Button(app_MenuOrg, text="CREAR EVENTO", relief="flat", command=partial(mostrar_pagina_evento, vector_paginas, app_MenuOrg))
    btn_evento.place(x=20, y=190, width=160, height=30)

    app_MenuOrg.mainloop()



