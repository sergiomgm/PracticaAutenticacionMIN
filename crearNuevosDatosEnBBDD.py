from __future__ import print_function
from flask import Flask, render_template, request, make_response
from random import randint
from time import time


import sys
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
  tiemposDeVuelo = [tiempo for tiempo in (x.strip() for x in request.form['tiemposDeVueloForm'].split(','))]
  tiemposPulsacionesTeclas = [tiempo for tiempo in (x.strip() for x in request.form['tiemposPulsacionesTeclasForm'].split(','))]
  tiempoEnTeclearLaFrase = float(request.form['tiempoTranscurridoParaTeclearLaFraseForm'])

  target = Usuario.Sergio.value if nombre.upper() == "SERGIO" else Usuario.Otro.value
  typingPattern = TypingPattern(target, tiemposPulsacionesTeclas, tiemposDeVuelo, tiempoEnTeclearLaFrase)
 
  typingPattern.save() 

  return render_template("formulario.html")
  
app.debug = True

if __name__ == "__main__":
    app.run()