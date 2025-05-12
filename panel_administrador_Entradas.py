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

    lbl1 = Label(pagina_entradas, text="Entradas", font=(fuente, 16, "bold"), background="gainsboro")
    lbl1.place(relx=0.5, y=15, anchor="center", relwidth=1, height=30)

    lbl_evento = Label(pagina_entradas, text="Evento:")
    lbl_evento.place(x=50, y=70)
    combo_eventos = ttk.Combobox(pagina_entradas, state="readonly")
    combo_eventos.place(x=150, y=70, width=250)

    lbl_tipo = Label(pagina_entradas, text="Tipo de entrada:")
    lbl_tipo.place(x=50, y=110)
    ent_tipo = Entry(pagina_entradas)
    ent_tipo.place(x=150, y=110, width=150)

    lbl_precio = Label(pagina_entradas, text="Precio:")
    lbl_precio.place(x=50, y=150)
    ent_precio = Entry(pagina_entradas)
    ent_precio.place(x=150, y=150, width=150)

    var_asiento = BooleanVar()
    check_asiento = Checkbutton(pagina_entradas, text="Tiene asiento", variable=var_asiento, bg="gainsboro", command=lambda: toggle_asientos())
    check_asiento.place(x=50, y=190)

    lbl_cupo = Label(pagina_entradas, text="Cupo total:", font=(fuente, 10, "bold"), bg="gainsboro")
    lbl_cupo.place(x=50, y=220)
    ent_cupo = Entry(pagina_entradas)
    ent_cupo.place(x=50, y=240, width=150)

    lbl_filas = Label(pagina_entradas, text="Filas:", font=(fuente, 10, "bold"), bg="gainsboro")
    ent_filas = Entry(pagina_entradas)
    lbl_columnas = Label(pagina_entradas, text="Columnas:", font=(fuente, 10, "bold"), bg="gainsboro")
    ent_columnas = Entry(pagina_entradas)

    def toggle_asientos():
        if var_asiento.get():
            lbl_filas.place(x=50, y=220)
            ent_filas.place(x=50, y=240, width=70)
            lbl_columnas.place(x=130, y=220)
            ent_columnas.place(x=130, y=240, width=70)
            lbl_cupo.place_forget()
            ent_cupo.place_forget()
        else:
            lbl_cupo.place(x=50, y=220)
            ent_cupo.place(x=50, y=240, width=150)
            lbl_filas.place_forget()
            ent_filas.place_forget()
            lbl_columnas.place_forget()
            ent_columnas.place_forget()

    eventos_dict = {}

    def cargar_eventos_combo():
        try:
            conexion = funciones_generales.iniciarConexion(vectorConexion)
            cursor = conexion.cursor()
            consulta = "SELECT id_evento, titulo FROM Evento WHERE id_organizador = %s"
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

    btn_guardar = Button(pagina_entradas, text="Guardar Entrada", 
        command=lambda: guardar_entrada(eventos_dict, combo_eventos, ent_tipo, ent_precio,
                                        ent_cupo, tree_entradas, var_asiento, ent_filas, ent_columnas))
    btn_guardar.place(x=100, y=280, width=150, height=30)

    tree_entradas = ttk.Treeview(pagina_entradas, columns=("tipo", "precio", "cupo", "asiento"), show="headings", height=8)
    tree_entradas.place(x=450, y=70, width=340)
    tree_entradas.heading("tipo", text="Tipo")
    tree_entradas.heading("precio", text="Precio")
    tree_entradas.heading("cupo", text="Cupo total")
    tree_entradas.heading("asiento", text="Asientos")

    def actualizar_treeview(*args):
        titulo_sel = combo_eventos.get()
        if titulo_sel in eventos_dict:
            cargar_entradas_en_treeview(eventos_dict[titulo_sel], tree_entradas)

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
