from flask import Flask, render_template, request, make_response
from random import randint
from time import time

import datetime
import sklearn
from sklearn.externals import joblib

from TypingPersonality import TypingPersonality

app = Flask(__name__)

@app.route("/")
def formulario():
  return render_template("formulario.html")


@app.route("/sentenceTyped", methods=['POST'])
def formularioRellenado():
  nombre = request.form['nombre']
  tiempoMedioPulsacion = float(request.form['tiempoMedioDePulsacionPorTeclaForm'])
  tiempoMedioVuelo = float(request.form['tiempoMedioDeVueloForm'])
  tiempoEnTeclearLaFrase = float(request.form['tiempoTranscurridoParaTeclearLaFraseForm'])
  numeroDeFallos = int(request.form['numeroDeFallosForm'])

  if (nombre == "Sergio"):
    typingPersonality = TypingPersonality(1, tiempoMedioPulsacion, tiempoMedioVuelo, tiempoEnTeclearLaFrase)
  else: 
    typingPersonality = TypingPersonality(0, tiempoMedioPulsacion, tiempoMedioVuelo, tiempoEnTeclearLaFrase)
    
  typingPersonality.save() 

  return render_template("formulario.html")
  
  

app.debug = True

if __name__ == "__main__":
    app.run()