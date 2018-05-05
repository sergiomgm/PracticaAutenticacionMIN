import pandas as pd
from sklearn import linear_model
from sklearn import ensemble
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
import time
from TypingPersonality import TypingPersonality

nObservations = 0
from pymongo.mongo_client import MongoClient

client = MongoClient('localhost', 27017)
db = client['myDB']
collection = db["autenticacion"]

def train():
  global nObservations

  records = []
  for t in collection.find({}):
      typingPersonality = TypingPersonality()
      typingPersonality.tiempoMedioDePulsacionPorTeclaEnMilisegundos = t["tiempoMedioDePulsacionPorTeclaEnMilisegundos"]
      typingPersonality.tiempoMedioDeVueloEnMilisegundos = t["tiempoMedioDeVueloEnMilisegundos"]
      typingPersonality.tiempoQueTardaEnTeclearLaFrase = t["tiempoQueTardaEnTeclearLaFrase"]
      typingPersonality.numeroDeFallos = t["numeroDeFallos"]
      typingPersonality.target = t["target"]
      records.append(typingPersonality.toTuple())

  features = ["tiempoMedioDePulsacionPorTeclaEnMilisegundos", "tiempoMedioDeVueloEnMilisegundos", "tiempoQueTardaEnTeclearLaFrase", "numeroDeFallos"]
  target = "target"

  labels =  features + [target]
  df = pd.DataFrame.from_records(records, columns = labels)
  print ("Before filtering ", df.shape)


  #Eliminar las observaciones que no esten en un intervalo alrededor de las medias correspondientes para Sergio
  dfSergio = df[df.target  == 1]
  dfNoSergio = df[df.target == 0] 

  mediaTiempoPulsacion = dfSergio["tiempoMedioDePulsacionPorTeclaEnMilisegundos"].mean()
  mediaTiempoDeVuelo = dfSergio["tiempoMedioDeVueloEnMilisegundos"].mean()
  mediaTiempoTotal = dfSergio["tiempoQueTardaEnTeclearLaFrase"].mean()

  dfSergio = dfSergio[dfSergio.tiempoMedioDePulsacionPorTeclaEnMilisegundos <= (2.5*mediaTiempoPulsacion)]
  dfSergio = dfSergio[dfSergio.tiempoMedioDePulsacionPorTeclaEnMilisegundos >= (0.4*mediaTiempoPulsacion)]

  dfSergio = dfSergio[dfSergio.tiempoMedioDeVueloEnMilisegundos <= (2.5*mediaTiempoDeVuelo)]
  dfSergio = dfSergio[dfSergio.tiempoMedioDeVueloEnMilisegundos >= (0.4*mediaTiempoDeVuelo)]

  dfSergio = dfSergio[dfSergio.tiempoQueTardaEnTeclearLaFrase <= (2.5*mediaTiempoTotal)]
  dfSergio = dfSergio[dfSergio.tiempoQueTardaEnTeclearLaFrase >= (0.4*mediaTiempoTotal)]

  df = pd.concat([dfSergio, dfNoSergio])

  print ("After filtering ", df.shape)

  if df.shape[0] <= nObservations:
    return

  nObservations = df.shape[0]

  clf = ensemble.RandomForestClassifier(n_estimators=100)


  X = df[features]
  y = df[target]
  clf = clf.fit(X, y)
  scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
  print("Accuracy: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std()))

  prediction = clf.predict(X)
  
  joblib.dump(clf, 'clf.pkl',  protocol=2)
  print("DUMP")
  return df.shape[0]

while True:
  train()
  time.sleep(3)

