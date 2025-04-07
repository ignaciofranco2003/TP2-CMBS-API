Iniciar un entorno

     py -m venv .venv
  
    .venv\Scripts\activate

Instalar las librerias:

     pip install -r req.txt

Iniciar la api desde una consola:

     py api.py

Endpoints disponibles:

     http://IP:5000/linterna GET ---> Devuelve todos los registros de la db

     http://IP:5000/linterna POST --> con el json {"estado": "encendida/apagada"} registramos un nuevo estado

     http://IP:5000/linterna/tiempo_apagada GET --> Devuelve el tiempo que el sensor recibe mas de la luz minima (linterna apagada)
                                                    o habia algo delante, en minutos.

     http://IP:5000/linterna/tiempo_encendida GET -> Devuelve el tiempo que el sensor recibe menos de la luz minima (linterna encendida)
                                                     o si no habia nada adelante, en minutos.

Config DB:
     
modificar los valores de:
     
     conn = mysql.connector.connect(
         host='localhost',
         user='root',
         password='1234'
     )

Por los valores de nuestro usuario y pass, si es necesrio el del host, de alguna base de datos MySQL.

La DB se crea de manera automatica cuando iniciamos el archivo .py
