from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion


class TypeOf(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("typeof##Param1")
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de type of", self.fila, self.columna)

        self.tipo = TIPO.CADENA
        return str(simbolo.getTipo()).replace("TIPO.","")