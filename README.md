Iniciar un entorno

     py -m venv .venv
  
    .venv\Scripts\activate

Instalar las librerias:

     pip install -r req.txt

Iniciar la api desde una consola:

     py api.py

Endpoints disponibles:

     http://127.0.0.1:5000/linterna GET ---> Devuelve todos los registros de la db
     http://127.0.0.1:5000/linterna POST --> con el json {"estado": "encendida/apagada"} registramos un nuevo estado
