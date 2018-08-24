import pandas as pd

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

import numpy as np


from sklearn import linear_model

from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
import time
from TypingPattern import TypingPattern
from pymongo.mongo_client import MongoClient

nObservations = 0

client = MongoClient('localhost', 27017)
db = client['myDB']
collection = db["autenticacion"]

def train():
  global nObservations
  j = 0
  records = []
  
  for t in collection.find({}):
    try:
      typingPattern = TypingPattern()
      j = j + 1
      typingPattern.tiemposDeVuelo = [float(i) for i in t["tiemposDeVuelo"]]
      typingPattern.tiemposDePulsacion = [float(i) for i in t["tiemposDePulsacion"]]
      typingPattern.tiempoQueTardaEnTeclearLaFrase = float(t["tiempoQueTardaEnTeclearLaFrase"])
      typingPattern.target = int(t["target"])
      records.append(typingPattern.toTuple())
    except ValueError,e:
      print "error : ",e, " element ", j

  features = ["tiempoMedioDePulsacionDeLasTeclasDeLaPrimeraFila", "tiempoMedioDePulsacionDeLasTeclasDeLaSegundaFila", 
              "tiempoMedioPulsacionDeLaT", "tiempoMedioPulsacionDeLaR", "tiempoMedioPulsacionDeLaE", "tiempoMedioPulsacionDeLaS", 
              "tiempoMedioPulsacionDeLaI", "tiempoMedioPulsacionDelEspacio", "tiempoMedioPulsacionDeLaG", 
              "tiempoDeVueloDeTaR", "tiempoDeVueloDeRaE", "tiempoDeVueloDeEaS", "tiempoDeVueloDeSaEspacio",
              "tiempoDeVueloDeEspacioaT", "tiempoDeVueloDeRaI", "tiempoDeVueloDeIaS", "tiempoDeVueloDeSaT",
              "tiempoDeVueloDeTaE", "tiempoDeVueloDeTaI", "tiempoDeVueloDeIaG", "tiempoDeVueloDeGaR",
              "tiempoQueTardaEnTeclearLaFrase", "varianzaDeLosTiemposDePulsacion"]
  target = "target"

  labels =  features + [target]
  df = pd.DataFrame.from_records(records, columns = labels)
  print ("Before filtering ", df.shape[0])

  #Eliminar outliers

  #Si el tiempo de vuelo o el tiempo de pulsacion
  #son demasiado elevados es porque ha habido algun error
  #al medirlos y esa observacion no es util 
  for feature in features:
    if "tiempoDeVuelo" in feature:
        df = df[df[feature] <= 600]
    elif "tiempoMedioDePulsacion" in feature:
        df = df[df[feature] <= 300]
        
  #Si el usuario se ha quedado esperando demasiado tiempo
  #para completar la frase no es una buena medida
  #del tiempo que ha tardado en escribirla
  df = df[df.tiempoQueTardaEnTeclearLaFrase <= 10000]
  

  print ("After filtering ", df.shape[0])

  if df.shape[0] <= nObservations:
    return

  nObservations = df.shape[0]

  clasificadores = dict()

  clf1 = RandomForestClassifier(n_estimators=250, random_state=0)
  clf2 = AdaBoostClassifier(n_estimators=150)
  clf3 = GradientBoostingClassifier(n_estimators=91, random_state=0, learning_rate=0.2, max_depth = 4, loss='exponential', min_samples_split=20, min_samples_leaf=1)
  
  clasificadores[0] = clf1
  clasificadores[1] = clf2
  clasificadores[2] = clf3

  X = df[features]
  y = df[target]

  maximo = 0.0
  indiceDelMejorClasificador = 0

  numberOfClassifiers = len(clasificadores)

  for k in range(numberOfClassifiers):
    clf = clasificadores[k]
    clf = clf.fit(X, y)
    scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std()))
    if (scores.mean() > maximo):
      maximo = scores.mean()
      indiceDelMejorClasificador = k


  clf = clasificadores[indiceDelMejorClasificador]

  print "Most important feature: ", features[np.argmax(clf.feature_importances_)]
  print "Importance: %0.8f" % np.max(clf.feature_importances_)

  print "Less important feature: ", features[np.argmin(clf.feature_importances_)]
  print "Importance: %0.8f" % np.min(clf.feature_importances_)
    
  prediction = clf.predict(X)
  
  joblib.dump(clf, 'clf.pkl',  protocol=2)
  print("DUMP")
  return df.shape[0]

while True:
  train()
  time.sleep(3)

