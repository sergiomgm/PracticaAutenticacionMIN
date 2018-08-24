from flask import Flask, render_template, request, make_response
from random import randint
from time import time

import datetime
import sklearn
from sklearn.externals import joblib

from TypingPattern import TypingPattern
from Usuario import Usuario

app = Flask(__name__)

@app.route("/")
def formulario():
  return render_template("formulario.html")

@app.route("/sentenceTyped", methods=['POST'])
def formularioRellenado():
  nombre = request.form['nombre']
  tiemposDeVuelo = [float(tiempo) for tiempo in (x.strip() for x in request.form['tiemposDeVueloForm'].split(','))]
  tiemposPulsacionesTeclas = [float(tiempo) for tiempo in (x.strip() for x in request.form['tiemposPulsacionesTeclasForm'].split(','))]
  tiempoEnTeclearLaFrase = float(request.form['tiempoTranscurridoParaTeclearLaFraseForm'])

  target = Usuario.Sergio.value if nombre.upper() == "SERGIO" else Usuario.Otro.value
  typingPattern = TypingPattern(target, tiemposPulsacionesTeclas, tiemposDeVuelo, tiempoEnTeclearLaFrase)
  
  typingPattern.save()

  clf = joblib.load('clf.pkl')
  typingPattern.predict(clf)

  template = "submitCorrecto.html" if typingPattern.prediction == Usuario.Sergio.value else "submitNoSergio.html"
  
  return render_template(template) 

app.debug = True

if __name__ == "__main__":
    app.run()