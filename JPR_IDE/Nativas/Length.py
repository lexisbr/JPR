from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion


class Length(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
        self.length = 0

    def interpretar(self, tree, table):
        simbolo = table.getTabla("Length##Param1")
        if simbolo == None : return Excepcion("Semantico", "No se encontró el parámetro de Length", self.fila, self.columna)

        if simbolo.getTipo() != TIPO.CADENA and not(simbolo.getArreglo()):
            return Excepcion("Semantico", "Tipo de parametro de Length no es cadena o un arreglo.", self.fila, self.columna)

        self.tipo = TIPO.ENTERO
        
        if(simbolo.getArreglo()):
            expresiones = simbolo.getValor()
            self.getLength(expresiones)
            return self.length
        else:
            return len(simbolo.getValor()) 

    def getLength(self, expresiones):
        self.length = 0
        for expresion in expresiones:
            if(isinstance(expresion,list)):
                self.getLength(expresion)
            else:
                self.length += 1 