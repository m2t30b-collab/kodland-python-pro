from random import choice
from flask import Flask

app = Flask(__name__)
facts_list = [
    'Silenciar notificaciones ayuda a concentrarse en una sola tarea.',
    'Alternar las pantallas con actividades al aire libre permite descansar.',
    'Puedes reservar momentos del día para revisar mensajes.',
    'Las herramientas digitales son útiles cuando las usamos con un propósito.',
]

def page(title, content):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{title}</title><style>body{{font:18px system-ui;max-width:760px;
    margin:60px auto;padding:24px;background:#eef2ff;color:#17244d}}
    a{{color:#254ec9}}nav{{display:flex;gap:24px;flex-wrap:wrap}}
    main{{background:white;padding:32px;border-radius:20px}}</style></head>
    <body><nav><a href="/">Inicio</a><a href="/random_fact">Dato aleatorio</a>
    <a href="/secret">Sorpresa</a></nav><main><h1>{title}</h1>{content}</main></body></html>'''

@app.route('/')
def home():
    return page('Tecnología con equilibrio', '<p>Pequeñas ideas para usar mejor la tecnología.</p><a href="/random_fact">¡Ver un dato aleatorio!</a>')

@app.route('/random_fact')
def random_fact():
    return page('Un dato para recordar', f'<p>{choice(facts_list)}</p><a href="/random_fact">Ver otro dato</a>')

@app.route('/secret')
def secret():
    return page('¡Lanzamiento de moneda!', f'<p>Resultado: <strong>{choice(["Cara", "Cruz"])}</strong></p><a href="/secret">Lanzar otra vez</a>')

if __name__ == '__main__':
    app.run(debug=True)
