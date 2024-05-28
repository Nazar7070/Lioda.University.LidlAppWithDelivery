import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if the username and password match
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return 'Username already exists. Please choose a different one.'

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()

        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

# Your email sending function
def send_email(receiver_email):
    sender_email = 'nastyalioda@gmail.com'
    password = '24123051Nl'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Welcome to Our Platform!'

    body = """
    <html>
        <body>
            <h1>Welcome to Our Platform!</h1>
            <p>Thank you for joining us.</p>
        </body>
    </html>
    """
    message.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

@app.route('/send-email')
def send_welcome_email():
    receiver_email = 'nastyalioda@example.com'  # Replace with the recipient's email
    send_email(receiver_email)
    return 'Email sent successfully!'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
