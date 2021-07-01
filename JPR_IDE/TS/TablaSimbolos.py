from TS.Tipo import OperadorAritmetico
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO


simbolos = []
entorno = ""
class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior

    def setTabla(self, simbolo):      # Agregar una variable
        global simbolos 
        if simbolo.id.lower() in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            bandera=True
            if len(simbolos)>0:
                for simbolo_aux in simbolos:
                    if simbolo_aux.id==simbolo.id and simbolo_aux.entorno==entorno and simbolo_aux.fila==simbolo.fila and simbolo_aux.columna==simbolo.columna :
                        bandera=True
                        break
                    else:
                        bandera=False
                if bandera==False:
                    simbolo.entorno=entorno
                    simbolos.append(simbolo)
            else:
                simbolo.entorno=entorno
                simbolos.append(simbolo)
            return None

    def getTabla(self, id):            # obtener una variable
        try:
            tablaActual = self
            while tablaActual != None:
                if id.lower() in tablaActual.tabla :
                    return tablaActual.tabla[id.lower()]           # RETORNA SIMBOLO
                else:
                    tablaActual = tablaActual.anterior
            return None
        except:
            return None
            

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id.lower() in tablaActual.tabla :
                if tablaActual.tabla[simbolo.id.lower()].getTipo() == simbolo.getTipo() or tablaActual.tabla[simbolo.id.lower()].getTipo()== TIPO.VAR or simbolo.getTipo()== TIPO.NULO:
                    if simbolo.getTipo()== TIPO.NULO:
                        tablaActual.tabla[simbolo.id.lower()].setTipo(TIPO.VAR)
                    else:
                        tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())
                    tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                    actualizarSimbolo(simbolo.id,tablaActual.tabla[simbolo.id.lower()].getValor(),tablaActual.tabla[simbolo.id.lower()].getTipo(),simbolo.getFila(),simbolo.getColumna())
                    return None #VARIABLE ACTUALIZADA
                elif simbolo.getTipo() == OperadorAritmetico.INCREMENTO or simbolo.getTipo() == OperadorAritmetico.DECREMENTO:
                    if (tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.ENTERO or tablaActual.tabla[simbolo.id.lower()].getTipo() == TIPO.DECIMAL):
                        valorAnterior = tablaActual.tabla[simbolo.id.lower()].getValor()
                        tablaActual.tabla[simbolo.id.lower()].setValor(valorAnterior+simbolo.getValor())
                        actualizarSimbolo(simbolo.id,tablaActual.tabla[simbolo.id.lower()].getValor(),tablaActual.tabla[simbolo.id.lower()].getTipo(),simbolo.getFila(),simbolo.getColumna())
                        return None
                return Excepcion("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable no encontrada en asignacion.", simbolo.getFila(), simbolo.getColumna())
    
    def getSimbolos(self):
        return simbolos
    
    def vaciarSimbolos(self):
        global simbolos
        simbolos=[]
        
    def setEntorno(self, ambito):
        global entorno
        entorno= ambito
    
def actualizarSimbolo(id,valor,tipo,fila,columna):
    global simbolos
    global entorno
    for simbolo in simbolos:
        if simbolo.id==id and entorno == simbolo.getEntorno() and simbolo.fila==fila and simbolo.columna==columna:
            simbolo.setValor(valor)
            simbolo.setTipo(tipo)
            break