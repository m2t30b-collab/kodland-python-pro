from flask import Flask, render_template, request, abort
from pathlib import Path
import json
app = Flask(__name__)
PROJECTS = {
 'button_python': ('Python y PNL', 'resumidor'),
 'button_discord': ('Bots educativos', 'bots'),
 'button_html': ('HTML y CSS', 'tecnologia'),
 'button_db': ('SQLite y Flask', 'diario'),
}
@app.route('/', methods=['GET', 'POST'])
def index():
    selected = next((key for key in PROJECTS if key in request.form), None)
    project = PROJECTS.get(selected)
    return render_template('index.html', project=project)
@app.route('/feedback', methods=['POST'])
def feedback():
    email = request.form.get('email', '').strip()
    text = request.form.get('text', '').strip()
    if '@' not in email or not text:
        abort(400)
    with Path(app.root_path, 'feedback.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps({'email': email, 'text': text}, ensure_ascii=False) + '\n')
    return render_template('index.html', project=None, feedback_received=True)
if __name__ == '__main__':
    app.run(debug=True)
