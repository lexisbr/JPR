from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from Instrucciones.Break import Break
from TS.Excepcion         import Excepcion
from TS.Tipo              import TIPO
from TS.TablaSimbolos     import TablaSimbolos

class For(Instruccion):
    def __init__(self, value_init, condicion, incremento_decremento, instrucciones,linea,columna):
        self.condicion         = condicion
        self.value_init        = value_init
        self.incr_decr         = incremento_decremento
        self.instrucciones     = instrucciones
        self.linea             = linea
        self.columna           = columna

        

    def interpretar(self, tree, table):
        value_init = self.value_init.interpretar(tree,table)
        if isinstance(value_init, Excepcion): return value_init

        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:  # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL FOR
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en For ", self.fila, self.columna)
            self.incr_decr.interpretar(tree,table)


    def instruccionesInterpreter(self, instruccion, tree, table):

    # REALIZAR LAS ACCIONES
        if isinstance(instruccion, list):           #agregado
            for element in instruccion:
                self.instruccionesInterpreter(element, tree,table)
        else:              
            value = instruccion.interpretar(tree,table)
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
                

    def getNodo(self):
        nodo = NodoAST("FOR")

        instrucciones = NodoAST("INSTRUCCIONES")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo 