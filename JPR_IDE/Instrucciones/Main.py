from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Main(Instruccion):
    def __init__(self, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table) 
        listaerrores= []
        for instruccion in self.instrucciones:      # REALIZAR LAS ACCIONES
            value = instruccion.interpretar(tree,nuevaTabla)
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
                listaerrores.append(value)
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())
                listaerrores.append(err)
        return listaerrores
    
    def getNodo(self):
        nodo = NodoAST("MAIN")

        instrucciones = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo 
     