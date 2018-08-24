  var tiempoPulsacionTecla = 0;
  var tiemposPulsacionesTeclas = [];
 
  var timeStampAlPulsarLaTecla = 0;
  var timeStampAlSoltarLaTeclaActual = 0;
  var timeStampAlSoltarLaTeclaAnterior = 0;
  
  var tiempoDeVuelo = 0;
  var tiemposDeVuelo = [];
  var tiempoTranscurridoParaTeclearLaFrase = 0;
  var timeStampInicial = 0;
  var timeStampTeclaAnterior = 0;
  
  //Estos números corresponden al número del evento que se dispara al pulsar
  //cada tecla, ordenados igual que la frase "Tres tristes tigres"
  var eventosPorTecla = [84, 82, 69, 83, 32, 84, 82, 73, 83, 84, 69, 83, 32, 84, 73, 71, 82, 69, 83];
  var numeroDeTeclasPulsadas = 0;
  var numeroDeTeclasSoltadas = 0;
  var actualizarTiempoTranscurrido;

  var i = 0;

  $( "#password" ).keypress(function( event ) {
    //Si la tecla pulsada es enter y se han pulsado y soltado previamente todas las teclas
    //Es necesario poner teclas soltadas porque si se pulsa enter sin haber soltado la 
    //última s el último tiempo de pulsación no se mandaba a través del servidor
    if ( event.which == 13 && numeroDeTeclasPulsadas == "Tres tristes tigres".length && numeroDeTeclasSoltadas == "Tres tristes tigres".length ) { 
      event.preventDefault();
      tiempoTranscurridoParaTeclearLaFrase = event.timeStamp - timeStampInicial;

      //Para que la función que se invoca al pulsar submit pueda hacer request.form
      $("#tiemposDeVueloForm").val(tiemposDeVuelo);
      $("#tiemposPulsacionesTeclasForm").val(tiemposPulsacionesTeclas);
      $("#tiempoTranscurridoParaTeclearLaFraseForm").val(tiempoTranscurridoParaTeclearLaFrase);
    
      //Para mostrar los datos por pantalla
      document.getElementById("tiempoTranscurrido").innerHTML = parseInt(tiempoTranscurridoParaTeclearLaFrase) + " ms";
      
      $("#password").val("");
      clearInterval(actualizarTiempoTranscurrido);
      document.getElementById("submitButton").disabled = false;

    } else if (event.which == eventosPorTecla[numeroDeTeclasPulsadas]) {

      timeStampAlPulsarLaTecla = event.timeStamp;
      tiempoDeVuelo = event.timeStamp - timeStampTeclaAnterior;

      if (numeroDeTeclasPulsadas == 0) {
        timeStampInicial = event.timeStamp;
        timeStampTeclaAnterior = event.timeStamp;
        initialTime = new Date().getTime();
        actualizarTiempoTranscurrido = setInterval(func, 1);
      } else {
        tiemposDeVuelo.push(tiempoDeVuelo);
      }

      document.getElementById(numeroDeTeclasPulsadas).style.color ="green";
      
      timeStampAlPulsarLaTecla = event.timeStamp;
      tiempoDeVuelo = event.timeStamp - timeStampAlSoltarLaTeclaAnterior;
      
      timeStampTeclaAnterior = event.timeStamp;
      
      document.getElementById("tiempoDeVuelo").innerHTML = parseInt(tiempoDeVuelo) + " ms"; 

      numeroDeTeclasPulsadas += 1;   
    }
  });

  $( "#password" ).keyup(function( event ) {
    if ( event.which == 13 ) { 
      event.preventDefault();
    } else if (event.which == eventosPorTecla[numeroDeTeclasSoltadas]) {

      timeStampAlSoltarLaTeclaActual = event.timeStamp;
      timeStampAlSoltarLaTeclaAnterior = event.timeStamp;
      tiempoPulsacionTecla = timeStampAlSoltarLaTeclaActual - timeStampAlPulsarLaTecla;

      tiemposPulsacionesTeclas.push(tiempoPulsacionTecla);   
      
      document.getElementById("duracionPulsacion").innerHTML = parseInt(tiempoPulsacionTecla) + " ms";   
      ++numeroDeTeclasSoltadas;
    }
  });
  
  var initialTime;
  var func = function() {
    document.getElementById("tiempoTranscurrido").innerHTML = new Date().getTime() - initialTime + " s";
  }
  