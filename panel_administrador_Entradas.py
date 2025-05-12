'''
from librerias import * 
import librerias as lib
import funciones_generales
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import BooleanVar, Checkbutton

vectorConexion = ["boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com","u1s6xofortb1nhmx","TIjcUe5NAXwsr8Rtu8U8","boznowy5qzijb8uhhqoj"]
COLOR_NORMAL = "#f0f0f0"
COLOR_ACTIVO = "gainsboro"

def ocultar_pagina(vector_paginas, paginaMostrar):
    for pagina in vector_paginas:
        if pagina != paginaMostrar:
            pagina.place_forget()

global fuente

def mostrar_pagina_entradas(vector_paginas, app_MenuOrg, botones, btn_seleccionado, id_organizador, fuente):
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)

    pagina_entradas = vector_paginas[6]
    pagina_entradas.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_entradas)

    # Parte izquierda: Crear entrada
    parte1 = Frame(pagina_entradas)
    parte1.place(x=10, y=30, width=385, height=460)

    lbl_titulo = Label(parte1, text="Crear / Modificar Entrada", font=(fuente, 14, "bold"), bg="gainsboro")
    lbl_titulo.place(relx=0.5, anchor="center", y=30)

    lbl_evento = Label(parte1, text="Evento:")
    lbl_evento.place(x=30, y=60)
    combo_eventos = ttk.Combobox(parte1, state="readonly")
    combo_eventos.place(x=30, y=80, width=200)

    lbl_tipo = Label(parte1, text="Tipo de entrada:")
    lbl_tipo.place(x=30, y=110)
    ent_tipo = Entry(parte1)
    ent_tipo.place(x=30, y=130, width=150)

    lbl_precio = Label(parte1, text="Precio:")
    lbl_precio.place(x=30, y=160)
    ent_precio = Entry(parte1)
    ent_precio.place(x=30, y=180, width=150)

    var_asiento = BooleanVar()
    check_asiento = Checkbutton(parte1, text="Tiene asiento", variable=var_asiento, bg="gainsboro", command=lambda: toggle_asientos())
    check_asiento.place(x=30, y=210)

    lbl_cupo = Label(parte1, text="Cupo total:", font=(fuente, 10, "bold"), bg="gainsboro")
    lbl_cupo.place(x=30, y=240)
    ent_cupo = Entry(parte1)
    ent_cupo.place(x=30, y=260, width=150)

    lbl_filas = Label(parte1, text="Filas:", font=(fuente, 10, "bold"), bg="gainsboro")
    ent_filas = Entry(parte1)
    lbl_columnas = Label(parte1, text="Columnas:", font=(fuente, 10, "bold"), bg="gainsboro")
    ent_columnas = Entry(parte1)
    
    def toggle_asientos():
        if var_asiento.get():
            lbl_filas.place(x=30, y=240)
            ent_filas.place(x=30, y=260, width=70)
            lbl_columnas.place(x=110, y=240)
            ent_columnas.place(x=110, y=260, width=70)
            lbl_cupo.place_forget()
            ent_cupo.place_forget()
        else:
            lbl_cupo.place(x=30, y=240)
            ent_cupo.place(x=30, y=260, width=150)
            lbl_filas.place_forget()
            ent_filas.place_forget()
            lbl_columnas.place_forget()
            ent_columnas.place_forget()

    eventos_dict = {}

    def cargar_eventos_combo():
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()
            consulta = "SELECT id_evento, titulo FROM Evento WHERE id_organizador = %s AND estado = 'activo'"
            cursor.execute(consulta, (id_organizador,))
            resultado = cursor.fetchall()
            titulos = []
            for id_evento, titulo in resultado:
                titulos.append(titulo)
                eventos_dict[titulo] = id_evento
            combo_eventos['values'] = titulos
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar eventos: {e}")
        finally:
            try:
                cursor.close()
                conexion.close()
            except:
                pass

    cargar_eventos_combo()

    btn_guardar = Button(parte1, text="Guardar Entrada", 
        command=lambda: guardar_entrada(eventos_dict, combo_eventos, ent_tipo, ent_precio,
                                        ent_cupo, tree_entradas, var_asiento, ent_filas, ent_columnas))
    btn_guardar.place(x=100, y=300, width=150, height=30)

    # Parte derecha: Listado de entradas
    parte2 = Frame(pagina_entradas)
    parte2.place(x=405, y=30, width=385, height=460)

    lbl_titulo2 = Label(parte2, text="Entradas Existentes", font=(fuente, 14, "bold"))
    lbl_titulo2.place(relx=0.5, anchor="center", y=30)

    tree_entradas = ttk.Treeview(parte2, columns=("tipo", "precio", "cupo", "asiento"), show="headings", height=15)
    tree_entradas.place(x=10, y=100, width=370)
    tree_entradas.heading("tipo", text="Tipo")
    tree_entradas.heading("precio", text="Precio")
    tree_entradas.heading("cupo", text="Cupo total")
    tree_entradas.heading("asiento", text="Asientos")
    

    def actualizar_treeview(*args):
        titulo_sel = combo_eventos.get()
        if titulo_sel and titulo_sel in eventos_dict:
            cargar_entradas_en_treeview(eventos_dict[titulo_sel], tree_entradas)
        else:
            cargar_todas_entradas(id_organizador, tree_entradas)

def cargar_entradas_en_treeview(evento_id, tree):
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        consulta = "SELECT tipo, precio, cupo_total, asiento FROM Entrada WHERE Evento_id = %s"
        cursor.execute(consulta, (evento_id,))
        resultados = cursor.fetchall()

        tree.delete(*tree.get_children())
        for tipo, precio, cupo, asiento in resultados:
            tree.insert("", "end", values=(tipo, precio, cupo, "✔️" if asiento else "❌"))

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar entradas: {e}")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass


def guardar_entrada(eventos_dict, combo_eventos, ent_tipo, ent_precio, ent_cupo,
                    tree_entradas, var_asiento, ent_filas, ent_columnas):
    tipo = ent_tipo.get()
    precio = ent_precio.get()
    titulo = combo_eventos.get()
    asiento = var_asiento.get()

    if not (tipo and precio and titulo):
        messagebox.showwarning("Campos vacíos", "Completa todos los campos obligatorios.")
        return

    try:
        precio = float(precio)
        evento_id = eventos_dict[titulo]

        if asiento:
            filas = int(ent_filas.get())
            columnas = int(ent_columnas.get())
            cupo_total = filas * columnas
        else:
            cupo_total = int(ent_cupo.get())
            filas = columnas = None

        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = """INSERT INTO Entrada (Evento_id, tipo, precio, cupo_total, cupo_disponible, asiento)
                      VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(consulta, (evento_id, tipo, precio, cupo_total, cupo_total, asiento))
        conexion.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        id_entrada = cursor.fetchone()[0]

        if asiento:
            for f in range(1, filas + 1):
                for c in range(1, columnas + 1):
                    cursor.execute("""INSERT INTO Asiento (fila, columna, disponible, Entrada_id)
                                      VALUES (%s, %s, %s, %s)""",
                                   (f, c, True, id_entrada))
            conexion.commit()

        messagebox.showinfo("Éxito", "¡Entrada registrada correctamente!")
        ent_tipo.delete(0, END)
        ent_precio.delete(0, END)
        ent_cupo.delete(0, END)
        ent_filas.delete(0, END)
        ent_columnas.delete(0, END)

        cargar_entradas_en_treeview(evento_id, tree_entradas)

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar entrada: {e}")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass


def cargar_todas_entradas(id_organizador, tree):
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = """
            SELECT Entrada.tipo, Entrada.precio, Entrada.cupo_total, Entrada.asiento
            FROM Entrada
            JOIN Evento ON Entrada.Evento_id = Evento.id_evento
            WHERE Evento.id_organizador = %s
        """
        cursor.execute(consulta, (id_organizador,))
        resultados = cursor.fetchall()

        tree.delete(*tree.get_children())
        for tipo, precio, cupo, asiento in resultados:
            tree.insert("", "end", values=(tipo, precio, cupo, "✔️" if asiento else "❌"))

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar entradas: {e}")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass
'''



from librerias import * 
import librerias as lib
import funciones_generales
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import BooleanVar, Checkbutton

vectorConexion = [
    "boznowy5qzijb8uhhqoj-mysql.services.clever-cloud.com",
    "u1s6xofortb1nhmx",
    "TIjcUe5NAXwsr8Rtu8U8",
    "boznowy5qzijb8uhhqoj"
]
COLOR_NORMAL = "#f0f0f0"
COLOR_ACTIVO = "gainsboro"

def ocultar_pagina(vector_paginas, paginaMostrar):
    for pagina in vector_paginas:
        if pagina != paginaMostrar:
            pagina.place_forget()

global fuente

def mostrar_pagina_entradas(vector_paginas, app_MenuOrg, botones, btn_seleccionado, id_organizador, fuente):
    funciones_generales.click_boton(btn_seleccionado, botones, COLOR_NORMAL, COLOR_ACTIVO)

    pagina_entradas = vector_paginas[6]
    pagina_entradas.place(x=200, width=800, height=500)
    ocultar_pagina(vector_paginas, pagina_entradas)

    # Parte izquierda: Crear entrada
    parte1 = Frame(pagina_entradas)
    parte1.place(x=10, y=30, width=385, height=460)

    lbl_titulo = Label(parte1, text="Crear / Modificar Entrada", font=(fuente, 14, "bold"), bg="gainsboro")
    lbl_titulo.place(relx=0.5, anchor="center", y=30)

    lbl_evento = Label(parte1, text="Evento:")
    lbl_evento.place(x=30, y=60)
    combo_eventos = ttk.Combobox(parte1, state="readonly")
    combo_eventos.place(x=30, y=80, width=200)

    lbl_tipo = Label(parte1, text="Tipo de entrada:")
    lbl_tipo.place(x=30, y=110)
    ent_tipo = Entry(parte1)
    ent_tipo.place(x=30, y=130, width=150)

    lbl_precio = Label(parte1, text="Precio:")
    lbl_precio.place(x=30, y=160)
    ent_precio = Entry(parte1)
    ent_precio.place(x=30, y=180, width=150)

    var_asiento = BooleanVar()
    check_asiento = Checkbutton(parte1, text="Tiene asiento", variable=var_asiento, bg="gainsboro", command=lambda: toggle_asientos())
    check_asiento.place(x=30, y=210)

    lbl_cupo = Label(parte1, text="Cupo total:", font=(fuente, 10, "bold"), bg="gainsboro")
    lbl_cupo.place(x=30, y=240)
    ent_cupo = Entry(parte1)
    ent_cupo.place(x=30, y=260, width=150)

    lbl_filas = Label(parte1, text="Filas:", font=(fuente, 10, "bold"), bg="gainsboro")
    ent_filas = Entry(parte1)
    lbl_columnas = Label(parte1, text="Columnas:", font=(fuente, 10, "bold"), bg="gainsboro")
    ent_columnas = Entry(parte1)
    

    def toggle_asientos():
        if var_asiento.get():
            lbl_filas.place(x=30, y=240)
            ent_filas.place(x=30, y=260, width=70)
            lbl_columnas.place(x=110, y=240)
            ent_columnas.place(x=110, y=260, width=70)
            lbl_cupo.place_forget()
            ent_cupo.place_forget()
        else:
            lbl_cupo.place(x=30, y=240)
            ent_cupo.place(x=30, y=260, width=150)
            lbl_filas.place_forget()
            ent_filas.place_forget()
            lbl_columnas.place_forget()
            ent_columnas.place_forget()

    eventos_dict = {}

    def cargar_eventos_combo():
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()
            consulta = "SELECT id_evento, titulo FROM Evento WHERE id_organizador = %s AND estado = 'activo'"
            cursor.execute(consulta, (id_organizador,))
            resultado = cursor.fetchall()
            titulos = []
            for id_evento, titulo in resultado:
                titulos.append(titulo)
                eventos_dict[titulo] = id_evento
            combo_eventos['values'] = titulos
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar eventos: {e}")
        finally:
            try:
                cursor.close()
                conexion.close()
            except:
                pass

    cargar_eventos_combo()
    
    def actualizar_treeview(*args):
        titulo_sel = combo_eventos.get()
        if titulo_sel and titulo_sel in eventos_dict:
            cargar_entradas_en_treeview(eventos_dict[titulo_sel], tree_entradas)
        else:
            cargar_todas_entradas(id_organizador, tree_entradas)
    btn_guardar = Button(parte1, text="Guardar Entrada", 
        command=lambda: guardar_entrada(eventos_dict, combo_eventos, ent_tipo, ent_precio,
                                        ent_cupo, tree_entradas, var_asiento, ent_filas, ent_columnas))
    btn_guardar.place(x=100, y=300, width=150, height=30)
    combo_eventos.bind("<<ComboboxSelected>>", actualizar_treeview)

    # Parte derecha: Listado de entradas
    parte2 = Frame(pagina_entradas)
    parte2.place(x=405, y=30, width=385, height=460)

    lbl_titulo2 = Label(parte2, text="Entradas Existentes", font=(fuente, 14, "bold"))
    lbl_titulo2.place(relx=0.5, anchor="center", y=30)

    tree_entradas = ttk.Treeview(parte2, columns=("tipo", "precio", "cupo", "asiento"), show="headings", height=15)
    tree_entradas.place(x=10, y=100, width=370)
    tree_entradas.heading("tipo", text="Tipo")
    tree_entradas.heading("precio", text="Precio")
    tree_entradas.heading("cupo", text="Cupo total")
    tree_entradas.heading("asiento", text="Asientos")

    cargar_todas_entradas(id_organizador, tree_entradas)

    combo_eventos.bind("<<ComboboxSelected>>", actualizar_treeview)

def cargar_entradas_en_treeview(evento_id, tree):
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()
        consulta = "SELECT tipo, precio, cupo_total, asiento FROM Entrada WHERE Evento_id = %s"
        cursor.execute(consulta, (evento_id,))
        resultados = cursor.fetchall()

        tree.delete(*tree.get_children())
        for tipo, precio, cupo, asiento in resultados:
            tree.insert("", "end", values=(tipo, precio, cupo, "✔️" if asiento else "❌"))

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar entradas: {e}")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

def guardar_entrada(eventos_dict, combo_eventos, ent_tipo, ent_precio, ent_cupo,
                    tree_entradas, var_asiento, ent_filas, ent_columnas):
    tipo = ent_tipo.get()
    precio = ent_precio.get()
    titulo = combo_eventos.get()
    asiento = var_asiento.get()

    if not (tipo and precio and titulo):
        messagebox.showwarning("Campos vacíos", "Completa todos los campos obligatorios.")
        return

    try:
        precio = float(precio)
        evento_id = eventos_dict[titulo]

        if asiento:
            filas = int(ent_filas.get())
            columnas = int(ent_columnas.get())
            cupo_total = filas * columnas
        else:
            cupo_total = int(ent_cupo.get())
            filas = columnas = None

        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = """INSERT INTO Entrada (Evento_id, tipo, precio, cupo_total, cupo_disponible, asiento)
                      VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(consulta, (evento_id, tipo, precio, cupo_total, cupo_total, asiento))
        conexion.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        id_entrada = cursor.fetchone()[0]

        if asiento:
            for f in range(1, filas + 1):
                for c in range(1, columnas + 1):
                    cursor.execute("""INSERT INTO Asiento (fila, columna, disponible, Entrada_id)
                                      VALUES (%s, %s, %s, %s)""",
                                   (f, c, True, id_entrada))
            conexion.commit()

        messagebox.showinfo("Éxito", "¡Entrada registrada correctamente!")
        ent_tipo.delete(0, END)
        ent_precio.delete(0, END)
        ent_cupo.delete(0, END)
        ent_filas.delete(0, END)
        ent_columnas.delete(0, END)

        cargar_entradas_en_treeview(evento_id, tree_entradas)

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar entrada: {e}")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass

def cargar_todas_entradas(id_organizador, tree):
    try:
        conexion = funciones_generales.iniciarConexion(vectorConexion)
        cursor = conexion.cursor()

        consulta = """
            SELECT Entrada.tipo, Entrada.precio, Entrada.cupo_total, Entrada.asiento
            FROM Entrada
            JOIN Evento ON Entrada.Evento_id = Evento.id_evento
            WHERE Evento.id_organizador = %s
        """
        cursor.execute(consulta, (id_organizador,))
        resultados = cursor.fetchall()

        tree.delete(*tree.get_children())
        for tipo, precio, cupo, asiento in resultados:
            tree.insert("", "end", values=(tipo, precio, cupo, "✔️" if asiento else "❌"))

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar entradas: {e}")
    finally:
        try:
            cursor.close()
            conexion.close()
        except:
            pass
