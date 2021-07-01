
class Simbolo:
    def __init__(self, identificador, tipo, fila, columna, valor ):
        self.id = identificador
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.valor = valor
        self.entorno = None

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo  

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor
        
    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna
    
    def setEntorno(self, entorno):
        self.entorno = entorno

    def getEntorno(self):
        return self.entorno