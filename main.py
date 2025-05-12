from librerias import *
import perfil_usuario
import panel_administracion
#FUNCIONES=============================================================================
#--------------------Pantalla Menu Principal
def creacionPantalla_Principal(app,fuente):
    #Bienvenidos
    lbl_1 = Label(app, text="Bienvenido", font=(fuente,20,"bold"))
    lbl_1.place(relx=0.5, y=100, anchor="center")
    #Iniciar Sesion
    btn_InSe = Button(app,text="Iniciar Sesion",font=(fuente,14,"bold"), 
                      command=partial(perfil_usuario.creacionPantalla_IniciarSesion,app,fuente))
    btn_InSe.place(relx=0.5, y= 200, anchor="center", width=200)
    #Registrarse
    btn_Regis = Button(app,text="Registrarse",font=(fuente,14,"bold"),
                       command=partial(perfil_usuario.creacionPantalla_Registrarse,app,fuente))
    btn_Regis.place(relx=0.5, y= 280, anchor="center", width=200)

#PROGRAMA PRINCIPAL====================================================================
app = Tk() #Pantalla Principal
app.title("Menu Principal")
#--------------(ancho,alto,app)
perfil_usuario.centrarPantalla(500,500,app)
#--------------Definicion de Fuentes
fuente= ("Source Code Pro")
 
#creacionPantalla_Principal(app,fuente)
#perfil_usuario.creacionPantalla_MenuUsuario(app,fuente,"a")
panel_administracion.creacionPantalla_MenuOrganizador2(app, fuente, "alumbraEventos", 3)
app.mainloop()