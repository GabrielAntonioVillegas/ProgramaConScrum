from librerias import * 
import librerias as lib
import funciones_generales
from tkcalendar import DateEntry
from datetime import datetime
import panel_administrador_Notificaciones
from panel_administrador_Entradas import mostrar_pagina_entradas
import panel_administrador_Entradas
from datetime import date
from datetime import timedelta

vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]
COLOR_NORMAL = "#f0f0f0"
COLOR_ACTIVO = "gainsboro"


#FUNCIONES==============================================================================================


#PAGINA MENU PRINCIPAL-----------------------------------
def mostrar_pagina_menuPrincipal(vector_paginas, app_MenuOrg, botones, btn_seleccionado, id_organizador):
    # Cambiar el estado del botón seleccionado
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)
    
    # Mostrar la página
    panel2 = vector_paginas[0]
    panel2.place(x=200, width=800, height=500)
    funciones_generales.ocultar_pagina(vector_paginas, panel2)

    # Crear un Treeview para mostrar los eventos
    treeview = ttk.Treeview(panel2, columns=("titulo", "fecha_inicio", "fecha_fin", "entradas_totales", "entradas_vendidas", "entradas_disponibles"), show="headings")
    
    # Definir las columnas
    treeview.heading("titulo", text="Título")
    treeview.heading("fecha_inicio", text="Fecha Inicio")
    treeview.heading("fecha_fin", text="Fecha Fin")
    treeview.heading("entradas_totales", text="Entradas Totales")
    treeview.heading("entradas_vendidas", text="Entradas Vendidas")
    treeview.heading("entradas_disponibles", text="Entradas Disponibles")
    
    # Establecer el tamaño de las columnas
    treeview.column("titulo", width=150)
    treeview.column("fecha_inicio", width=120)
    treeview.column("fecha_fin", width=120)
    treeview.column("entradas_totales", width=120)
    treeview.column("entradas_vendidas", width=120)
    treeview.column("entradas_disponibles", width=120)
    
    # Ubicar el Treeview en el panel
    treeview.place(x=20, y=50, width=760, height=400)
    
    # Llamar a la función que obtiene los datos y llena el Treeview
    mostrar_eventos_con_estadisticas(treeview, id_organizador)
#Mostrar Treeview Eventos Con Estadisticas---------------
def mostrar_eventos_con_estadisticas(arbol_eventos, id_organizador):
    try:
        # Establecer conexión a la base de datos
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        # Consulta para obtener los eventos activos para el organizador
        consulta = """
            SELECT E.id_evento, E.titulo, E.fecha_inicio, E.fecha_fin, 
                   SUM(En.cupo_total) as entradas_totales,
                   SUM(En.cupo_total - En.cupo_disponible) as entradas_vendidas,
                   SUM(En.cupo_disponible) as entradas_disponibles
            FROM Evento E
            JOIN Entrada En ON E.id_evento = En.evento_id
            WHERE E.id_organizador = %s AND E.estado = 'activo'
            GROUP BY E.id_evento, E.titulo, E.fecha_inicio, E.fecha_fin
        """
        cursor.execute(consulta, (id_organizador,))
        eventos = cursor.fetchall()

        # Limpiar el árbol antes de agregar nuevos datos
        for item in arbol_eventos.get_children():
            arbol_eventos.delete(item)

        # Insertar los datos de los eventos en el Treeview
        for evento in eventos:
            id_evento = evento[0]
            titulo = evento[1]
            fecha_inicio = evento[2]
            fecha_fin = evento[3]
            entradas_totales = evento[4]
            entradas_vendidas = evento[5]
            entradas_disponibles = evento[6]
            
            # Insertar la fila en el Treeview
            arbol_eventos.insert("", "end", values=(
                titulo, 
                fecha_inicio.strftime("%Y-%m-%d %H:%M:%S"),
                fecha_fin.strftime("%Y-%m-%d %H:%M:%S"),
                entradas_totales,
                entradas_vendidas,
                entradas_disponibles
            ))

    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"Hubo un error al conectar con la base de datos: {err}")
    finally:
        cursor.close()
        conexion.close()
#
#
#
#PAGINA EVENTO-------------------------------------------
def eleccion_paginaEvento(vector_paginas, app_MenuOrg, botones, btn_seleccionado, id_organizador):
    if(verificar_Ubicaciones_Categorias_Evento() == False):
        mostrar_pagina_eventoNoPosible(app_MenuOrg, vector_paginas)
    else:
        mostrar_pagina_evento(vector_paginas, app_MenuOrg, botones, btn_seleccionado, id_organizador)
#MOSTRAR PAGINA EN CASO DE EVENTO NO POSIBLE-------------
def mostrar_pagina_eventoNoPosible(app_MenuOrg, vector_paginas):
    pagina_evento = vector_paginas[5]
    pagina_evento.place(x=200, width=800, height=500)
    funciones_generales.ocultar_pagina(vector_paginas, pagina_evento)

    lbl1 = Label(pagina_evento, text="Eventos", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    parte1 = Frame(pagina_evento)
    parte1.place(x=10, y=30, width=780, height=460)
    lbl_titulo1 = Label(parte1, text="¡Ups! Es imposible Crear un Evento si no\nhay al menos 1 Categoria y 1 Ubicacion Registradas", font=(fuente, 14, "bold"))
    lbl_titulo1.place(relx=0.5, anchor="center", y=30)
#MOSTRAR PAGINA EVENTO-----------------------------------
def mostrar_pagina_evento(vector_paginas, app_MenuOrg, botones, btn_seleccionado, id_organizador):
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)

    pagina_evento = vector_paginas[2]
    pagina_evento.place(x=200, width=800, height=500)
    funciones_generales.ocultar_pagina(vector_paginas, pagina_evento)

    lbl1 = Label(pagina_evento, text="Eventos", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
    
    # Componentes Graficos
    parte1 = Frame(pagina_evento)
    parte1.place(x=10, y=30, width=385, height=460)

    lbl_titulo1 = Label(parte1, text="Crear / Modificar Evento", font=(fuente, 14, "bold"))
    lbl_titulo1.place(relx=0.5, anchor="center", y=30)
    #ID-----------------------------------
    lbl_id = Label(parte1, text="Id")
    lbl_id.place(x=30, y=50)
    ent_id = Entry(parte1)
    ent_id.place(x=30, y=70, width=150, height=20)
    ent_id.config(state="readonly")
    #TITULO-------------------------------
    lbl_tit = Label(parte1, text="Titulo")
    lbl_tit.place(x=30, y=100)
    ent_tit = Entry(parte1)
    ent_tit.place(x=30, y=120, width=150, height=20)
    #CATEGORIA----------------------------
    lbl_cat = Label(parte1, text="Categoria")
    lbl_cat.place(x=30, y=150)
    combo_cate = ttk.Combobox(parte1)
    combo_cate.config(state="readonly")
    combo_cate.place(x=30, y=170, width=150, height=20)
    #UBICACION----------------------------
    lbl_ubi = Label(parte1, text="Ubicacion")
    lbl_ubi.place(x=210, y=150)
    combo_ubi = ttk.Combobox(parte1)
    combo_ubi.config(state="readonly")
    combo_ubi.place(x=210, y=170, width=150, height=20)
    #FECHA DE INICIO----------------------
    lbl_fe_ini = Label(parte1, text="Fecha Inicio")
    lbl_fe_ini.place(x=30, y=200)
    dateEntry_inicio = DateEntry(parte1,mindate=date.today(), date_pattern='yyyy-mm-dd')
    dateEntry_inicio.delete(0, "end")
    #dateEntry_inicio.config(state="readonly")
    dateEntry_inicio.place(x=30, y=220, width=150, height=20)
    

    lbl_hr_ini = Label(parte1, text="Hora")
    lbl_hr_ini.place(x=30, y=245)
    spin_hr_ini = ttk.Spinbox(parte1, from_=0, to=23, width=3, format="%02.0f")
    spin_hr_ini.place(x=30, y=265, width=60)
    spin_hr_ini.config(state="readonly")

    lbl_min_ini = Label(parte1, text="Minutos")
    lbl_min_ini.place(x=120, y=245)
    spin_min_ini = ttk.Spinbox(parte1, from_=0, to=59, width=3, format="%02.0f")
    spin_min_ini.place(x=120, y=265, width=60)
    spin_min_ini.config(state="readonly")
    #FECHA DE FINAL-----------------------
    lbl_fe_fin = Label(parte1, text="Fecha Final")
    lbl_fe_fin.place(x=210, y=200)
    dateEntry_fin = DateEntry(parte1,mindate=date.today(),date_pattern='yyyy-mm-dd')
    dateEntry_fin.delete(0, "end")
    #dateEntry_fin.config(state="readonly")
    dateEntry_fin.place(x=210, y=220, width=150, height=20)
    dateEntry_fin.delete(0, 'end')
        
    lbl_hr_fin = Label(parte1, text="Hora")
    lbl_hr_fin.place(x=210, y=245)
    spin_hr_fin = ttk.Spinbox(parte1, from_=0, to=23, width=3, format="%02.0f")
    spin_hr_fin.place(x=210, y=265, width=60)
    spin_hr_fin.config(state="readonly")

    lbl_min_fin = Label(parte1, text="Minutos")
    lbl_min_fin.place(x=300, y=245)
    spin_min_fin = ttk.Spinbox(parte1, from_=0, to=59, width=3, format="%02.0f")
    spin_min_fin.place(x=300, y=265, width=60)
    spin_min_fin.config(state="readonly")
    #ESTADO--------------------------------
    lista = ["activo","cancelado","finalizado"]
    lbl_estado = Label(parte1, text="Estado")
    lbl_estado.place(x=30, y=290)
    combo_est = ttk.Combobox(parte1, values=lista)
    combo_est.config(state="readonly")
    combo_est.place(x=30, y=310, width=150, height=20)
    #DESCRIPCION---------------------------
    lbl_desc = Label(parte1, text="Descripcion")
    lbl_desc.place(x=30, y=340)
    ent_desc = Entry(parte1)
    ent_desc.place(x=30, y=360, width=330, height=40)
    #Eventos Existentes 
    parte2 = Frame(pagina_evento)
    parte2.place(x=405, y=30, width=385, height=460)
    lbl_titulo2 = Label(parte2, text="Eventos Existentes", font=(fuente, 14, "bold"))
    lbl_titulo2.place(relx=0.5, anchor="center", y=30)

    trv_evento = ttk.Treeview(parte2,columns=(1, 2, 3, 4), show="headings",height="15")
    trv_evento.place(x=10,y=100, width=370)
    trv_evento.heading(1, text="")
    trv_evento.heading(2, text="Título")
    trv_evento.heading(3, text="Dirección")
    trv_evento.heading(4, text="Fecha")
    trv_evento.column(1, width=0, stretch=False)
    trv_evento.column(2, width=80)
    trv_evento.column(3, width=140)
    trv_evento.column(4, width=200)

    mostrar_eventosArbol(trv_evento, id_organizador)
    dictCategorias, dictUbicaciones = mostrar_CategoriasUbicaciones(combo_cate, combo_ubi)

    btn_guardar = Button(parte1, text="Guardar Cambios", 
                         command=partial(guardar_evento,ent_id, ent_tit, combo_cate, combo_ubi, dateEntry_inicio, dateEntry_fin, combo_est, 
                                         ent_desc,id_organizador,  dictCategorias, dictUbicaciones,trv_evento, spin_hr_ini, spin_min_ini, 
                                         spin_hr_fin, spin_min_fin))
    btn_guardar.place(x=30, y=415, width=150, height=30)

    btn_eliminar = Button(parte1, text="Eliminar Evento",
                          command=partial(eliminar_evento,ent_id, ent_tit, combo_cate, combo_ubi, dateEntry_inicio, dateEntry_fin, combo_est, 
                                          ent_desc,trv_evento, spin_hr_ini, spin_min_ini, spin_hr_fin, spin_min_fin, id_organizador))
    btn_eliminar.place(x=210, y=415, width=150, height=30)
    btn_eliminar.config(state="disable")

    trv_evento.bind('<ButtonRelease-1>', lambda event:
                    tomar_datos_eventosArbol(event, ent_id, ent_tit, combo_cate, combo_ubi, dateEntry_inicio, dateEntry_fin, combo_est, 
                                            ent_desc, id_organizador,  dictCategorias, dictUbicaciones, trv_evento, btn_eliminar))
#VERIFICAR QUE EXISTAN CATEGORIAS Y UBICACIONES----------   
def verificar_Ubicaciones_Categorias_Evento():
    estado = False
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        consulta = "SELECT 1 FROM Categoria LIMIT 1 "
        cursor.execute(consulta)
        resultado = cursor.fetchone()
        if resultado:
            consulta2 = "SELECT 1 FROM Ubicacion LIMIT 1"
            cursor.execute(consulta2)
            resultado2 = cursor.fetchone()
            if resultado2:
                estado = True 
    except Exception as e:
        messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
        print (e)
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass
    return estado
#MOSTRAR EVENTOS ARBOL-----------------------------------
def mostrar_eventosArbol(arbol_eventos, id_organizador):
    try:
        funciones_generales.actualizar_estados_eventos(vectorConexion)
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = "SELECT COUNT(*) FROM Evento WHERE id_organizador=%s"
        cursor.execute(consulta, (id_organizador,))
        cantidad = cursor.fetchone()[0]
        if cantidad ==0:
            arbol_eventos.insert("","end", values=("-","-","No tienes ningun Evento por ahora"))
        else:
            consulta= "SELECT Evento.id_evento, Evento.titulo, Ubicacion.direccion, Evento.fecha_inicio, Evento.fecha_fin FROM Evento JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion WHERE id_organizador = %s AND estado = 'activo';"
            cursor.execute(consulta, (id_organizador,))
            resultado = cursor.fetchall()
            arbol_eventos.delete(*arbol_eventos.get_children())

            for fila in resultado:
                id_evento, titulo, direccion, fecha_ini, fecha_fin = fila
                
                #Formatear las fechas para mostrar solo la fecha (sin la hora)
                fecha_ini_formateada = datetime.strptime(str(fecha_ini), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
                fecha_fin_formateada = datetime.strptime(str(fecha_fin), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
                
                fechas = f"{fecha_ini_formateada} al {fecha_fin_formateada}"

                
                arbol_eventos.insert("", "end", values=(id_evento, titulo, direccion, fechas))
    except Exception as e:
        messagebox.showerror(title="Error de Conexión", message="¡Ups! Hubo un error al conectar con la Base de Datos")
        print("Error al mostrar eventos:", e)
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass
#MOSTRAR CATEGORIAS Y UBICACIONES------------------------
def mostrar_CategoriasUbicaciones(combo_cate, combo_ubi):
    vectorCategorias = []
    vectorUbicaciones = []
    dictCategorias = {}
    dictUbicaciones = {}

    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta1 = "SELECT id_categoria, nombre FROM Categoria WHERE activo = 1 ORDER BY id_categoria ASC"
        consulta2 = "SELECT id_ubicacion, direccion FROM Ubicacion WHERE activo = 1 ORDER BY id_ubicacion ASC"
        
        cursor.execute(consulta1)
        resultado = cursor.fetchall()

        cursor.execute(consulta2)
        resultado2 = cursor.fetchall()

        if resultado and resultado2:
            for id_cat, nombre in resultado:
                vectorCategorias.append(nombre)
                dictCategorias[nombre] = id_cat

            for id_ubi, direccion in resultado2:
                vectorUbicaciones.append(direccion)
                dictUbicaciones[direccion] = id_ubi

            combo_cate["values"] = vectorCategorias
            combo_ubi["values"] = vectorUbicaciones

    except Exception as e:
        messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
        print(e)
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

    return dictCategorias, dictUbicaciones
#GUARDAR EVENTO------------------------------------------
def guardar_evento(ent_id, ent_tit, combo_cate, combo_ubi, dateEntry_inicio, dateEntry_fin, combo_est, ent_desc, id_organizador,  
                   dictCategorias, dictUbicaciones, arbol_eventos, spin_hr_ini, spin_min_ini, spin_hr_fin, spin_min_fin):
    #VALIDACION DE QUE NINGUN  WIDGET QUEDE VACIO
    if(len(ent_tit.get()) > 0 and len(combo_cate.get()) > 0 and len(combo_ubi.get()) > 0 and len(dateEntry_inicio.get()) > 0 and
       len(dateEntry_fin.get()) > 0 and len(combo_est.get()) > 0 and len(spin_hr_ini.get()) > 0 and len(spin_min_ini.get()) > 0 and
       len(spin_hr_fin.get()) > 0 and len(spin_min_fin.get()) > 0):
        
        
        fecha_inicio_date = dateEntry_inicio.get_date()
        fecha_fin_date = dateEntry_fin.get_date()

        hora_inicio = int(spin_hr_ini.get())
        minuto_inicio = int(spin_min_ini.get())
        hora_fin = int(spin_hr_fin.get())
        minuto_fin = int(spin_min_fin.get())

        fechaInicio_dt = datetime(year=fecha_inicio_date.year,month=fecha_inicio_date.month,day=fecha_inicio_date.day,hour=hora_inicio,minute=minuto_inicio)
        fechaFinal_dt = datetime(year=fecha_fin_date.year,month=fecha_fin_date.month,day=fecha_fin_date.day,hour=hora_fin,minute=minuto_fin)
        #VALIDACION QUE LA FECHA FINAL NO SEA MAYOR O IGUAL A LA FECHA DE INICIO (Incluye la hora en el analisis)
        if(fechaFinal_dt <= fechaInicio_dt):
            messagebox.showerror(title="Fechas inválidas", message="La fecha y hora de fin no pueden ser anteriores o iguales a la de inicio.")
        else:
            titulo = ent_tit.get()
            id_categoria = dictCategorias[combo_cate.get()]
            id_ubicacion = dictUbicaciones[combo_ubi.get()]
            descripcion = ent_desc.get()    
            estado = combo_est.get()

            try: 
                fechaInicio = fechaInicio_dt.strftime("%Y-%m-%d %H:%M:%S")
                fechaFinal = fechaFinal_dt.strftime("%Y-%m-%d %H:%M:%S")

                conexion = funciones_generales.iniciarConexion(vectorConexion)
                cursor = conexion.cursor()

                consulta = "SELECT COUNT(*) FROM Evento WHERE titulo = %s and id_organizador = %s and id_categoria = %s and id_ubicacion = %s and fecha_inicio = %s and fecha_fin = %s and estado = %s"
                cursor.execute(consulta, (titulo, id_organizador, id_categoria, id_ubicacion, fechaInicio, fechaFinal, estado, ))
                resultado = cursor.fetchone()[0]

                if resultado > 0:
                    messagebox.showerror(title="Error", message="Este evento ya está registrado.")
                else:
                    #MODIFICAR------------------
                    if len(ent_id.get()) > 0:
                        id = ent_id.get()

                        consulta2 = "SELECT COUNT(*) FROM Evento WHERE id_ubicacion = %s and fecha_inicio = %s and fecha_fin = %s and id_evento != %s"
                        cursor.execute(consulta2, (id_ubicacion, fechaInicio, fechaFinal, id, ))
                        resultado2 = cursor.fetchone()[0]

                        consulta_solapamiento = "SELECT COUNT(*) FROM Evento WHERE id_ubicacion = %s AND fecha_inicio < %s AND fecha_fin > %s and id_evento != %s"
                        cursor.execute(consulta_solapamiento, (id_ubicacion, fechaFinal, fechaInicio, id))
                        solapados = cursor.fetchone()[0]

                        if(resultado2 > 0 or solapados > 0):
                            messagebox.showerror(title="Error", message="¡Ups! Parece que ya hay eventos que transcurren en el mismo lugar, fechas y horarios")
                        else:
                            consulta = "UPDATE Evento SET titulo=%s, descripcion=%s, id_categoria=%s, fecha_inicio=%s, fecha_fin=%s, estado=%s, id_ubicacion=%s WHERE id_evento = %s"
                            valores = (titulo, descripcion, id_categoria, fechaInicio, fechaFinal, estado, id_ubicacion, id)
                            cursor.execute(consulta, valores)
                            conexion.commit()
                            messagebox.showinfo(title="Éxito", message="¡Evento Actualizado Correctamente!")
                            #NOTIFICACION DE QUE SE HA CREADO EL EVENTO
                            consulta_Notificacion = "INSERT INTO Notificacion (id_evento, descripcion_noti, fecha) VALUES (%s,%s,NOW())"
                            descripcionNotificacion = "¡Ey! El evento " + titulo + " para el que tienes una entrada ha sufrido una modificacion, verifica los cambios realizados en el apartado de Busqueda de Eventos"
                            cursor.execute(consulta_Notificacion, (id, descripcionNotificacion, ))
                            conexion.commit()
                            #NOTIFICACION RECORDATORIO DE ASISTENCIA AL EVENTO
                            fecha_notificacion = fechaInicio_dt - timedelta(days=1)
                            fecha_notificacion_str = fecha_notificacion.strftime("%Y-%m-%d %H:%M:%S")
                            consulta_Recordatorio = "INSERT INTO Notificacion (id_evento, descripcion_noti, fecha) VALUES (%s,%s,%s)"
                            descripcionRecordatorio = "¡Ey! El evento " + titulo + " para el que tienes una entrada ha sufrido una modificacion, verifica los cambios realizados en el apartado de Busqueda de Eventos"
                            cursor.execute(consulta_Recordatorio, (id, descripcionRecordatorio,fecha_notificacion_str, ))
                            conexion.commit()
                    #GUARDAR--------------------
                    else:
                        
                        consulta2 = "SELECT COUNT(*) FROM Evento WHERE id_ubicacion = %s and fecha_inicio = %s and fecha_fin = %s"
                        cursor.execute(consulta2, (id_ubicacion, fechaInicio, fechaFinal, ))
                        resultado2 = cursor.fetchone()[0]

                        consulta_solapamiento = "SELECT COUNT(*) FROM Evento WHERE id_ubicacion = %s AND fecha_inicio < %s AND fecha_fin > %s"
                        cursor.execute(consulta_solapamiento, (id_ubicacion, fechaFinal, fechaInicio, ))
                        solapados = cursor.fetchone()[0]

                        if(resultado2 > 0 or solapados > 0):
                            messagebox.showerror(title="Error", message="¡Ups! Parece que ya hay eventos que transcurren en el mismo lugar, fechas y horarios")
                        else:
                            consulta = "INSERT INTO Evento (id_organizador, titulo, descripcion, id_categoria, fecha_inicio, fecha_fin, estado, id_ubicacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(consulta, (id_organizador, titulo, descripcion, id_categoria, fechaInicio, fechaFinal, estado, id_ubicacion))
                            conexion.commit()
                            messagebox.showinfo(title="Éxito", message="¡Evento Registrado Correctamente!")

                            idReciente = cursor.lastrowid
                            consulta_Notificacion = "INSERT INTO Notificacion (id_evento, descripcion_noti, fecha) VALUES (%s,%s,NOW())"
                            descripcionNotificacion = "¡Ey! Se ha creado el evento " + titulo + ", de la categoria " + combo_cate.get().lower() + ". Puedes encontrarlo ya en el apartado Busqueda de Eventos"
                            cursor.execute(consulta_Notificacion, (idReciente, descripcionNotificacion, ))
                            conexion.commit()

                    #Limpiar todos los Cambos-----------------
                    ent_id.config(state="normal")
                    ent_id.delete(0, "end")
                    ent_id.config(state="readonly")
                    ent_tit.delete(0, "end")
                    combo_cate.set("")
                    combo_ubi.set("")
                    dateEntry_inicio.config(state="normal")
                    dateEntry_inicio.delete(0, "end")
                    dateEntry_inicio.config(state="readonly")
                    spin_hr_ini.config(state="normal")
                    spin_hr_ini.delete(0, "end")
                    spin_hr_ini.config(state="readonly")
                    spin_min_ini.config(state="normal")
                    spin_min_ini.delete(0, "end")
                    spin_min_ini.config(state="readonly")
                    dateEntry_fin.config(state="normal")
                    dateEntry_fin.delete(0, "end")
                    dateEntry_fin.config(state="readonly")
                    spin_hr_fin.config(state="normal")
                    spin_hr_fin.delete(0, "end")
                    spin_hr_fin.config(state="readonly")
                    spin_min_fin.config(state="normal")
                    spin_min_fin.delete(0, "end")
                    spin_min_fin.config(state="readonly")
                    combo_est.set("")
                    ent_desc.delete(0, "end")
                    mostrar_eventosArbol(arbol_eventos, id_organizador)

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
        messagebox.showerror(title="Campos vacíos", message="Por favor llene todos los campos.")
#ELIMINAR EVENTO-----------------------------------------
def eliminar_evento(ent_id, ent_tit, combo_cate, combo_ubi, dateEntry_inicio, dateEntry_fin, combo_est, ent_desc,
                    arbol_eventos, spin_hr_ini, spin_min_ini, spin_hr_fin, spin_min_fin, id_organizador):
    
    if(len(ent_tit.get()) > 0 and len(combo_cate.get()) > 0 and len(combo_ubi.get()) > 0 and len(dateEntry_inicio.get()) > 0 and
       len(dateEntry_fin.get()) > 0 and len(combo_est.get()) > 0 and len(spin_hr_ini.get()) > 0 and len(spin_min_ini.get()) > 0 and
       len(spin_hr_fin.get()) > 0 and len(spin_min_fin.get()) > 0):
        
        id = ent_id.get()
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta = "UPDATE Evento SET estado = 'cancelado' WHERE id_evento = %s"
            cursor.execute(consulta,(id, ))
            conexion.commit()
            messagebox.showinfo(title="Éxito", message="¡Evento Cancelado Correctamente!")

            consulta_Notificacion = "INSERT INTO Notificacion (id_evento, descripcion_noti, fecha) VALUES (%s,%s,NOW())"
            descripcionNotificacion = "¡Ups! El evento " + ent_tit.get() + " ha sido cancelado. Lamentamos el inconveniente, recibiras un reembolso de la compra pronto"
            cursor.execute(consulta_Notificacion, (id, descripcionNotificacion, ))
            conexion.commit()
            #Limpiar todos los Cambos-----------------
            ent_id.config(state="normal")
            ent_id.delete(0, "end")
            ent_id.config(state="readonly")
            ent_tit.delete(0, "end")
            combo_cate.set("")
            combo_ubi.set("")
            dateEntry_inicio.config(state="normal")
            dateEntry_inicio.delete(0, "end")
            dateEntry_inicio.config(state="readonly")
            spin_hr_ini.config(state="normal")
            spin_hr_ini.delete(0, "end")
            spin_hr_ini.config(state="readonly")
            spin_min_ini.config(state="normal")
            spin_min_ini.delete(0, "end")
            spin_min_ini.config(state="readonly")
            dateEntry_fin.config(state="normal")
            dateEntry_fin.delete(0, "end")
            dateEntry_fin.config(state="readonly")
            spin_hr_fin.config(state="normal")
            spin_hr_fin.delete(0, "end")
            spin_hr_fin.config(state="readonly")
            spin_min_fin.config(state="normal")
            spin_min_fin.delete(0, "end")
            spin_min_fin.config(state="readonly")
            combo_est.set("")
            ent_desc.delete(0, "end")

            
            arbol_eventos.selection_remove(arbol_eventos.selection())
            funciones_generales.limpiar_treeview(arbol_eventos)
            mostrar_eventosArbol(arbol_eventos, id_organizador)
        except mysql.connector.IntegrityError as e:  
            if e.errno == 1451: 
                messagebox.showerror(title="Error de Eliminación", message="No se puede eliminar el evento, ya que tiene entradas asociadas.")
            
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
        finally: 
            try:
                cursor.close()
                conexion.close()
            except:
                pass
    else:
        messagebox.showerror(title="Campos vacíos", message="Por favor llene todos los campos.")
#TOMAR DATOS TREEVIEW------------------------------------
def tomar_datos_eventosArbol(event, ent_id, ent_tit, combo_cate, combo_ubi, dateEntry_inicio, dateEntry_fin, combo_est, 
                             ent_desc, id_organizador, dictCategorias, dictUbicaciones, arbol_eventos, btn_eliminar):
    btn_eliminar.config(state="normal")
    ent_id.config(state='normal')

    fila = arbol_eventos.focus()
    valores = arbol_eventos.item(fila, 'values')    

    if valores:
        id_evento = valores[0] 
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta = "SELECT Evento.id_evento, Evento.titulo, Evento.descripcion, Categoria.nombre, Evento.fecha_inicio, Evento.fecha_fin,  Evento.estado, Ubicacion.direccion FROM Evento JOIN Categoria ON Evento.id_categoria = Categoria.id_categoria JOIN Ubicacion ON Evento.id_ubicacion = Ubicacion.id_ubicacion WHERE Evento.id_evento = %s"
            cursor.execute(consulta, (id_evento,))
            resultado = cursor.fetchone()  

            if resultado: 
                ent_id.delete(0, END)
                ent_tit.delete(0, END)
                combo_cate.delete(0, END)
                combo_ubi.delete(0, END)
                dateEntry_inicio.delete(0, 'end')
                dateEntry_fin.delete(0, 'end')
                combo_est.delete(0, END)
                ent_desc.delete(0, END)

                ent_id.insert(0,resultado[0])
                ent_tit.insert(0, resultado[1])
                ent_desc.insert(0, resultado[2])
                combo_cate.set(resultado[3])

                dateEntry_inicio.set_date(resultado[4])
                dateEntry_fin.set_date(resultado[5])

                combo_est.set(resultado[6])
                combo_ubi.set(resultado[7])

                ent_id.config(state='readonly')
        except Exception as e:
            messagebox.showerror(title="Error de Conexión", message="¡Ups! Hubo un error al conectar con la Base de Datos")
            print("Error al mostrar eventos:", e)

        finally:
            try:
                cursor.close()
                conexion.close()
            except:
                pass
# 
#
#  
#PAGINA UBICACIONES--------------------------------------
def mostrar_pagina_ubicaciones(vector_paginas, app_MenuOrg, botones, btn_seleccionado):
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)
    
    pagina_ubicaciones = vector_paginas[4]
    pagina_ubicaciones.place(x=200, width=800, height=500)
    funciones_generales.ocultar_pagina(vector_paginas, pagina_ubicaciones)

    lbl1 = Label(pagina_ubicaciones, text="Ubicaciones", font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
    
    #Añadir Ubicacion
    parte1 = Frame(pagina_ubicaciones)
    parte1.place(x=10, y=30, width=385, height=460)
    lbl_titulo1 = Label(parte1, text="Crear / Modificar Ubicacion", font=(fuente, 14, "bold"))
    lbl_titulo1.place(relx=0.5, anchor="center", y=30)
    #----------------------------------------------
    lbl_id= Label(parte1, text= "Id")
    lbl_id.place(x=115, y=100)
    ent_id = Entry(parte1)
    ent_id.place(x=115, y=130, width=150)
    ent_id.config(state='readonly')
    #----------------------------------------------
    lbl_nomCalle = Label(parte1, text= "Nombre de la calle")
    lbl_nomCalle.place(x=115, y=170)
    ent_nomCalle = Entry(parte1)
    ent_nomCalle.place(x=115, y=200, width=150)
    ent_nomCalle.config(state="normal")
    #---------------------------------------------
    lbl_altura = Label(parte1, text= "Altura")
    lbl_altura.place(x=115, y=240)
    ent_altura = Entry(parte1)
    ent_altura.place(x=115, y=270, width=75)
    ent_altura.config(state="normal")

    #Mostrar Ubicacion
    parte2 = Frame(pagina_ubicaciones)
    parte2.place(x=405, y=30, width=385, height=460)

    
    lbl_titulo2 = Label(parte2, text="Ubicaciones Existentes", font=(fuente, 14, "bold"))
    lbl_titulo2.place(relx=0.5, anchor="center", y=30)
    
    trv_ubicaciones = ttk.Treeview(parte2, columns=(1, 2), show="headings", height="15")
    trv_ubicaciones.place(x=10,y=100, width=370)

    trv_ubicaciones.heading(1, text="Id")
    trv_ubicaciones.heading(2, text="Direccion")

    trv_ubicaciones.column(1, width=20)

    #---------------------------------------------    
    btn_guardar = Button(parte1, text="Guardar Cambios", command=partial(guardar_ubicacion,ent_id, ent_nomCalle, ent_altura, trv_ubicaciones))
    btn_guardar.place(x=115, y=320, width=150, height=30)

    btn_eliminar = Button(parte1, text="Inhabilitar Ubicacion", command=partial(eliminar_ubicacion,ent_id, ent_nomCalle, ent_altura, trv_ubicaciones))
    btn_eliminar.place(x=115, y=360, width=150, height=30)
    btn_eliminar.config(state="disable")

    btn_habilitar = Button(parte1, text="Habilitar Ubicacion", 
                           command=partial(habilitar_ubicaciones,ent_id, ent_nomCalle,ent_altura,trv_ubicaciones))
    btn_habilitar.place(x=115, y=400, width=150, height=30)
    btn_habilitar.config(state="disable")

    #Mostrar Activos
    btn_mostrarActivos = Button(parte2, text="MOSTRAR HABILITADAS", 
                                command=partial(funcion_mostrarUbicacioneshabilitadas,trv_ubicaciones, 
                                                1, btn_habilitar, btn_guardar, btn_eliminar, ent_nomCalle, ent_id, ent_altura))
    btn_mostrarActivos.place(x=10, y=60, width=175, height=30)

    #Mostrar Inactivos
    btn_mostrarInactivos = Button(parte2, text="MOSTRAR INHABILITADAS", 
                                command=partial(funcion_mostrarUbicacionesInhabilitadas,trv_ubicaciones, 0, btn_habilitar,
                                 btn_guardar, btn_eliminar, ent_nomCalle, ent_id, ent_altura))
    btn_mostrarInactivos.place(x=205, y=60, width=175,height=30)

    mostrar_ubicacionesArbol(trv_ubicaciones, 1)
    trv_ubicaciones.bind('<ButtonRelease-1>', lambda event:tomar_datos_ubicacionesArbol(event, trv_ubicaciones, ent_id, ent_nomCalle,ent_altura,btn_eliminar, btn_habilitar))
    app_MenuOrg.bind("<Button-1>", lambda event: deseleccionarUbicaciones(event, trv_ubicaciones, ent_id, ent_nomCalle, ent_altura, btn_guardar, btn_eliminar, btn_habilitar))
#MOSTRAR TREEVIEW CATEGORIAS-----------------------------
def mostrar_ubicacionesArbol(arbol_ubicaciones, activo):
    funciones_generales.limpiar_treeview(arbol_ubicaciones)
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        
        consulta = "SELECT COUNT(*) FROM Ubicacion WHERE activo = %s ORDER BY id_ubicacion ASC"
        cursor.execute(consulta, (activo, ))
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            arbol_ubicaciones.insert("","end", values=("-","Ninguna categoría por ahora"))
        else:
            consulta = "SELECT id_ubicacion, direccion FROM Ubicacion WHERE activo = %s ORDER BY id_ubicacion ASC"
            cursor.execute(consulta,(activo, ))
            resultado = cursor.fetchall()

            arbol_ubicaciones.delete(*arbol_ubicaciones.get_children())

            for fila in resultado:
                arbol_ubicaciones.insert("", "end", values=fila)

    except Exception as e:
        messagebox.showerror(title="Error de Conexión", message="¡Ups! Hubo un error al conectar con la Base de Datos")
        print("Error al mostrar categorías:", e)
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass
#TOMAR DATOS TREEVIEW------------------------------------
def tomar_datos_ubicacionesArbol(event, trv_ubicaciones, ent_id, ent_nomCalle,ent_altura, btn_eliminar, btn_habilitar):
    if(btn_habilitar.cget("state") == "normal"):
        btn_eliminar.config(state="disable")
    else:
        btn_eliminar.config(state="normal")

    ent_id.config(state='normal')
    ent_id.delete(0, END)

    if(ent_nomCalle.cget("state") == "readonly"):
        ent_nomCalle.config(state="normal")
        ent_altura.config(state="normal")

        ent_nomCalle.delete(0, END)
        ent_altura.delete(0, END)

        ent_nomCalle.config(state="readonly")
        ent_altura.config(state="readonly")
    else:
        ent_nomCalle.delete(0, END)
        ent_altura.delete(0, END)

    fila = trv_ubicaciones.focus()
    valores= trv_ubicaciones.item(fila, 'values')

    if valores:    
        ent_id.insert(0,valores[0])
        aux = valores[1].split(" ")
        if(ent_nomCalle.cget("state") == "readonly"):
            
            ent_nomCalle.config(state='normal')
            ent_altura.config(state='normal')

            ent_nomCalle.insert(0,aux[:-1])
            ent_altura.insert(0,aux[-1])

            ent_nomCalle.config(state="readonly")
            ent_altura.config(state="readonly")

        ent_nomCalle.insert(0,aux[:-1])
        ent_altura.insert(0,aux[-1])

        ent_id.config(state="readonly")
#GUARDAR UBICACION---------------------------------------
def guardar_ubicacion(ent_id, ent_nomCalle, ent_altura, arbol_ubicaciones):
    #DAR  DE ALTA
    if(len(ent_nomCalle.get()) > 0 and len(ent_altura.get())):
        
        calle = ent_nomCalle.get()
        altura = ent_altura.get()
        direccion = calle + " " + altura 
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta = "SELECT COUNT(*) FROM Ubicacion WHERE direccion = %s"
            cursor.execute(consulta, (direccion,))
            resultado = cursor.fetchone()[0]
            if(resultado > 0):
                messagebox.showerror(title="Error", message="Esta direccion ya está registrada.")
            else:
                if(len(ent_id.get()) > 0):
                    id= ent_id.get()

                    consulta= "UPDATE Ubicacion SET direccion = %s WHERE id_ubicacion = %s"
                    valores = (direccion, id)
                    cursor.execute(consulta, valores)
                    conexion.commit()
                    messagebox.showinfo(title="Éxito", message="¡Ubicacion Actualizada Correctamente!")
                    ent_id.config(state="normal")
                    ent_id.delete(0,END)
                    ent_id.config(state="readonly")
                    ent_nomCalle.delete(0,END)
                    ent_altura.delete(0,END)
                    mostrar_ubicacionesArbol(arbol_ubicaciones, 1)
                else:
                    consulta = "INSERT INTO Ubicacion (direccion,activo) VALUES (%s,1)"
                    cursor.execute(consulta, (direccion, ))
                    conexion.commit()
                    messagebox.showinfo(title="Éxito", message="¡Ubicacion Registrada Correctamente!")
                    ent_nomCalle.delete(0,END)
                    ent_altura.delete(0,END)
                    mostrar_ubicacionesArbol(arbol_ubicaciones, 1)
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
        finally:
            try:
                cursor.close()
                conexion.close()
            except:
                pass
    else:
        ent_nomCalle.delete(0,END)
        ent_nomCalle.focus()
        messagebox.showerror(title="Campos vacios", message="Por favor llene los campos")
#ELIMINAR UBICACION--------------------------------------
def eliminar_ubicacion(ent_id, ent_nomCalle, ent_altura, arbol_ubicacion):
    ent_nomCalle.config(state="normal")
    if(len(ent_id.get()) > 0 and len(ent_nomCalle.get()) > 0):
        id = ent_id.get()
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta = "UPDATE Ubicacion SET activo = 0 WHERE id_ubicacion = %s"
            cursor.execute(consulta,(id, ))
            conexion.commit()
            messagebox.showinfo(title="Éxito", message="¡Ubicacion Eliminada Correctamente!")
            ent_id.config(state="normal")
            ent_id.delete(0,END)
            ent_id.config(state="readonly")

            ent_nomCalle.delete(0,END)
            ent_altura.delete(0,END)
            arbol_ubicacion.selection_remove(arbol_ubicacion.selection())
            funciones_generales.limpiar_treeview(arbol_ubicacion)
            mostrar_ubicacionesArbol(arbol_ubicacion, 1)
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
        finally: 
            try:
                cursor.close()
                conexion.close()
            except:
                pass
#DESELECCIONAR FILA--------------------------------------
def deseleccionarUbicaciones(event, trv_ubicaciones, ent_id, ent_nomCalle, ent_altura, btn_guardar, btn_eliminar, btn_habilitar):
    widget = event.widget
    if widget not in (trv_ubicaciones,ent_id, ent_nomCalle, ent_altura,btn_guardar, btn_eliminar, btn_habilitar):
        trv_ubicaciones.selection_remove(trv_ubicaciones.selection())
        ent_id.config(state='normal')

        if(ent_nomCalle.cget("state")=="readonly"):
            ent_nomCalle.config(state='normal')
            ent_nomCalle.delete(0,END)

            ent_altura.config(state='normal')
            ent_altura.delete(0,END)

            ent_nomCalle.config(state='readonly')
            ent_altura.config(state='readonly')
        else:
            ent_nomCalle.delete(0,END)
            ent_altura.delete(0,END)

        ent_id.delete(0,END)
        ent_id.config(state="readonly")

        btn_eliminar.config(state="disable")
#MOSTRAR UBICACIONES INHABILITADAS------------------------
def funcion_mostrarUbicacionesInhabilitadas(trv_ubicaciones, activo, btn_habilitar, btn_guardar, btn_eliminar, ent_nom, ent_id, ent_altura):
    ent_id.config(state='normal')
    ent_id.delete(0, END)
    if(ent_nom.cget("state")=="readonly"):
        ent_nom.config(state="normal")
        ent_nom.delete(0, END)
        ent_altura.config(state="normal")
        ent_altura.delete(0, END)
    else:
        ent_nom.delete(0, END)
        ent_altura.delete(0, END)

    ent_nom.delete(0, END)
    ent_altura.delete(0, END)
    ent_id.config(state="readonly")
    
    btn_eliminar.config(state="disable")
    mostrar_ubicacionesArbol(trv_ubicaciones, activo)
    btn_habilitar.config(state="normal")
    btn_eliminar.config(state="disable")
    btn_guardar.config(state="disable")
    ent_nom.config(state="readonly")
    ent_altura.config(state="readonly")
#MOSTRAR UBICACIONES HABILITADAS--------------------------
def funcion_mostrarUbicacioneshabilitadas(trv_ubicaciones, activo, btn_habilitar, btn_guardar, btn_eliminar, ent_nom, ent_id, ent_altura):
    ent_id.config(state='normal')
    ent_id.delete(0, END)
    if(ent_nom.cget("state")=="readonly"):
        ent_nom.config(state="normal")
        ent_nom.delete(0, END)
        ent_altura.config(state="normal")
        ent_altura.delete(0, END)
    else:
        ent_nom.delete(0, END)
        ent_altura.delete(0, END)

    ent_id.config(state="readonly")

    mostrar_ubicacionesArbol(trv_ubicaciones, activo)
    btn_habilitar.config(state="disable")
    btn_eliminar.config(state="normal")
    btn_guardar.config(state="normal")
    ent_nom.config(state="normal")
    ent_altura.config(state="normal")
#HABILITAR NUEVAMENTE UBICACIONES-------------------------
def habilitar_ubicaciones(ent_id, ent_nom,ent_altura,arbol_ubicaciones):
    if(len(ent_id.get()) > 0):
        id = ent_id.get()
        
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta = "UPDATE Ubicacion SET activo = 1 WHERE id_ubicacion = %s"
            cursor.execute(consulta,(id, ))
            conexion.commit()
            messagebox.showinfo(title="Éxito", message="¡Categoria Habilitada Correctamente!")
            ent_id.config(state="normal")
            ent_id.delete(0,END)
            ent_id.config(state="readonly")

            ent_nom.config(state="normal")
            ent_nom.delete(0,END)
            ent_nom.config(state="readonly")

            ent_altura.config(state="normal")
            ent_altura.delete(0,END)
            ent_altura.config(state="readonly")


            arbol_ubicaciones.selection_remove(arbol_ubicaciones.selection())
            funciones_generales.limpiar_treeview(arbol_ubicaciones)
            mostrar_ubicacionesArbol(arbol_ubicaciones, 0)
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
        finally: 
            try:
                cursor.close()
                conexion.close()
            except:
                pass
    else:
        ent_nom.delete(0,END)
        ent_altura.delete(0,END)
        ent_nom.focus()
        messagebox.showerror(title="Campos vacios", message="Por favor llene los campos")
#
# 
# 
#PAGINA CATEGORIAS---------------------------------------
def mostrar_pagina_categorias(vector_paginas, app_MenuOrg, botones, btn_seleccionado):
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)
    
    pagina_categoria = vector_paginas[3]
    pagina_categoria.place(x=200, width=800, height=500)
    funciones_generales.ocultar_pagina(vector_paginas, pagina_categoria)

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
    ent_nom.config(state="normal")
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

    mostrar_categoriasArbol(trv_categorias, 1)

    #----------------------------------------------
    btn_guardar = Button(parte1, text="Guardar Cambios", command=partial(guardar_categorias,ent_id,ent_nom, trv_categorias, vector_paginas))
    btn_guardar.place(relx=0.5, anchor="center", y=260, width=150, height=30)

    btn_eliminar = Button(parte1, text="Inhabilitar Categoria", command=partial(eliminar_categoria,ent_id, ent_nom, trv_categorias))
    btn_eliminar.place(relx=0.5, anchor="center", y=320, width=150, height=30)
    btn_eliminar.config(state="disable")

    btn_habilitar = Button(parte1, text="Habilitar Categoria", command=partial(habilitar_categoria,ent_id, ent_nom, trv_categorias))
    btn_habilitar.place(relx=0.5, anchor="center", y=380, width=150, height=30)
    btn_habilitar.config(state="disable")

    #Mostrar Activos
    btn_mostrarActivos = Button(parte2, text="MOSTRAR HABILITADAS", command=partial(funcion_mostrarhabilitadas,trv_categorias, 1, btn_habilitar, btn_guardar, btn_eliminar, ent_nom, ent_id))
    btn_mostrarActivos.place(x=10, y=60, width=175, height=30)

    #Mostrar Inactivos
    btn_mostrarActivos = Button(parte2, text="MOSTRAR INHABILITADAS", command=partial(funcion_mostrarInhabilitadas,trv_categorias, 0, btn_habilitar, btn_guardar, btn_eliminar, ent_nom, ent_id))
    btn_mostrarActivos.place(x=205, y=60, width=175,height=30)

    trv_categorias.bind('<ButtonRelease-1>', lambda event:tomar_datos_categoriasArbol(event, trv_categorias, ent_id, ent_nom, btn_eliminar,btn_guardar, btn_habilitar))
    app_MenuOrg.bind_all("<Button-1>", lambda event:deseleccionarCategorias(event, trv_categorias, ent_id, ent_nom, btn_guardar, btn_eliminar, btn_habilitar))
#GUARDAR CATEGORIA---------------------------------------
def guardar_categorias(ent_id, ent_nom, arbol_categorias, vector_paginas):
    #DAR  DE ALTA
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
                if(len(ent_id.get()) > 0):
                    id= ent_id.get()

                    consulta= "UPDATE Categoria SET nombre = %s WHERE id_categoria = %s"
                    valores = (nombre, id)
                    cursor.execute(consulta, valores)
                    conexion.commit()
                    messagebox.showinfo(title="Éxito", message="¡Categoria Actualizada Correctamente!")
                    ent_id.config(state="normal")
                    ent_id.delete(0,END)
                    ent_id.config(state="readonly")
                    ent_nom.delete(0,END)
                    mostrar_categoriasArbol(arbol_categorias, 1)
                else:
                    consulta = "INSERT INTO Categoria (nombre, activo) VALUES (%s, 1)"
                    cursor.execute(consulta, (nombre, ))
                    conexion.commit()
                    messagebox.showinfo(title="Éxito", message="¡Categoria Registrada Correctamente!")
                    ent_nom.delete(0,END)
                    mostrar_categoriasArbol(arbol_categorias, 1)
                
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
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
#ELIMINAR CATEGORIA--------------------------------------
def eliminar_categoria(ent_id, ent_nom, arbol_categorias):
    ent_nom.config(state="normal")
    if(len(ent_id.get()) > 0 and len(ent_nom.get()) > 0):
        id = ent_id.get()
        nom = ent_nom.get()
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta = "UPDATE Categoria SET activo = 0 WHERE id_categoria = %s"
            cursor.execute(consulta,(id, ))
            conexion.commit()
            messagebox.showinfo(title="Éxito", message="¡Categoria Inhabilitada Correctamente!")
            ent_id.config(state="normal")
            ent_id.delete(0,END)
            ent_id.config(state="readonly")
            ent_nom.delete(0,END)
            arbol_categorias.selection_remove(arbol_categorias.selection())
            funciones_generales.limpiar_treeview(arbol_categorias)
            mostrar_categoriasArbol(arbol_categorias, 1)
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
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
#MOSTRAR TREEVIEW CATEGORIAS-----------------------------
def mostrar_categoriasArbol(arbol_categorias, activo):
    funciones_generales.limpiar_treeview(arbol_categorias)
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        
        consulta = "SELECT COUNT(*) FROM Categoria WHERE activo = %s ORDER BY id_categoria ASC"
        cursor.execute(consulta, (activo, ))
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            arbol_categorias.insert("","end", values=("-","Ninguna categoría por ahora"))
        else:
            consulta = "SELECT id_categoria, nombre FROM Categoria WHERE activo = %s ORDER BY id_categoria ASC"
            cursor.execute(consulta,(activo, ))
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
#TOMAR DATOS TREEVIEW------------------------------------
def tomar_datos_categoriasArbol(event,trv_categorias, ent_id, ent_nom,btn_eliminar, btn_guardar, btn_habilitar):
    if(btn_habilitar.cget("state") == "normal"):
        btn_eliminar.config(state="disable")
    else:
        btn_eliminar.config(state="normal")

    ent_id.config(state='normal')
    ent_id.delete(0,END)
    if(ent_nom.cget("state") == "readonly"):
        ent_nom.config(state="normal")
        ent_nom.delete(0, END)
        ent_nom.config(state="readonly")
    else:
        ent_nom.delete(0, END)
    

    fila = trv_categorias.focus()
    valores= trv_categorias.item(fila, 'values')

    if valores:    
        ent_id.insert(0,valores[0])
        if(ent_nom.cget("state") == "readonly"):
            ent_nom.config(state="normal")
            ent_nom.insert(0,valores[1])
            ent_nom.config(state="readonly")
        ent_nom.insert(0,valores[1])
        ent_id.config(state="readonly")
#DESELECCIONAR FILA--------------------------------------
def deseleccionarCategorias(event, trv_categorias, ent_id, ent_nom, btn_guardar, btn_eliminar, btn_habilitar):
    widget = event.widget

    if widget not in (trv_categorias,ent_id, ent_nom, btn_guardar, btn_eliminar, btn_habilitar):
        trv_categorias.selection_remove(trv_categorias.selection())

        ent_id.config(state='normal')
        if(ent_nom.cget("state")=="readonly"):
            ent_nom.config(state='normal')
            ent_nom.delete(0, END)
            ent_nom.config(state='readonly')
        else:
            ent_nom.delete(0, END)
        ent_id.delete(0, END)
        ent_id.config(state="readonly")
        
        btn_eliminar.config(state="disable")
#MOSTRAR CATEGORIAS INHABILITADAS------------------------
def funcion_mostrarInhabilitadas(trv_categorias, activo, btn_habilitar, btn_guardar, btn_eliminar, ent_nom, ent_id):
    ent_id.config(state='normal')
    ent_id.delete(0, END)
    if(ent_nom.cget("state")=="readonly"):
        ent_nom.config(state="normal")
        ent_nom.delete(0, END)
    else:
        ent_nom.delete(0, END)
    ent_nom.delete(0, END)
    ent_id.config(state="readonly")
    
    btn_eliminar.config(state="disable")
    mostrar_categoriasArbol(trv_categorias, activo)
    btn_habilitar.config(state="normal")
    btn_eliminar.config(state="disable")
    btn_guardar.config(state="disable")
    ent_nom.config(state="readonly")
#MOSTRAR CATEGORIAS HABILITADAS--------------------------
def funcion_mostrarhabilitadas(trv_categorias, activo, btn_habilitar, btn_guardar, btn_eliminar, ent_nom, ent_id):
    ent_id.config(state='normal')
    ent_id.delete(0, END)
    if(ent_nom.cget("state")=="readonly"):
        ent_nom.config(state="normal")
        ent_nom.delete(0, END)
    else:
        ent_nom.delete(0, END)
    ent_id.config(state="readonly")

    mostrar_categoriasArbol(trv_categorias, activo)
    btn_habilitar.config(state="disable")
    btn_eliminar.config(state="normal")
    btn_guardar.config(state="normal")
    ent_nom.config(state="normal")
#HABILITAR NUEVAMENTE CATEGORIAS-------------------------
def habilitar_categoria(ent_id, ent_nom, arbol_categorias):
    if(len(ent_id.get()) > 0):
        id = ent_id.get()
        nom = ent_nom.get()
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()

            consulta = "UPDATE Categoria SET activo = 1 WHERE id_categoria = %s"
            cursor.execute(consulta,(id, ))
            conexion.commit()
            messagebox.showinfo(title="Éxito", message="¡Categoria Habilitada Correctamente!")
            ent_id.config(state="normal")
            ent_id.delete(0,END)
            ent_id.config(state="readonly")
            ent_nom.config(state="normal")
            ent_nom.delete(0,END)
            ent_nom.config(state="readonly")
            arbol_categorias.selection_remove(arbol_categorias.selection())
            funciones_generales.limpiar_treeview(arbol_categorias)
            mostrar_categoriasArbol(arbol_categorias, 0)
        except Exception as e:
            messagebox.showerror(title="Error de Conexion", message="¡Ups! Hubo un Error al conectar con la Base de Datos")
            print (e)
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
#
# 
# 
#FUNCION PRINCIPAL=====================================================================================
def creacionPantalla_MenuOrganizador2(app, _fuente, nombreUsuario, id_organizador):
    global fuente
    fuente = _fuente
    app_MenuOrg = Toplevel(app)
    app_MenuOrg.title("Sesion Organizador")
    funciones_generales.centrarPantalla(1000, 500, app_MenuOrg)
    #PANEL 1 (izquierda, el mas angosto)
    panel1 = Frame(app_MenuOrg, bg="gray")
    panel1.place(x=0, width=200, height=500)
    #PANEL 2 (derecha, el mas ancho)
    panel2 = Frame(app_MenuOrg, bg="gainsboro")
    panel2.place(x=200, width=800, height=500)
    #COMPONENTES PARA EL PANEL 1--------------------
    lbl1 = Label(panel2, text=("¡Bienvenido/a " + nombreUsuario + "!"), font=(fuente, 16, "bold"), background= "gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)
    #PAGINA CUENTA
    pagina_cuenta = Frame(app_MenuOrg, background="gainsboro")
    #PAGINA EVENTO
    pagina_evento = Frame(app_MenuOrg, background="gainsboro")
    #PAGINA EVENTO EN CASO DE QUE NO HAYA CATEGORIA Y/O UBICACIONES
    pagina_eventoMala = Frame(app_MenuOrg, bg="gainsboro")
    #PAGINA CATEGORIAS
    pagina_categoria = Frame(app_MenuOrg, background="gainsboro")
    #PAGINA UBICACIONES
    pagina_ubicaciones = Frame(app_MenuOrg, background="gainsboro")
    #PAGINA ENTRADAS
    pagina_entradas = Frame(app_MenuOrg,background="gainsboro")
    #PAGINA NOTIFICACIONES
    pagina_notificaciones = Frame(app_MenuOrg,background="gainsboro")
    #PAGINA DE CARGA
    pagina_carga = Frame(app_MenuOrg, background="gainsboro")
    lbl = Label(pagina_carga, text="CARGANDO.....", font=(fuente, 20, "bold"))
    lbl.place(relx=0.5, rely=0.5, anchor="center")
    #VECTOR CON TODOS LAS PAGINAS
    vector_paginas = [panel2, 
                      pagina_cuenta, 
                      pagina_evento, 
                      pagina_categoria, 
                      pagina_ubicaciones, 
                      pagina_eventoMala, 
                      pagina_entradas, 
                      pagina_notificaciones,
                      pagina_carga]
    for i in range(len(vector_paginas)):
        if vector_paginas[i] != panel2:
            vector_paginas[i].place_forget()
    #COMPONENTES PARA EL PANEL 2--------------------
    #BOTON VOLVER
    btn_volver = Button(app_MenuOrg, text="🡸", command=partial(funciones_generales.cerrar_abrirVentanas, app_MenuOrg, app))
    btn_volver.place(x=10, y=10)
    #BOTON MENU PRINCIPAL
    botones = []
    btn_principal = Button(app_MenuOrg, text="MENU PRINCIPAL", relief="flat")
    botones.append(btn_principal)
    btn_principal.place(x=20, y=70, width=160, height=30)
    #BOTON GESTIONAR CUENTA (FUNCION ELIMINADA PERO LO DEJO PARA NO AFECTAR AL VECTOR DE BOTONES)
    btn_cuenta = Button(app_MenuOrg, text="CUENTA", relief="flat" )
    botones.append(btn_cuenta)
    #BOTON GESTIONAR CATEGORIAS
    btn_categorias = Button(app_MenuOrg, text="CATEGORIAS", relief="flat" )
    botones.append(btn_categorias)
    btn_categorias.place(x=20, y=100, width=160, height=30)
    #BOTON GESTIONAR UBICACIONES
    btn_ubicaciones = Button(app_MenuOrg, text="UBICACIONES", relief="flat" )
    botones.append(btn_ubicaciones)
    btn_ubicaciones.place(x=20, y=130, width=160, height=30)
    #BOTON GESTIONAR EVENTO
    btn_evento = Button(app_MenuOrg, text="EVENTOS", relief="flat")
    botones.append(btn_evento)
    btn_evento.place(x=20, y=160, width=160, height=30)
    #BOTON GESTIONAR ENTRADAS 
    btn_entradas = Button(app_MenuOrg, text="ENTRADAS", relief="flat")
    botones.append(btn_entradas)
    btn_entradas.place(x=20, y=190, width=160, height=30)
    #BOTON GESTIONAR NOTIFICACIONES 
    btn_notificaciones = Button(app_MenuOrg, text="NOTIFICACIONES", relief="flat")
    botones.append(btn_notificaciones)
    btn_notificaciones.place(x=20, y=220, width=160, height=30)
    #SE ASIGNAS LAS FUNCIONES A LOS BOTONES YA CREADOS
    btn_principal.config(command=partial(mostrar_pagina_menuPrincipal,vector_paginas, app_MenuOrg, botones, 0, id_organizador))
    btn_categorias.config(command=partial(mostrar_pagina_categorias, vector_paginas, app_MenuOrg, botones, 2))
    btn_ubicaciones.config(command=partial(mostrar_pagina_ubicaciones, vector_paginas, app_MenuOrg, botones, 3))
    btn_evento.config(command=partial(eleccion_paginaEvento,vector_paginas, app_MenuOrg, botones, 4, id_organizador))
    btn_entradas.config(command=partial(mostrar_pagina_entradas,vector_paginas, app_MenuOrg, botones, 5, id_organizador, fuente))
    btn_notificaciones.config(command=partial(panel_administrador_Notificaciones.mostrar_pagina_notificaciones,vector_paginas, app_MenuOrg, botones, 6, fuente, id_organizador))
    btn_principal.config(bg="gainsboro")

    mostrar_pagina_menuPrincipal(vector_paginas, app_MenuOrg, botones, 0, id_organizador)
    funciones_generales.actualizar_estados_eventos(vectorConexion)


