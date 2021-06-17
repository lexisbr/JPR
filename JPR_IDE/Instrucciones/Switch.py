from Abstract.Instruccion import Instruccion
from TS.Excepcion         import Excepcion

class Switch(Instruccion):
    def __init__(self, expresion, cases,default, fila, columna):
        self.expresion= expresion
        self.cases= cases
        self.default= default
        self.fila= fila
        self.columna = columna

    def interpretar(self, tree, table):
        if self.cases == None:
            if self.default != None:
                self.default.interpretar(tree,table)
        else:
            result = False
            for case in self.cases:
                value = case.expresion.interpretar(tree,table)
                if isinstance(value, Excepcion): return value

                value2 = self.expresion.interpretar(tree,table)
                if isinstance(value2,Excepcion): return 2

                if value2 == value:
                    result = case.interpretar(tree, table)
                    #Analiza si el case tiene break
                    if (result): 
                        break
                    else:
                        if self.default != None:
                            self.default.interpretar(tree,table)
            

    def instruccionesInterpreter(self, instruccion, tree, table):

    # Realiza las acciones
        if isinstance(instruccion, list): 
            for element in instruccion:
                self.instruccionesInterpreter(element, tree,table)
        else:              
            value = instruccion.interpretar(tree,table)
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())