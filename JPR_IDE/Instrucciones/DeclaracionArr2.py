from re import A
from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
import copy


class DeclaracionArr2(Instruccion):
    def __init__(self, tipo, corchetes, identificador, expresiones, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.t_esperado= tipo
        self.corchetes = corchetes
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.arreglo = True


    def interpretar(self, tree, table):
        try:
            print("expresiones "+str(self.expresiones))
            dimensiones = self.dimensiones(self.expresiones,0)
            arreglo = []
            
            if self.corchetes == dimensiones:
                #crear arreglos
                value = self.crear_dimensiones(tree, table, copy.copy(self.expresiones),self.tipo)  # RETORNA EL ARREGLO DE DIMENSIONES
                if isinstance(value, Excepcion): return value
                simbolo = Simbolo(str(self.identificador), self.tipo, self.arreglo, self.fila, self.columna, value)

                result = table.setTabla(simbolo)
                print(result)
                if isinstance(result, Excepcion): return result
                return None
            else:
                return Excepcion("Semantico","El indice del array sobrepasa el rango.",self.fila,self.columna)
        except:
            return Excepcion("Semantico","El indice del array sobrepasa el rango.",self.fila,self.columna)
        
    def dimensiones(self, element, ttry):
        if isinstance(element, list):
            if isinstance(element[0], list):
                ttry += 1
                return self.dimensiones(element[0], ttry)
            else:
                return ttry
       
            

    def crear_dimensiones(self, tree, table, expresiones,tipo):
        arr = []
        if len(expresiones) == 0:
            return None
        dimension = expresiones.pop(0)
        #verificar si es una lista o una expresion, para ver si se interpreta o no
        if isinstance(dimension,list):
            cant_list = len(dimension)
            while  cant_list != 0:
                arreglo = self.crear_dimensiones(tree,table,dimension,tipo)
                arr.append(arreglo)
                cant_list -= 1
        else:
            primitivo = dimension.interpretar(tree,table)
            if self.t_esperado == dimension.tipo:
                return  primitivo
            else:
                return Excepcion("Semantico","JPR.ArrayTypeError: No se puede inferir tipo de datos en Arreglos",self.fila,self.columna)

        return arr
    
    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(self.dimensiones))
        nodo.agregarHijo(str(self.identificador))
        '''exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.expresiones:
            exp.agregarHijoNodo(str(expresion))
        nodo.agregarHijoNodo(exp)'''
        return nodo



