from flask import Flask, request, session, redirect, url_for, make_response
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

users = {"alice": {"password": "qwerty", "balance": 1000}}

@app.route('/')
def home():
    return 'Добро пожаловать! <a href="/login">Войти</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) and users[username]['password'] == password:
            session['user'] = username
            response = make_response(redirect(url_for('transfer')))
            response.set_cookie('session', samesite='Strict', secure=True)
            return response
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Логин">
            <input type="password" name="password" placeholder="Пароль">
            <button type="submit">Войти</button>
        </form>
    '''

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = int(request.form['amount'])
        users[session['user']]['balance'] -= amount
        return f"Перевод успешен! Новый баланс: {users[session['user']]['balance']}"
    
    return '''
        <form method="post">
            <input type="number" name="amount" placeholder="Сумма">
            <button type="submit">Перевести</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
