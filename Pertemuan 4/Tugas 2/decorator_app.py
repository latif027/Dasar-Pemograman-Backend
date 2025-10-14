from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = '12345'

def login_required(f):
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '123':
        session['user'] = username
        return redirect(url_for('dashboard'))
    return "<h3>Login gagal, coba lagi!</h3><a href='/'>Kembali</a>"

@app.route('/dashboard')
@login_required
def dashboard():
    user = session['user']
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
