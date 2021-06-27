import tkinter as tk
from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Tipo import TIPO

class Read(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.CADENA

    def interpretar(self, tree, table):
        lectura = self.messageBox("Ingrese el valor del read") 
        return lectura

    def getNodo(self):
        nodo = NodoAST("READ")
        return nodo 

    def messageBox(self,prompt):
        root = tk.Toplevel()
        var = tk.StringVar()
        # GUI
        label = tk.Label(root, text=prompt)
        entry = tk.Entry(root, textvariable=var)
        label.pack(side="left", padx=(20, 0), pady=20)
        entry.pack(side="right", fill="x", padx=(0, 20), pady=20, expand=True)
        entry.bind("<Return>", lambda event: root.destroy())
        root.wait_window()
        value = var.get()
        return value