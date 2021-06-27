from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorAritmetico
from Abstract.NodoAST import NodoAST

class Aritmetica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = None

    
    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None  and self.OperacionDer!="++"  and self.OperacionDer!="--":
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der


        if self.operador == OperadorAritmetico.MAS: #SUMA
            if (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO) or (self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO):
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.BOOLEANO) or (self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            elif (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.CADENA) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.CADENA) or (self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.CADENA)  or (self.OperacionIzq.tipo == TIPO.CARACTER and self.OperacionDer.tipo == TIPO.CARACTER)  or (self.OperacionIzq.tipo == TIPO.CARACTER and self.OperacionDer.tipo == TIPO.CADENA) or (self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.BOOLEANO) or (self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CARACTER) or (self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CADENA):
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + str(self.obtenerVal(self.OperacionDer.tipo, der))
            return Excepcion("Semantico", "Tipo Erroneo de operacion para +.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.MENOS: #RESTA
            if (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO) or (self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO):
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            elif (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.BOOLEANO) or (self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para -.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.POR: #MULTIPLICACION
            if (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO):
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            elif (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para *.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.DIV: #DIVISION
            if (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para /.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.POT: #POTENCIA
            if (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO):
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) ** self.obtenerVal(self.OperacionDer.tipo, der)
            elif (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) ** self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para **.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.MOD: #MODULO
            if (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para %.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.UMENOS: #NEGACION UNARIA
            if self.OperacionIzq.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para - unario.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.INCREMENTO:  # INCREMENTO
            
            if (self.OperacionIzq.tipo == TIPO.ENTERO ):
                self.tipo = TIPO.ENTERO
                print(self.obtenerVal(self.OperacionIzq.tipo, izq))
                return self.obtenerVal(self.OperacionIzq.tipo, izq) +1
            elif (self.OperacionIzq.tipo == TIPO.DECIMAL ):
                self.tipo = TIPO.DECIMAL
                print(self.obtenerVal(self.OperacionIzq.tipo, izq))
                return self.obtenerVal(self.OperacionIzq.tipo, izq) +1
            return Excepcion("Semantico", "Tipo Erroneo de operacion para ++.", self.fila, self.columna)
        
        elif self.operador == OperadorAritmetico.DECREMENTO:  # INCREMENTO
            
            if (self.OperacionIzq.tipo == TIPO.ENTERO ):
                self.tipo = TIPO.ENTERO
                print(self.obtenerVal(self.OperacionIzq.tipo, izq))
                return self.obtenerVal(self.OperacionIzq.tipo, izq) -1
            elif (self.OperacionIzq.tipo == TIPO.DECIMAL ):
                self.tipo = TIPO.DECIMAL
                print(self.obtenerVal(self.OperacionIzq.tipo, izq))
                return self.obtenerVal(self.OperacionIzq.tipo, izq) -1
            return Excepcion("Semantico", "Tipo Erroneo de operacion para --.", self.fila, self.columna)
        
        return Excepcion("Semantico", "Tipo de Operacion no Especificado.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("ARITMETICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())

        return nodo

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)
        