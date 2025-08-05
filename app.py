from flask import Flask, request, render_template_string
import os
import sqlite3

app = Flask(__name__)

# Vulnerability 1: Server-Side Template Injection (SSTI)
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    template = f"Hello, {name}!"
    return render_template_string(template)

# Vulnerability 2: Command Injection
@app.route('/ping', methods=['POST'])
def ping():
    ip = request.form.get('ip')
    response = os.popen(f"ping -c 1 {ip}").read()
    return f"<pre>{response}</pre>"

# Vulnerability 3: SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    if user:
        return "Login successful"
    else:
        return "Invalid credentials"

# Vulnerability 4: Hardcoded Secret
API_KEY = "SECRET-1234567890"

@app.route('/')
def index():
    return "Welcome to the vulnerable Flask app!"

if __name__ == '__main__':
    app.run(debug=True)
