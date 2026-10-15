from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__)
IMAGES = {'logo.svg', 'meme_1.jpg', 'meme_2.jpg', 'codigo.svg', 'error.svg', 'exito.svg'}
COLORS = {'white', 'black', 'yellow', 'red', 'cyan', 'lime'}
def position(value):
    try:
        return str(max(0, min(500, int(str(value).removesuffix('px'))))) + 'px'
    except (TypeError, ValueError):
        return '20px'
@app.route('/', methods=['GET', 'POST'])
def index():
    selected_image = request.form.get('image-selector', 'meme_1.jpg')
    if selected_image not in IMAGES:
        selected_image = 'meme_1.jpg'
    selected_color = request.form.get('color-selector', 'white')
    if selected_color not in COLORS:
        selected_color = 'white'
    return render_template('index.html', selected_image=selected_image,
        text_top=request.form.get('textTop', ''), text_bottom=request.form.get('textBottom', ''),
        selected_color=selected_color, text_top_y=position(request.form.get('textTop_y')),
        text_bottom_y=position(request.form.get('textBottom_y')))
@app.route('/static/img/<path:path>')
def serve_images(path):
    return send_from_directory('static/img', path)
if __name__ == '__main__':
    app.run(debug=True)
