from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo


class Declaracion(Instruccion):
    def __init__(self, tipo, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        if(self.expresion!=None):
            value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
            if isinstance(value, Excepcion): return value
            if (self.tipo != self.expresion.tipo and self.tipo!=TIPO.VAR and self.expresion.tipo!=TIPO.NULO)  :
                return Excepcion("Semantico", "Tipo de dato diferente en Declaracion", self.fila, self.columna)
            if(self.tipo==TIPO.VAR):
                simbolo = Simbolo(str(self.identificador), self.expresion.tipo, self.fila, self.columna, value)
            else:
                simbolo = Simbolo(str(self.identificador), self.tipo, self.fila, self.columna, value)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            return None
        else:
            simbolo = Simbolo(str(self.identificador), self.tipo, self.fila, self.columna, None)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
            return None
