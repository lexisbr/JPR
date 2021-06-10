# Imports
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from grammar import interfaz as compilar

# Metodos
# Actualizar lineas
def lineas(*args):
    linesLbl.delete("all")

    cont = entradaTxt.index("@1,0")
    while True:
        dline = entradaTxt.dlineinfo(cont)
        if dline is None:
            break
        y = dline[1]
        strline = str(cont).split(".")[0]
        linesLbl.create_text(2, y, anchor="nw", text=strline,
                          font=("Consolas", 10))
        cont = entradaTxt.index("%s+1line" % cont)

# Actualizar posicion
def posicion(event=None):
    actualizarArchivoLbl()
    posicionLbl.config(
        text="Fila: " + str(entradaTxt.index(INSERT)).replace(".", ", Columna: "))

# Llamar metodos
def actualizarLineas(event):
    posicion()
    lineas()

#Actualizar label del archivo modificado
def actualizarArchivoLbl():
    text_archivo = archivoLbl.cget("text") 
    last_char = text_archivo[-1]
    if last_char != "*":
        archivoLbl.config(text = archivoLbl.cget("text")+"*")

#Actualizar label de archivo guardado
def actualizarArchivoLblGuardar():
    text_archivo = archivoLbl.cget("text") 
    last_char = text_archivo[-1]
    if last_char == "*" and archivo != "":
        archivoLbl.config(text = archivo)

        

#Path del archivo en memoria
archivo=""

#Abrir archivo
def abrir():       
    global archivo
    archivo = filedialog.askopenfilename(title = "Abrir Archivo", initialdir = "C:/",filetypes=[("jpr files", ".jpr")])
    entrada = open(archivo)
    content = entrada.read()
    entradaTxt.delete(1.0, END)
    entradaTxt.insert(INSERT, content)
    entrada.close()
    lineas()
    archivoLbl.config(text = archivo)



#Nuevo archivo
def nuevo():   
    global archivo
    entradaTxt.delete(1.0, END)
    archivo = ""
    archivoLbl.config(text = "Archivo sin guardar")

#Guardar archivo
def guardarArchivo():    
    global archivo
    if archivo == "":
        guardarComo()
    else:
        guardarc = open(archivo, "w")
        guardarc.write(entradaTxt.get(1.0, END))
        guardarc.close()
        actualizarArchivoLblGuardar()

#Guardar como archivo
def guardarComo():      #GUARDAR COMO
    global archivo
    guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/",filetypes=[("jpr files", ".jpr")],defaultextension='.jpr')
    fguardar = open(guardar, "w+")
    fguardar.write(entradaTxt.get(1.0, END))
    fguardar.close()
    archivo = guardar
    archivoLbl.config(text = guardar)
    actualizarArchivoLblGuardar()

#Compilacion
def compilar_archivo():
    consoleTxt.delete(1.0, END)
    contenido = compilar(entradaTxt.get(1.0, END))
    consoleTxt.insert(INSERT,contenido)

# Declaracion del tk
root = Tk()
root.title("JPR Editor")
# Frame principal
frame = Frame(root, bg="bisque2")
frame.grid(sticky='news')
# Canvas
canvas = Canvas(frame, bg="bisque2")
canvas.grid(row=0, column=1)
# Frame del canvas
frameEditors = Frame(canvas, bg="bisque2")
canvas.create_window((0, 0), window=frameEditors, anchor="nw")
canvas.configure(width=1500, height=650)

# Componentes
#Archivo Label
archivoLbl= Label(frameEditors, text="Archivo sin guardar",width=77,background="snow",fg="gray9")
archivoLbl.grid(column=0, row=1,sticky="nw",padx=25)
# Label de fila y columna
posicionLbl= Label(frameEditors, text="Fila: 0, Columna: 0",width=20,background="gray60",fg="blue4")
posicionLbl.grid(column=0, row=1,sticky="sw",padx=25)
# ScrolledText de entrada
entradaTxt = scrolledtext.ScrolledText(frameEditors, undo=True, width=70, height=15)
entradaTxt.grid(column=0, row=1, pady=30, padx=60)
# ScrolledText de la consola
consoleTxt = scrolledtext.ScrolledText(frameEditors, undo=True, width=70, height=15,bg="black",foreground="white")
consoleTxt.grid(column=1, row=1, pady=30, padx=40)
# Canvas de fila del editor
linesLbl = Canvas(frameEditors, width=30, height=258, background='gray60')
linesLbl.grid(column=0, row=1,padx=25,sticky="w")
# Menu bar
menu = Menu(frameEditors)
nuevoItem = Menu(menu,tearoff=0)
nuevoItem.add_command(label='Nuevo',command=nuevo)
nuevoItem.add_command(label='Abrir',command=abrir)
nuevoItem.add_command(label='Guardar',command=guardarArchivo)
nuevoItem.add_command(label='Guardar como',command=guardarComo)
menu.add_cascade(label='Archivo', menu=nuevoItem)
root.config(menu=menu)
#Titulo
tituloLbl = Label(frameEditors,text="JPR Editor",font="Helvetica 18",fg="blue4")
tituloLbl.grid(row=0,column=0,sticky="e",pady=10)
#Label Tabla de Simbolos
simbolosLbl = Label(frameEditors,text="Tabla de Simbolos",font="Helvetica 18",fg="blue4")
simbolosLbl.grid(row=5,column=0,pady=30)
#Label Tabla de Errores
erroresLbl = Label(frameEditors,text="Tabla de Errores",font="Helvetica 18",fg="blue4")
erroresLbl.grid(row=5,column=1)
#Boton de compilacion
compilarButton= Button(frameEditors,text="Compilar",width=10,command=compilar_archivo)
compilarButton.grid(row=1,column=0,sticky="s")

#Tabla De Simbolos
tv=ttk.Treeview(frameEditors,height=7)
tv['columns']=('#', 'Identificador', 'Tipo', 'Dimension', 'Valor', 'Ambito', 'Referencias')
tv.column('#0', width=0, stretch=NO)
tv.column('#', anchor=CENTER, width=10)
tv.column('Identificador', anchor=CENTER, width=110)
tv.column('Tipo', anchor=CENTER, width=80)
tv.column('Dimension', anchor=CENTER, width=110)
tv.column('Valor', anchor=CENTER, width=80)
tv.column('Ambito', anchor=CENTER, width=80)
tv.column('Referencias', anchor=CENTER, width=110)
tv.heading('#0', text='', anchor=CENTER)
tv.heading('#', text='#', anchor=CENTER)
tv.heading('Identificador', text='Identificador', anchor=CENTER)
tv.heading('Tipo', text='Tipo', anchor=CENTER)
tv.heading('Dimension', text='Dimension', anchor=CENTER)
tv.heading('Valor', text='Valor', anchor=CENTER)
tv.heading('Ambito', text='Ambito', anchor=CENTER)
tv.heading('Referencias', text='Referencias', anchor=CENTER)

tv.grid(column=0, row=6,padx=25,sticky="w")

#Tabla Reporte de erroresLbl
tv1=ttk.Treeview(frameEditors,height=7)
tv1['columns']=('#', 'Tipo', 'Descripcion', 'Linea', 'Columna')
tv1.column('#0', width=0, stretch=NO)
tv1.column('#', anchor=CENTER, width=10)
tv1.column('Tipo', anchor=CENTER, width=100)
tv1.column('Descripcion', anchor=CENTER, width=350)
tv1.column('Linea', anchor=CENTER, width=100)
tv1.column('Columna', anchor=CENTER, width=100)
tv1.heading('#0', text='', anchor=CENTER)
tv1.heading('#', text='#', anchor=CENTER)
tv1.heading('Tipo', text='Tipo', anchor=CENTER)
tv1.heading('Descripcion', text='Descripcion', anchor=CENTER)
tv1.heading('Linea', text='Linea', anchor=CENTER)
tv1.heading('Columna', text='Columna', anchor=CENTER)
tv1.grid(row=6,column=1)



# Acciones del teclado
entradaTxt.bind('<Return>', actualizarLineas)
entradaTxt.bind('<BackSpace>', actualizarLineas)
entradaTxt.bind('<<Change>>', actualizarLineas)
entradaTxt.bind('<Configure>', actualizarLineas)
entradaTxt.bind('<Motion>', actualizarLineas)
entradaTxt.bind('<KeyPress>', posicion)
entradaTxt.bind('<Button>', posicion)
entradaTxt.bind('<Key>', actualizarLineas)
entradaTxt.bind('<Enter>', actualizarLineas)


# Main loop
root.mainloop()

