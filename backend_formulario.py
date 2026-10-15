from flask import request, render_template, abort

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    address = request.form.get('address', '').strip()
    date = request.form.get('date', '').strip()
    if not all((name, email, address, date)):
        abort(400, 'Faltan campos obligatorios')
    from pathlib import Path
    with Path(app.root_path, 'form.txt').open('a', encoding='utf-8') as f:
        for label, value in [('Nombre', name), ('Email', email), ('Direccion', address), ('Fecha', date)]:
            f.write(label + ': ' + value.replace('\n', ' ').replace('\r', ' ') + '\n')
        f.write('---\n')
    return render_template('form_result.html', name=name, email=email, address=address, date=date)

