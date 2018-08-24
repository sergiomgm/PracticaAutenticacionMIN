from pymongo.mongo_client import MongoClient
from Usuario import Usuario
import numpy as np

class TypingPattern():
    tiemposDeVuelo = []
    tiemposDePulsacion = []
    tiempoQueTardaEnTeclearLaFrase = 0
    target = Usuario.Otro.value
    prediction = 0

    def __init__(self, target = Usuario.Otro, tiemposDePulsacion = [], tiemposDeVuelo = [], tiempoQueTardaEnTeclearLaFrase=0):
        self.target = target
        self.tiemposDeVuelo = tiemposDeVuelo
        self.tiemposDePulsacion = tiemposDePulsacion
        self.tiempoQueTardaEnTeclearLaFrase = tiempoQueTardaEnTeclearLaFrase

    def predict(self, model):
        self.prediction = model.predict([self.toTuple()[:-1]])[0]
    
    def toTuple(self):
        tupla = ()
        tupla = tupla + (self.getTiempoMedioDePulsacionDeLasTeclasDeLaPrimeraFila(), )
        tupla = tupla + (self.getTiempoMedioDePulsacionDeLasTeclasDeLaSegundaFila(), )
        tupla = tupla + self.getTiemposDePulsacionEnTupla()
        tupla = tupla + self.getTiemposDeVueloEnTupla()
        tupla = tupla + (self.tiempoQueTardaEnTeclearLaFrase, np.var(self.tiemposDePulsacion), self.target)  

        return tupla

    def save(self):
        typingPattern = {
            "tiemposDeVuelo": self.tiemposDeVuelo,
            "tiemposDePulsacion": self.tiemposDePulsacion,
            "tiempoQueTardaEnTeclearLaFrase": self.tiempoQueTardaEnTeclearLaFrase,
            "target": self.target
        }

        client = MongoClient('localhost', 27017)
        db = client['myDB']
        collection = db["autenticacion"]
        collection.insert(typingPattern)

    def getTiempoMedioDePulsacionDeLasTeclasDeLaPrimeraFila(self):
        tiempoTotal = 0.0
        
        #Tiempos de pulsacion de la t
        tiempoTotal += self.tiemposDePulsacion[0] + self.tiemposDePulsacion[5] + self.tiemposDePulsacion[9] + self.tiemposDePulsacion[13]

        #Tiempos de pulsacion de la r
        tiempoTotal += self.tiemposDePulsacion[1] + self.tiemposDePulsacion[16]

        #Tiempos de pulsacion de la e
        tiempoTotal += self.tiemposDePulsacion[2] + self.tiemposDePulsacion[10] + self.tiemposDePulsacion[17]

        #Tiempos de pulsacion de la i
        tiempoTotal += self.tiemposDePulsacion[7] + self.tiemposDePulsacion[14]

        return tiempoTotal / 11


    def getTiempoMedioDePulsacionDeLasTeclasDeLaSegundaFila(self):
        tiempoTotal = 0.0
        
        #Tiempos de pulsacion de la s
        tiempoTotal += self.tiemposDePulsacion[3] + self.tiemposDePulsacion[8] + self.tiemposDePulsacion[11] + self.tiemposDePulsacion[18]

        #Tiempos de pulsacion de la g
        tiempoTotal += self.tiemposDePulsacion[15]

        return tiempoTotal / 5


    #Tiempos de vuelo
    def getTiemposDeVueloEnTupla(self):
        tupla = ()
        tupla = tupla + (self.getTiempoMedioDeVueloDeTaR(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeRaE(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeEaS(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeSaEspacio(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeEspacioaT(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeRaI(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeIaS(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeSaT(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeTaE(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeTaI(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeIaG(), )
        tupla = tupla + (self.getTiempoMedioDeVueloDeGaR(), )

        return tupla

    def getTiempoMedioDeVueloDeTaR(self):
        return (self.tiemposDeVuelo[0] + self.tiemposDeVuelo[5]) / 2

    def getTiempoMedioDeVueloDeEaS(self):
        return (self.tiemposDeVuelo[2] + self.tiemposDeVuelo[10] + self.tiemposDeVuelo[17]) / 3

    def getTiempoMedioDeVueloDeRaE(self):
        return (self.tiemposDeVuelo[1] + self.tiemposDeVuelo[16]) / 2

    def getTiempoMedioDeVueloDeSaEspacio(self):
        return (self.tiemposDeVuelo[1] + self.tiemposDeVuelo[16]) / 2

    def getTiempoMedioDeVueloDeEspacioaT(self):
        return (self.tiemposDeVuelo[4] + self.tiemposDeVuelo[12]) / 2

    def getTiempoMedioDeVueloDeRaI(self):
        return self.tiemposDeVuelo[6]

    def getTiempoMedioDeVueloDeIaS(self):
        return self.tiemposDeVuelo[7]

    def getTiempoMedioDeVueloDeSaT(self):
        return self.tiemposDeVuelo[8]

    def getTiempoMedioDeVueloDeTaE(self):
        return self.tiemposDeVuelo[9]

    def getTiempoMedioDeVueloDeTaI(self):
        return self.tiemposDeVuelo[13]

    def getTiempoMedioDeVueloDeIaG(self):
        return self.tiemposDeVuelo[14]

    def getTiempoMedioDeVueloDeGaR(self):
        return self.tiemposDeVuelo[15]

    def getTiempoMedioDeVueloDeRaE(self):
        return self.tiemposDeVuelo[16]
    
    #Tiempos de pulsacion
    def getTiemposDePulsacionEnTupla(self):
        tupla = ()
        tupla += (self.getTiempoMedioDePulsacionDeLaT(), )
        tupla += (self.getTiempoMedioDePulsacionDeLaR(), )
        tupla += (self.getTiempoMedioDePulsacionDeLaE(), ) 
        tupla += (self.getTiempoMedioDePulsacionDeLaS(), )
        tupla += (self.getTiempoMedioDePulsacionDeLaI(), )
        tupla += (self.getTiempoMedioDePulsacionDelEspacio(), )
        tupla += (self.getTiempoMedioDePulsacionDeLaG(), )

        return tupla

    def getTiempoMedioDePulsacionDeLaT(self):
        tiempoTotal = 0.0
        tiempoTotal += self.tiemposDePulsacion[0] + self.tiemposDePulsacion[5] + self.tiemposDePulsacion[9] + self.tiemposDePulsacion[13]
        return tiempoTotal / 4

    def getTiempoMedioDePulsacionDeLaR(self):
        tiempoTotal = 0.0
        tiempoTotal += self.tiemposDePulsacion[1] + self.tiemposDePulsacion[16]
        return tiempoTotal / 2

    def getTiempoMedioDePulsacionDeLaE(self):
        tiempoTotal = 0.0
        tiempoTotal += self.tiemposDePulsacion[2] + self.tiemposDePulsacion[10] + self.tiemposDePulsacion[17]
        return tiempoTotal / 3

    def getTiempoMedioDePulsacionDeLaS(self):
        tiempoTotal = 0.0
        tiempoTotal += self.tiemposDePulsacion[3] + self.tiemposDePulsacion[8] + self.tiemposDePulsacion[11] + self.tiemposDePulsacion[18]
        return tiempoTotal / 4

    def getTiempoMedioDePulsacionDeLaI(self):
        tiempoTotal = 0.0
        tiempoTotal += self.tiemposDePulsacion[7] + self.tiemposDePulsacion[14]
        return tiempoTotal / 2

    def getTiempoMedioDePulsacionDelEspacio(self):
        tiempoTotal = 0.0
        tiempoTotal += self.tiemposDePulsacion[4] + self.tiemposDePulsacion[12]
        return tiempoTotal / 2

    def getTiempoMedioDePulsacionDeLaG(self):
        return self.tiemposDePulsacion[15]

    
