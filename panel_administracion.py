from librerias import * 
import librerias as lib
import funciones_generales

#FUNCIONES==============================================================================================

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

#PAGINA EVENTO---------------------------------------
def mostrar_pagina_evento(vector_paginas):
    pagina_evento = vector_paginas[2]
    pagina_evento.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_evento)

#FUNCION PRINCIPAL=====================================================================================
def creacionPantalla_MenuOrganizador2(app, fuente, nombreUsuario):
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
    lbl1 = Label(panel2, text=("¡Bienvenido/a " + nombreUsuario + "!"), font=(fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=50, anchor="center")

    #PAGINA CUENTA
    pagina_cuenta = Frame(app_MenuOrg)
    pagina_cuenta.place(x=200, width=800, height=500)

    #PAGINA EVENTO
    pagina_evento = Frame(app_MenuOrg)
    pagina_evento.place(x=200, width=800, height=500)

    #VECTOR CON TODOS LAS PAGINAS
    vector_paginas = [panel2, pagina_cuenta, pagina_evento]

    for i in range(len(vector_paginas)):
        if vector_paginas[i] != panel1:
            vector_paginas[i].place_forget()

    #COMPONENTES PARA EL PANEL 2--------------------
    #BOTON VOLVER
    btn_volver = Button(app_MenuOrg, text="🡸", command=partial(funciones_generales.cerrar_abrirVentanas, app_MenuOrg, app))
    btn_volver.place(x=10, y=10)

    #BOTON MENU PRINCIPAL
    btn_principal = Button(app_MenuOrg, text="MENU PRINCIPAL", relief="flat", command=partial(mostrar_pagina_menuPrincipal,vector_paginas))
    btn_principal.place(x=20, y=70, width=180, height=30)

    #BOTON CUENTA 
    btn_cuenta = Button(app_MenuOrg, text="CUENTA", relief="flat", command=partial(mostrar_pagina_cuenta, vector_paginas))
    btn_cuenta.place(x=20, y=100, width=180, height=30)

    #BOTON CREAR EVENTO
    btn_evento = Button(app_MenuOrg, text="CREAR EVENTO", relief="flat", command=partial(mostrar_pagina_evento, vector_paginas))
    btn_evento.place(x=20, y=130, width=180, height=30)

    app_MenuOrg.mainloop()