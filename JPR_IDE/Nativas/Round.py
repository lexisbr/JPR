from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion


class Round(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("round##Param1")
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de round", self.fila, self.columna)

        if simbolo.getTipo() != TIPO.ENTERO and simbolo.getTipo() != TIPO.DECIMAL:
            return Excepcion("Semantico", "Tipo de parametro de Round no es un valor numerico.", self.fila, self.columna)

        self.tipo = TIPO.ENTERO
        return int(round(simbolo.getValor()))