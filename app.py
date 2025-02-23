from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)

# Ініціалізація бази даних
def init_db():
    with sqlite3.connect("ip_logs.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          ip TEXT,
                          timestamp TEXT)''')
        conn.commit()

@app.route('/')
def home():
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Збереження IP у базу даних
    with sqlite3.connect("ip_logs.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (ip, timestamp) VALUES (?, ?)", (ip, timestamp))
        conn.commit()

    return render_template('index.html', ip=ip)

@app.route('/logs')
def view_logs():
    with sqlite3.connect("ip_logs.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs")
        data = cursor.fetchall()
    
    return render_template('logs.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
