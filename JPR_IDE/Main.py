# Imports
import os
import platform
import re
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from grammar import interfaz as compilar
from grammar import getErrores as lista_errores

# Metodos

# Recorrer el texto para separar palabras por colores
def recorrerInput(i):  
    lista = []
    val = ''
    counter = 0
    while counter < len(i):
            if re.search(r"[a-z|0-9|.|A-Z]", i[counter]):
                val += i[counter]
            elif i[counter] == "\"":
                if len(val) != 0:
                    l = []
                    l.append("cadena")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = i[counter]
                counter += 1
                
                while counter < len(i):
                    if i[counter] == "\"":
                        val += i[counter]
                        l = []
                        l.append("cadena")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += i[counter]
                    counter += 1
            elif i[counter] == "#":
                if len(val) != 0:
                    l = []
                    l.append("comentario")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = i[counter]
                counter += 1
                if i[counter] == "*":
                   while counter < len(i):
                        if i[counter] == "#":
                            val += i[counter]
                            l = []
                            l.append("comentario")
                            l.append(val)
                            lista.append(l)
                            val = ''
                            break
                        val += i[counter]
                        counter += 1 
                else:    
                    while counter < len(i):
                        if i[counter] == "\n":
                            val += i[counter]
                            l = []
                            l.append("comentario")
                            l.append(val)
                            lista.append(l)
                            val = ''
                            break
                        val += i[counter]
                        counter += 1
            elif i[counter] == "\'":
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                val = i[counter]
                counter += 1
                while counter < len(i):
                    if i[counter] == "\'":
                        val += i[counter]
                        l = []
                        l.append("cadena")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += i[counter]
                    counter += 1
            else:
                if len(val) != 0:
                    l = []
                    l.append("variable")
                    l.append(val)
                    lista.append(l)
                    val = ''
                l = []
                l.append("normal")
                l.append(i[counter])
                lista.append(l)
            counter +=1
    for s in lista:
        if s[1] == 'var' or s[1] == 'func' or s[1] == 'read' or s[1] == 'tolower' or s[1] == 'toupper' or s[1] == 'lenght' or s[1] == 'truncate' or s[1] == 'round' or s[1] == 'typeof' or s[1] == 'return' or s[1] == 'break' or s[1] == 'switch' or s[1] == 'case' or s[1] == 'default' or s[1] == 'false' or s[1] == 'true' or s[1] == 'while' or s[1] == 'for' or s[1] == 'continue' or  s[1] == 'else' or s[1] == 'if' or s[1] == 'null' or s[1] == 'boolean' or s[1] == 'string' or s[1] == 'int' or s[1] == 'double' or s[1] == 'char' or s[1] == 'print' or s[1] == 'main':
            s[0] = 'reservada'
        elif re.search(r'\d+',s[1]) or re.search(r'\d+\.\d+',s[1]):
            if re.search(r'\".*?\"',s[1]):
                s[0] = 'cadena'
            elif re.search(r'\#\*(.|\n)*?\*\#|\#.*\n',s[1]):
                s[0] = 'comentario'
            elif re.search(r'[a-z|A-Z]',s[1]):
                s[0]= "normal"
            else:
                s[0] = 'numero'
        elif re.search(r'\".*?\"',s[1]):
            s[0] = 'cadena'
        elif re.search(r'\#\*(.|\n)*?\*\#|\#.*\n',s[1]):
            s[0] = 'comentario'
    return lista

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

# Pintar texto
def pintar_texto():
    contenido = entradaTxt.get(1.0, END)
    entradaTxt.delete(1.0, "end")
    for s in recorrerInput(contenido):
        entradaTxt.insert(INSERT, s[1], s[0])        

#Path del archivo en memoria
archivo=""

#Abrir archivo
def abrir():       
    global archivo
    archivo = filedialog.askopenfilename(title = "Abrir Archivo", initialdir = "C:/",filetypes=[("jpr files", ".jpr")])
    entrada = open(archivo)
    content = entrada.read()
    entradaTxt.delete(1.0, END)
    for s in recorrerInput(content):
        entradaTxt.insert(INSERT, s[1], s[0])
    entrada.close()
    lineas()
    archivoLbl.config(text = archivo)
    consoleTxt.delete(1.0, END)


#Nuevo archivo
def nuevo():   
    global archivo
    entradaTxt.delete(1.0, END)
    consoleTxt.delete(1.0, END)
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
        pintar_texto()
            
#Guardar como archivo
def guardarComo():      #GUARDAR COMO
    global archivo
    guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/",filetypes=[("jpr files", ".jpr")],defaultextension='.jpr')
    if(guardar):
        fguardar = open(guardar, "w+")
        fguardar.write(entradaTxt.get(1.0, END))
        fguardar.close()
        archivo = guardar
        archivoLbl.config(text = guardar)
        actualizarArchivoLblGuardar()
        pintar_texto()

#Compilacion
def compilar_archivo():
    consoleTxt.delete(1.0, END)
    contenido = compilar(entradaTxt.get(1.0, END))
    consoleTxt.insert(INSERT,contenido)
    excepciones = lista_errores()
    cont = 1
    tabla_errores.delete(*tabla_errores.get_children())
    for excepcion in excepciones:
        tabla_errores.insert(parent='',index=cont,iid=cont,text='',values=(cont,excepcion.getTipo(),excepcion.getDescripcion(),excepcion.getFila(),excepcion.getColumna()))
        cont += 1
    pintar_texto()
        
# Exportar errores
def exportar_errores():
    archivo = "tablaErrores.dot"
    salida = "digraph errores {\n"
    salida += "tbl [\n shape = plaintext\n"
    salida += "label=<\n"
    salida += "<table border=\"1\" cellborder=\"1\" cellspacing=\"1\" cellpadding=\"8\">\n"
    salida += "<tr> <td colspan='5'>Reporte de Errores</td> </tr> \n"
    salida += "<tr> <td> </td> <td>Tipo</td> <td>Descripcion</td> <td>Linea</td> <td>Columna</td> </tr> \n"
    excepciones = lista_errores()
    cont = 1
    for excepcion in excepciones:
        salida += "<tr> <td>"+str(cont)+"</td> <td>"+excepcion.getTipo()+"</td> <td>"+excepcion.getDescripcion()+"</td> <td>"+str(excepcion.getFila())+"</td> <td>"+str(excepcion.getColumna())+"</td> </tr> \n"
        cont += 1
    salida += "</table>\n"
    salida += ">];\n"
    salida += "}"
    
    with open(archivo,'w') as f:
        f.write(salida) 
    
    os.system('dot -Tjpg '+archivo+' -o imagen.jpg')
    
    if(platform.system() == "Linux"):
        os.system('xdg-open imagen.jpg')
    else:
        os.startfile('imagen.jpg')
    
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
#Boton para exportar errores
exportarButton= Button(frameEditors,text="Exportar errores",width=10,command=exportar_errores)
exportarButton.grid(row=7,column=1,sticky="s")

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
tabla_errores=ttk.Treeview(frameEditors,height=7)
tabla_errores['columns']=('#', 'Tipo', 'Descripcion', 'Linea', 'Columna')
tabla_errores.column('#0', width=0, stretch=NO)
tabla_errores.column('#', anchor=CENTER, width=10)
tabla_errores.column('Tipo', anchor=CENTER, width=100)
tabla_errores.column('Descripcion', anchor=CENTER, width=350)
tabla_errores.column('Linea', anchor=CENTER, width=100)
tabla_errores.column('Columna', anchor=CENTER, width=100)
tabla_errores.heading('#0', text='', anchor=CENTER)
tabla_errores.heading('#', text='#', anchor=CENTER)
tabla_errores.heading('Tipo', text='Tipo', anchor=CENTER)
tabla_errores.heading('Descripcion', text='Descripcion', anchor=CENTER)
tabla_errores.heading('Linea', text='Linea', anchor=CENTER)
tabla_errores.heading('Columna', text='Columna', anchor=CENTER)
tabla_errores.grid(row=6,column=1)



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

# Tags para pintar el textos
entradaTxt.tag_config('reservada', foreground='DodgerBlue2')
entradaTxt.tag_config('cadena', foreground='orange')
entradaTxt.tag_config('numero', foreground='purple2')
entradaTxt.tag_config('comentario', foreground='gray')
entradaTxt.tag_config('normal', foreground='green2')


# Main loop
root.mainloop()

