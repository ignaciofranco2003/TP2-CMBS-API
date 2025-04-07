from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime,timedelta, date

app = Flask(__name__)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234'
)
cursor = conn.cursor()

def init_db():
    cursor.execute('''CREATE DATABASE IF NOT EXISTS linterna_db''')

    conn.database = 'linterna_db'

    cursor.execute('''CREATE TABLE IF NOT EXISTS linterna_eventos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        estado VARCHAR(10) NOT NULL,
                        inicio DATETIME NOT NULL,
                        fin DATETIME,
                        duracion_segundos INT
                    )''')
    conn.commit()

@app.route('/linterna', methods=['POST'])
def cambiar_estado():
    data = request.get_json()
    estado = data.get('estado')
    timestamp = data.get('timestamp')

    if estado not in ['encendida', 'apagada']:
        return jsonify({'error': 'Estado invalido'}), 400

    try:
        fecha = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return jsonify({'error': 'Formato de timestamp invalido. Usa YYYY-MM-DD HH:MM:SS'}), 400

    # Obtener el ultimo evento abierto (sin fin)
    cursor.execute('''
        SELECT id, estado, inicio FROM linterna_eventos
        WHERE fin IS NULL
        ORDER BY inicio DESC LIMIT 1
    ''')
    ultimo = cursor.fetchone()

    if ultimo:
        id_evento, estado_anterior, inicio = ultimo

        if estado_anterior != estado:
            duracion = (fecha - inicio).total_seconds()
            cursor.execute('''
                UPDATE linterna_eventos
                SET fin = %s, duracion_segundos = %s
                WHERE id = %s
            ''', (fecha, duracion, id_evento))
        else:
            # Si es el mismo estado, ignoramos
            return jsonify({'message': 'Estado repetido, sin cambios'}), 200

    # Insertar nuevo evento
    cursor.execute('''
        INSERT INTO linterna_eventos (estado, inicio)
        VALUES (%s, %s)
    ''', (estado, fecha))

    conn.commit()
    return jsonify({'message': 'Estado actualizado'}), 201

@app.route('/linterna', methods=['GET'])
def obtener_estados():

    cursor.execute('SELECT estado, timestamp FROM linterna')
    registros = cursor.fetchall()
    conn.commit()

    if registros:
        return jsonify([{'estado': estado, 'timestamp': timestamp} for estado, timestamp in registros]), 200
    else:
        return '', 204

@app.route('/linterna/tiempo_encendida', methods=['GET'])
def tiempo_encendida():
    segundos = obtener_duracion_por_estado('encendida')
    minutos = round(segundos / 60, 2)
    return jsonify({'tiempo_encendida': f"{minutos} minutos"}), 200

@app.route('/linterna/tiempo_apagada', methods=['GET'])
def tiempo_apagada():
    segundos = obtener_duracion_por_estado('apagada')
    minutos = round(segundos / 60, 2)
    return jsonify({'tiempo_apagada': f"{minutos} minutos"}), 200

def obtener_duracion_por_estado(estado_buscado):
    hoy = date.today()
    inicio_dia = datetime.combine(hoy, datetime.min.time())
    fin_dia = datetime.combine(hoy, datetime.max.time())

    cursor.execute('''
        SELECT duracion_segundos FROM linterna_eventos
        WHERE estado = %s AND inicio BETWEEN %s AND %s AND duracion_segundos IS NOT NULL
    ''', (estado_buscado, inicio_dia, fin_dia))

    eventos = cursor.fetchall()

    total_segundos = sum(duracion for (duracion,) in eventos)
    return total_segundos

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)

