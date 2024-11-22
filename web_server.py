import sqlite3
from flask import Flask,render_template,request,redirect,url_for,session
import os

app = Flask(__name__)
app.config['DATABASE'] = 'autos.db'
app.secret_key = 'your_secret_key'

def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_auto TEXT NOT NULL,
                precio_auto TEXT NOT NULL,
                nombre_usuario TEXT NOT NULL,
                email_usuario TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    conn.commit()


diretorio= 'img'

@app.route('/')
def index():
    autos = [
        {
            'nombre': 'Lamborghini Huracan',
            'imagen': 'Lamborghini_Huracan.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

        {
            'nombre': 'Lamborghini Veneno',
            'imagen': 'Lamborghini_Veneno.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

        {
            'nombre': 'Lamborghini Urus',
            'imagen': 'Lamborghini_Urus.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

        {
            'nombre': 'Lamborghini',
            'imagen': 'Lamborghini.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

        {
            'nombre': 'Lamborghini Huracan Performante',
            'imagen': 'Lamborghini_Huracan_Performante.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

        {
            'nombre': 'Lamborghini Veneno Spider',
            'imagen': 'Lamborghini_Veneno_Spider.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

        {
            'nombre': 'Lamborghini Diablo',
            'imagen': 'Lamborghini_Diablo.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

        {
            'nombre': 'Lamborghini Centenario',
            'imagen': 'Lamborghini_Centenario.jpg',
            'descripcion': 'Increíble automóvil deportivo con un motor poderoso y un diseño elegante.',
            'precio': '$250,000'
        },

      ]

    return render_template("index.html", autos=autos)

@app.route('/iniciar')
def iniciar():
    return render_template('iniciar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect('autos.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            
            if user:
                session['user_id'] = user[0] 
                session.pop('guest', None)
                return redirect(url_for('index', action='existente'))
            else:
                error = 'Credenciales incorrectas. Inténtalo de nuevo.'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error = 'Nombre de usuario y contraseña son obligatorios.'
            return render_template('register.html', error=error)

        with sqlite3.connect('autos.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        return redirect(url_for('index', action='registrado'))
    else:
        return render_template('register.html')


@app.route('/guest')
def guest():
    session['guest'] = True
    return redirect(url_for('index', action='invitado'))


@app.route('/comprar', methods=['POST'])
def comprar():
    if 'user_id' not in session and 'guest' not in session:
        return redirect(url_for('iniciar'))
    
    if request.method == 'POST':
        nombre_auto = request.form.get('nombre_auto')
        precio_auto = request.form.get('precio_auto')
        nombre_usuario = request.form.get('nombre')
        email_usuario = request.form.get('email')

        if not nombre_usuario or not email_usuario:
            return "Por favor, proporcione su nombre y correo electrónico para completar la compra."
            
        if 'guest' in session:
            return "Debe iniciar sesión con una cuenta existente o registrarse para poder comprar .<a href='/iniciar'>Ir</a>"

        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO compras (nombre_auto, precio_auto, nombre_usuario, email_usuario)
                VALUES (?, ?, ?, ?)
            ''', (nombre_auto, precio_auto, nombre_usuario, email_usuario))
            conn.commit()

        return f"¡Gracias por tu compra, {nombre_usuario}! Has comprado el {nombre_auto} por {precio_auto}."

@app.route('/auto/<nombre>')
def auto(nombre):
    imagen = nombre.lower().replace(' ', '_') + '.jpg'
    detalles_auto = {
        'nombre': nombre,
        'imagen': imagen,
        'descripcion': 'El Lamborghini Huracán Performante es un automóvil deportivo de alto rendimiento producido por el fabricante italiano Lamborghini. Es una versión mejorada del Lamborghini Huracán estándar, con características adicionales diseñadas para mejorar el rendimiento y la experiencia de conducción.',
        'precio': '$250,000'
    }
    return render_template('auto.html', auto=detalles_auto)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

 
