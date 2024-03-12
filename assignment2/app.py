"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""


from flask import Flask, request, render_template
import sqlite3

import ner
from sqlite_helpers import EntityDatabase
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entities.db'
db = SQLAlchemy(app)

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('form.html', input=open('input.txt').read())

@app.route('/result', methods=['POST'])
def result():
    text = request.form['text']
    doc = ner.SpacyDocument(text)
    markup = doc.get_entities_with_markup()
    markup_paragraphed = ''
    for line in markup.split('\n'):
        if line.strip() == '':
            markup_paragraphed += '<p/>\n'
        else:
            markup_paragraphed += line
    dep_paragraphed = ''
    dep = doc.get_dependencies()
    for line in dep:
        relation_id = sqlite_server.upload_relation(" ".join(line))
        # Upload both entities in relation with reference to relation id
        sqlite_server.upload_entity(line[0], relation_id)
        sqlite_server.upload_entity(line[2], relation_id)
        # &#0009; is HTML tab literal
        dep_paragraphed += f"<p class='dep_line'/>{line[0]}&#0009;<b>{line[1]}</b>&#0009;{line[2]}\n"
    return render_template('result.html', markup=markup_paragraphed, dep=dep_paragraphed)

@app.route('/relations', methods=['GET'])
def relations():
    entities = sqlite_server.get_entities_and_relations()
    return render_template('relations.html', entities=entities)

@app.route('/delete_all', methods=['POST'])
def delete_all():
    sqlite_server.delete_all()
    return "All files deleted."


if __name__ == '__main__':
    sqlite_server = EntityDatabase(db, app)
    app.run(debug=True,port=5555)
