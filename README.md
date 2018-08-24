# Práctica Minería de datos
La práctica consiste en hacer una aplicación web que aprenda el patrón de escritura de un usuario y permita el acceso únicamente a ese usuario.
Para ello en el campo contraseña se escribirá la frase **TRES TRISTES TIGRES**, cuántas más veces lo escriba el usuario mejor funcionará el algoritmo.

# Ejecución


### Instalación del entorno
Para no tener que realizar muchas instalaciones es conveniente instalar un entorno virtual e instalar los paquetes necesarios en él. PAra instalr el entorno virtual:

1. Instalar python

```
sudo easy_intall pip
```

2. Instalar entrono virtual

```
virtualenv env
```

3. Iniciar entrono virtual

```
source env/bin/activate
```

### Ejecución de la aplicación
Una vez instalado el entorno virtual ya se puede ejecutar la palicación ejecutando los siguientes comandos:

1. Ejecutar el servidor de mongo

```
mongod
```

2. Lanzar la aplicación para que se inicie el servidor, para ello situarse en el directorio donde est´ñe el fichero index.py

```
python index.py
```

3. Ejecutar el modelo para que se entrene cuando se generen nuevos datos en la base de datos.

```
python model.py
```

4. Abrir el navegador en la IP indicada en el paso 2.