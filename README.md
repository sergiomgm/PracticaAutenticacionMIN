# Práctica Minería de datos

[![CircleCI](https://circleci.com/gh/sergiomgm/PracticaAutenticacionMIN.svg?style=svg&circle-token=7e227970d2fd3e37e559ae104988caf59b935933)](https://circleci.com/gh/sergiomgm/PracticaAutenticacionMIN)


La práctica consiste en hacer una aplicación web que aprenda el patrón de escritura de un usuario y permita el acceso únicamente a ese usuario.
Para ello en el campo contraseña se escribirá la frase **TRES TRISTES TIGRES**, cuántas más veces lo escriba el usuario mejor funcionará el algoritmo.

# Ejecución


### Instalación del entorno
Para no instalar todos los paquetes de python en el ordenador es conveniente instalar un entorno virtual para ejecutar la aplicación. **Los pasos descritos a continuación sólo es necesario reallizarlos la primera vez que se ejecute la aplicación en caso de no tener el entorno virtual instalado previamente:**

1. Instalar python

```
sudo easy_intall pip
```

2. Instalar entorno virtual

```
virtualenv env
```



### Ejecución de la aplicación
Una vez instalado el entorno virtual ya se puede ejecutar la aplicación ejecutando los siguientes comandos:

1. Ejecutar el servidor de mongo

```
mongod
```

2. Iniciar entorno virtual

```
source env/bin/activate
```

3. Lanzar la aplicación para que se inicie el servidor, para ello situarse en el directorio donde esté el fichero index.py

```
python index.py
```

4. Ejecutar el modelo para que se entrene cuando se generen nuevos datos en la base de datos.

```
python model.py
```

5. Abrir el navegador en la IP indicada en el paso 3.
