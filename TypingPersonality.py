from pymongo.mongo_client import MongoClient

class TypingPersonality():
    tiempoMedioDePulsacionPorTeclaEnMilisegundos = 0
    tiempoMedioDeVueloEnMilisegundos = 0
    tiempoQueTardaEnTeclearLaFrase = 0
    numeroDeFallos = 0
    target = 0 #1 si soy yo y 0 si es cualquier otra persona
    prediction = 0

    def __init__(self, target=0, tiempoMedioDePulsacionPorTeclaEnMilisegundos=0, tiempoMedioDeVueloEnMilisegundos=0, tiempoQueTardaEnTeclearLaFrase=0, numeroDeFallos=0):
        self.target = target
        self.tiempoMedioDePulsacionPorTeclaEnMilisegundos = tiempoMedioDePulsacionPorTeclaEnMilisegundos
        self.tiempoMedioDeVueloEnMilisegundos = tiempoMedioDeVueloEnMilisegundos
        self.tiempoQueTardaEnTeclearLaFrase = tiempoQueTardaEnTeclearLaFrase
        self.numeroDeFallos = numeroDeFallos

    def predict(self, model):
        self.prediction = model.predict([self.toTuple()[:-1]])[0]
    
    def toTuple(self):
        return (self.tiempoMedioDePulsacionPorTeclaEnMilisegundos, self.tiempoMedioDeVueloEnMilisegundos, 
            self.tiempoQueTardaEnTeclearLaFrase, self.numeroDeFallos, self.target)   
    
    def save(self):
        typingPersonality = {
        "tiempoMedioDePulsacionPorTeclaEnMilisegundos": self.tiempoMedioDePulsacionPorTeclaEnMilisegundos,
        "tiempoMedioDeVueloEnMilisegundos": self.tiempoMedioDeVueloEnMilisegundos,
        "tiempoQueTardaEnTeclearLaFrase": self.tiempoQueTardaEnTeclearLaFrase,
        "numeroDeFallos" : self.numeroDeFallos,
        "target": self.target
        }

        client = MongoClient('localhost', 27017)
        db = client['myDB']
        collection = db["autenticacion"]
        collection.insert(typingPersonality)