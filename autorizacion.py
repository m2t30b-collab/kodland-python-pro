from flask import request, session, redirect, render_template

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_login = request.form.get('email', '')
        form_password = request.form.get('password', '')
        users_db = User.query.all()
        for user in users_db:
            if form_login == user.email and form_password == user.password:
                session.clear()
                session['user_email'] = user.email
                return redirect('/index')
        error = 'Nombre de usuario o contraseña incorrectos'
        return render_template('login.html', error=error)
    return render_template('login.html')
