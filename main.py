import sys
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tabulate import tabulate


"""--------------------------- Variables globales -----------------------------------------------"""

gramaticaLeida = []  # lista de gramatica leida
gramaticaPunto = []  # lista completa gramatica con punto
noTerminales = []  # lista de no terminales
terminales = []  # lista de terminales
terminalesMasNoTerminales = []  # lista de terminales mas no terminales
estados = []  # lista de estados del automata
transiciones = []  # lista de transiciones del automata
tabla = []  # tabla estática


"""--------------------------- Diseño interfaz del proyecto -------------------------------------"""

# Se crea la ventana:
ventana = Tk()

# Se le da un tamaño:
ventana.geometry("1350x670")

# Agregando un titulo a la ventana
ventana.title("Proyecto 2 Lenguajes")

# En este canvas colocaremos las herramientas que nos permitan manipular el programa
canvas_principal = Canvas(ventana, width=1350, height=670, bg="#2E065E")
canvas_principal.place(x=0, y=0)

"""--------------------------------------- Menú -----------------------------------------"""

# Insertar la gramática
lblGramatica = Label(canvas_principal, fg="white", bg="#2E065E", width=18, text="Gramática",
                     font=("Arial", 16)).place(x=75, y=20)

textGramatica = scrolledtext.ScrolledText(
    ventana, wrap=tk.WORD, width=23, height=9, font=("Arial", 15))
textGramatica.grid(column=0, row=0, padx=40, pady=60)
textGramatica.focus()

# Muestra información de la gramatica leida
lstGramaticaLeida = scrolledtext.ScrolledText(ventana, fg="white", bg="#2E065E", width=35, height=12, font=(
    "Arial", 10), relief="solid", highlightbackground="white", highlightthickness=2)
lstGramaticaLeida.place(x=35, y=410)

# Muestra información de los estados
lstEstados = scrolledtext.ScrolledText(ventana, fg="white", bg="#2E065E", width=33, height=16, font=(
    "Arial", 10), relief="solid", highlightbackground="white", highlightthickness=2)
lstEstados.place(x=380, y=20)

# Muestra información de las transiciones
lstTransiciones = scrolledtext.ScrolledText(ventana, fg="white", bg="#2E065E", width=33, height=16, font=(
    "Arial", 10), relief="solid", highlightbackground="white", highlightthickness=2)
lstTransiciones.place(x=380, y=340)

# Muestra la tabla sintáctica
lstTablaSintactica = scrolledtext.ScrolledText(
    ventana, fg="white", bg="#2E065E", width=75, height=38, relief="solid", highlightbackground="white", highlightthickness=2)
lstTablaSintactica.place(x=700, y=20)


"""---------------------------------- Funciones -------------------------------------------"""

# Leer gramatica desde el input


def leerGramatica():
    gram = textGramatica.get(1.0, END).split('\n')
    gram.remove('')

    for linea in gram:
        lineaLimpia = linea.replace(" ", "")
        gramaticaLeida.append(lineaLimpia)


# Mostrar la gramática leída
def mostrarGramaticaLeida():
    lstGramaticaLeida.delete(1.0, END)
    lstGramaticaLeida.insert(
        END, f"       ------------- Gramática leída ----------")
    for gram in gramaticaLeida:
        lstGramaticaLeida.insert(END, "\n\n " + gram)
    lstGramaticaLeida.configure(state='disabled')


#  Dividir terminales y no terminales
def dividirTerminalesYNoTerminales():
    for s in gramaticaLeida:
        x, y = s.split("->")

        if x not in noTerminales:
            noTerminales.append(x)

        for v in y:
            if v.isupper():
                if v not in noTerminales:
                    noTerminales.append(v)
            else:
                if v not in terminales:
                    terminales.append(v)
    terminales.append("$")
    terminalesMasNoTerminales.extend(noTerminales)
    terminalesMasNoTerminales.extend(terminales)


#  Agregar punto a todas las producciones
def agregarPunto():
    # gramática aumentada
    str0 = "S'->." + gramaticaLeida[0][0]
    gramaticaPunto.append(str0)
    str1 = "S'->" + gramaticaLeida[0][0] + "."
    gramaticaPunto.append(str1)

    for gram in gramaticaLeida:
        for i in range(len(gram) - 2):
            tmp = gram[:3 + i] + "." + gram[3 + i:]
            gramaticaPunto.append(tmp)


#  Gramática No terminales
def obtenerGramNoTerminal(v):
    res = []
    for gram in gramaticaPunto:
        index = gram.find("->")
        if gram[0] == v and gram[index + 2] == ".":
            res.append(gram)
    return res


# operacion LR(0)
def lr0(I):
    lr0 = I
    for it in I:
        if it not in lr0:
            lr0.append(it)
        x, y = it.split(".")
        if y == "":  # . Seguido por terminal, sin operación, salta al siguiente ciclo
            continue
        v = y[0]
        if v in noTerminales:  # . Seguido por un no Terminal , Join in B->.γ
            res = obtenerGramNoTerminal(v)
            for re in res:
                if re not in lr0:
                    lr0.append(re)
    return lr0


# funcion irA
def irA(I, v):
    #  Generar y volver al siguiente elemento
    temporal = []
    for it in I:
        x, y = it.split(".")
        if y != "":
            if y[0] == v:
                new_it = x + y[0] + "." + y[1:]
                temporal.append(new_it)

    if len(temporal) != 0:
        nuevoEstado = lr0(temporal)
        return nuevoEstado


# verificar si un estado ya existe
def estaEnEstados(nuevoEstado):
    #  verificar si un estado ya existe , Hay una ubicación de devolución , No hay devolución -1
    if nuevoEstado is None:
        return -1
    nuevoSet = set(nuevoEstado)
    num = 0
    for item in estados:
        viejoSet = set(item)
        if viejoSet == nuevoSet:
            return num
        num = num + 1
    return -1


#  add to DFA The conversion function of
def myAppend(xx, v, xy):
    t = []
    t.append(xx)
    t.append(v)
    t.append(xy)
    transiciones.append(t)


#  obtener estados
def obtenerEstados():
    estado = []
    estado.append(gramaticaPunto[0])
    it = lr0(estado)
    num = 0
    estados.append(it)
    num = num + 1

    for estado in estados:
        for v in terminalesMasNoTerminales:
            nuevoEstado = irA(estado, v)

            if nuevoEstado is not None:
                if estaEnEstados(nuevoEstado) == -1:
                    estados.append(nuevoEstado)
                    x = estaEnEstados(estado)
                    y = estaEnEstados(nuevoEstado)
                    myAppend(x, v, y)
                    num = num + 1
                else:
                    x = estaEnEstados(estado)
                    y = estaEnEstados(nuevoEstado)
                    myAppend(x, v, y)


# mostrar estados
def mostrarEstados():
    lstEstados.delete(1.0, END)
    lstEstados.insert(END, f"       ------------- Estados ----------")
    for i in range(len(estados)):
        lstEstados.insert(END, "\n\n Estado-I{0}: {1}".format(i, estados[i]))
    lstEstados.configure(state='disabled')


#  mostrar transiciones
def mostrarTransiciones():
    lstTransiciones.delete(1.0, END)
    lstTransiciones.insert(END, f"      -------- Transiciones --------")
    for f in transiciones:
        lstTransiciones.insert(
            END, "\n\n Transición (I{0} -> I{2}) = {1}".format(f[0], f[1], f[2]))
    lstTransiciones.configure(state='disabled')


#  crear tabla sintáctica
def crearTabla():
    tmp = []
    tmp1 = []
    index_tmp1 = 0
    for item in estados:
        t = []
        for it in item:
            x, y = it.split(".")
            if y == "":
                if it == gramaticaPunto[1]:
                    t.append("-1")
                else:
                    t.append("0")
                    new_gram = x + y
                    tmp1.append(estaEnGramatica(new_gram))
            else:
                t.append(y[0])
        tmp.append(t)
    # print(tmp)
    for index_temp in range(len(tmp)):
        t = []
        for v in terminales:
            # S'->E.  Aceptar
            if "-1" in tmp[index_temp]:
                if v == "$":
                    t.append("Aceptar")
                else:
                    t.append("")
            # . finales
            elif "0" in tmp[index_temp]:
                for vt in terminales:
                    t.append("R" + str(tmp1[index_tmp1]+1))
                index_tmp1 = index_tmp1 + 1
                break

            elif v in tmp[index_temp]:
                for f in transiciones:
                    if f[0] == index_temp and f[1] == v:
                        t.append("I" + str(f[2]))
                        break
            else:
                t.append("")

        for v in noTerminales:
            if v in tmp[index_temp]:
                for f in transiciones:
                    if f[0] == index_temp and f[1] == v:
                        t.append(str(f[2]))
                        break
            else:
                t.append("")
        tabla.append(t)


# mostrar la tabla sintáctica
def mostrarTablaSintactica():
    header = [''] * (len(terminales) + 1)
    header[(len(terminales) + 1) // 2] = 'ACCIÓN'
    header2 = [''] * len(noTerminales)
    header2[(len(noTerminales)) // 2] = 'IR A'

    tabla.insert(0, terminales + noTerminales)
    numerosFila = list(range(len(estados)))
    numerosFila.insert(0, 'ESTADOS')

    lstTablaSintactica.delete(1.0, END)
    lstTablaSintactica.insert(
        END, f"         ------------- Tabla Sintáctica ----------\n\n")
    lstTablaSintactica.insert(END, tabulate(tabla,
                                            headers=header + header2,
                                            tablefmt='fancy_grid',
                                            stralign='center',
                                            floatfmt='.0f',
                                            showindex=numerosFila))
    lstTablaSintactica.configure(state='disabled')


# Saber si la gramatica es LR(0)
def esLR0():
    for item in estados:
        shiftNum = 0
        protocolNum = 0
        for it in item:
            x, y = it.split(".")
            if y == "":
                protocolNum = protocolNum + 1
            elif y[0] in terminales:
                shiftNum = shiftNum + 1
        if protocolNum > 1 or (protocolNum >= 1 and shiftNum >= 1):
            print("\nNO es una gramática LR(0)")
            return -1
    print("\nSI es una gramática LR(0)")
    return 1


# Esta en la gramatica
def estaEnGramatica(nuevaGramatica):
    if nuevaGramatica is None:
        return -1
    for i in range(len(gramaticaLeida)):
        if nuevaGramatica == gramaticaLeida[i]:
            return i
    return -1


# Iniciar el Programa, lo activa el boton "iniciar"
def iniciarPrograma():
    if len(textGramatica.get(1.0, END)) == 1:
        messagebox.showerror(message="Gramatica Vacía", title="Error")
    else:
        btn_Iniciar["state"] = "disabled"
        leerGramatica()
        mostrarGramaticaLeida()
        dividirTerminalesYNoTerminales()
        agregarPunto()
        obtenerEstados()
        mostrarEstados()
        mostrarTransiciones()
        crearTabla()
        mostrarTablaSintactica()


'''---------------------------------------- Botonera -----------------------------------------'''

# Este botón inicia el programa:
btn_Iniciar = Button(ventana, fg="white", bg="#1E6F4A", width=15, text="Iniciar", state="normal", font=("Arial", 10),
                     command=iniciarPrograma)
btn_Iniciar.place(x=40, y=350)

# Este botón termina el programa:
btn_Salir = Button(canvas_principal, fg="white", bg="#1E6F4A", width=15, text="Salir", font=("Arial", 10),
                   command=sys.exit).place(x=200, y=350)

ventana.mainloop()
