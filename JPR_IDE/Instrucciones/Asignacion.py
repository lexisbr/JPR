from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
from TS.Tipo import OperadorAritmetico

class Asignacion(Instruccion):
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.arreglo = False
        
    def interpretar(self, tree, table):
        if(self.expresion=='++'):
            simbolo = Simbolo(self.identificador, OperadorAritmetico.INCREMENTO, self.arreglo, self.fila, self.columna, 1)
        elif(self.expresion=='--'):
            simbolo = Simbolo(self.identificador, OperadorAritmetico.DECREMENTO, self.arreglo, self.fila, self.columna, -1)
        else:    
            value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
            if isinstance(value, Excepcion): return value

            simbolo = Simbolo(self.identificador, self.expresion.tipo, self.arreglo, self.fila, self.columna, value)

        result = table.actualizarTabla(simbolo)

        if isinstance(result, Excepcion): return result
        return None
    
    def getNodo(self):
            nodo = NodoAST("ASIGNACION")
            nodo.agregarHijo(str(self.identificador))
            if self.expresion!=None and self.expresion!='++' and self.expresion!='--':
                nodo.agregarHijoNodo(self.expresion.getNodo())
            elif self.expresion=='++':
                nodo2 = NodoAST("INCREMENTO")
                nodo.agregarHijoNodo(nodo2)
            elif self.expresion=='--':
                nodo2 = NodoAST("DECREMENTO")
                nodo.agregarHijoNodo(nodo2)
            return nodo
    