from flask import Flask, request, jsonify
import mysql.connector

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

    cursor.execute('''CREATE TABLE IF NOT EXISTS linterna (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        estado VARCHAR(10) NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()

@app.route('/linterna', methods=['POST'])
def cambiar_estado():

    data = request.get_json()
    estado = data.get('estado')

    if estado not in ['encendida', 'apagada']:
        return jsonify({'error': 'Estado invalido'}), 400

    cursor.execute(f'INSERT INTO linterna (estado) VALUES ("{estado}")')
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)

