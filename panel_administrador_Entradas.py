from librerias import * 
import librerias as lib
import funciones_generales
from tkcalendar import DateEntry
from datetime import datetime
vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]
COLOR_NORMAL = "#f0f0f0"
COLOR_ACTIVO = "gainsboro"

#PAGINA ENTRADAS-----------------------------------------
def mostrar_pagina_entradas(vector_paginas,app_MenuOrg,botones,btn_seleccionado, fuente):
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)

    pagina_entradas = vector_paginas[1]
    pagina_entradas.place(x=200, width=800, height=500)
    funciones_generales.ocultar_pagina(vector_paginas, pagina_entradas)

    lbl1 = Label(pagina_entradas, text="Entradas", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)