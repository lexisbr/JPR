from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from TS.Tipo import TIPO
from Instrucciones.Break import Break
import copy


class Llamada(Instruccion):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        self.arreglo = False
    
    def interpretar(self, tree, table):
        result = tree.getFuncion(self.nombre.lower()) ## OBTENER LA FUNCION
        if result == None: # NO SE ENCONTRO LA FUNCION
            return Excepcion("Semantico", "NO SE ENCONTRO LA FUNCION: " + self.nombre, self.fila, self.columna)
        nuevaTabla = TablaSimbolos(tree.getTSGlobal())
        # OBTENER PARAMETROS
        if len(result.parametros) == len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
            contador=0
            for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                resultExpresion = expresion.interpretar(tree, table)
                if isinstance(resultExpresion, Excepcion): return resultExpresion

                if result.parametros[contador]['identificador'] == 'Truncate##Param1' or result.parametros[contador]['identificador']=='Round##Param1' or result.parametros[contador]['identificador']=='Typeof##Param1' or result.parametros[contador]['identificador']=='Length##Param1':
                    result.parametros[contador]['tipo'] = expresion.tipo
                
                try:
                    simboloEncontrado = table.getTabla(expresion.identificador)
                    if(simboloEncontrado.getArreglo() and (result.parametros[contador]['identificador']=='Length##Param1' or result.parametros[contador]['identificador']=='Typeof##Param1')):
                        result.parametros[contador]['tipo'] = expresion.tipo
                        self.arreglo=True
                except:
                    pass
                    
                if result.parametros[contador]["tipo"] == expresion.tipo or result.parametros[contador]["tipo"]==TIPO.ARREGLO:  # VERIFICACION DE TIPO
                    # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                    if result.parametros[contador]["tipo"]==TIPO.ARREGLO:
                        self.arreglo=True    
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), expresion.tipo, self.arreglo, self.fila, self.columna, resultExpresion)
                    else:
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), result.parametros[contador]['tipo'], self.arreglo, self.fila, self.columna, resultExpresion) 
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla

                else:
                    return Excepcion("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila, self.columna)
                contador += 1

            
        else: 
            return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
    
        value = result.interpretar(tree, nuevaTabla)         # INTERPRETAR EL NODO FUNCION
        if isinstance(value, Excepcion): return value
        self.tipo = result.tipo
        
        return value
    
    def getNodo(self):
        nodo = NodoAST("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        return nodo