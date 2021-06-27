from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from Instrucciones.Break import Break
from TS.Excepcion         import Excepcion
from TS.TablaSimbolos     import TablaSimbolos

class Case(Instruccion):
    def __init__(self, expresion, instrucciones, fila, columna):
        self.expresion         = expresion
        self.instrucciones     = instrucciones
        self.fila              = fila
        self.columna           = columna


    def interpretar(self, tree, table):

        nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
        for instruccion in self.instrucciones:
            result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL CASE
            if isinstance(result, Excepcion):
                tree.getExcepciones().append(result)
                tree.updateConsola(result.toString())
            if isinstance(result, Break): return True

    def getNodo(self):
        nodo = NodoAST("CASE")

        instrucciones = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo 