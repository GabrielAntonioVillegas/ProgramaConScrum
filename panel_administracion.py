from librerias import * 
import librerias as lib
import funciones_generales

def creacionPantalla_MenuOrganizador(app,fuente,nombreUsuario):
    app_MenuOrg = Toplevel(app)
    app_MenuOrg.title("Sesion Organizador")
    funciones_generales.centrarPantalla(1000,500,app_MenuOrg)
    #PANEL 1 (izquierda, el mas angosto)
    panel1 = Frame(app_MenuOrg, bg="gainsboro")
    panel1.place(x=0, width=200, height=500)
    #PANEL 2 (derecha, el mas ancho)
    panel2 = Frame(app_MenuOrg)
    panel2.place(x=200, width=800, height=500)
    #BOTON VOLVER
    btn_volver = Button(app_MenuOrg, text="🡸", command=partial(funciones_generales.cerrar_abrirVentanas,app_MenuOrg,app))
    btn_volver.place(x=10,y=10)
    #COMPONENTES PARA EL PANEL 1
    lbl1 = Label(panel2, text=("¡Bienvenido/a "+nombreUsuario+"!"), font=(fuente, 16, "bold"))
    lbl1.place(relx=0.5, y=50, anchor="center")

    #COMPONENTES PARA EL PANEL 2 