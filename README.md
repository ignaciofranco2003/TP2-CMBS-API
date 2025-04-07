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

Config DB:
     
modificar los valores de:
     
     conn = mysql.connector.connect(
         host='localhost',
         user='root',
         password='1234'
     )
Por los valores de nuestro usuario y pass, si es necesrio el del host, de alguna base de datos MySQL.

La DB se crea de manera automatica cuando iniciamos el archivo .py
