from librerias import * 
import librerias as lib
import funciones_generales
#FUNCIONES==============================================================================================

#OCULTAR PAGINA--------------------------------------
def ocultar_pagina(vector_paginas, paginaMostrar):
    for pagina in vector_paginas:
        if pagina != paginaMostrar:
            pagina.place_forget()

#PAGINA MENU PRINCIPAL-------------------------------
def mostrar_pagina_menuPrincipal(vector_paginas):
    panel2 = vector_paginas[0]
    panel2.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, panel2)

#PAGINA CUENTA---------------------------------------
def mostrar_pagina_cuenta(vector_paginas):
    pagina_cuenta = vector_paginas[1]
    pagina_cuenta.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_cuenta)

    lbl1 = Label(pagina_cuenta, text="Cuenta", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

#PAGINA EVENTO---------------------------------------
def mostrar_pagina_evento(vector_paginas):
    pagina_evento = vector_paginas[2]
    pagina_evento.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_evento)

    lbl1 = Label(pagina_evento, text="Crear Evento", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

#PAGINA CATEGORIAS---------------------------------------
def mostrar_pagina_categorias(vector_paginas):
    pagina_categoria = vector_paginas[3]
    pagina_categoria.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_categoria)

    lbl1 = Label(pagina_categoria, text="Categorias", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    #Añádir Categoria
    parte1 = Frame(pagina_categoria)
    parte1.place(x=0,y=30, width=390, height=470)
    #Mostrar Cateogiras
    parte2 = Frame(pagina_categoria)
    parte2.place(x=410, y=30, width=390, height=470)

#PAGINA UBICACIONES---------------------------------------
def mostrar_pagina_ubicaciones(vector_paginas):
    pagina_ubicaciones = vector_paginas[4]
    pagina_ubicaciones.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_ubicaciones)

    lbl1 = Label(pagina_ubicaciones, text="Ubicaciones", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

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
    btn_principal = Button(app_MenuOrg, text="MENU PRINCIPAL", relief="flat", command=partial(mostrar_pagina_menuPrincipal,vector_paginas))
    btn_principal.place(x=20, y=70, width=160, height=30)

    #BOTON CUENTA 
    btn_cuenta = Button(app_MenuOrg, text="CUENTA", relief="flat", command=partial(mostrar_pagina_cuenta, vector_paginas))
    btn_cuenta.place(x=20, y=100, width=160, height=30)

    #BOTON AÑADIR CATEGORIAS
    btn_categorias = Button(app_MenuOrg, text="CATEGORIAS", relief="flat", command=partial(mostrar_pagina_categorias, vector_paginas))
    btn_categorias.place(x=20, y=130, width=160, height=30)

    #BOTON AÑADIR UBICACIONES
    btn_ubicaciones = Button(app_MenuOrg, text="UBICACIONES", relief="flat", command=partial(mostrar_pagina_ubicaciones, vector_paginas))
    btn_ubicaciones.place(x=20, y=160, width=160, height=30)

    #BOTON CREAR EVENTO
    btn_evento = Button(app_MenuOrg, text="CREAR EVENTO", relief="flat", command=partial(mostrar_pagina_evento, vector_paginas))
    btn_evento.place(x=20, y=190, width=160, height=30)

    app_MenuOrg.mainloop()