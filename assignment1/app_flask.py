"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""


from flask import Flask, request, render_template

import ner

app = Flask(__name__)


# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt').read())
    else:
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
            # &#0009; is HTML tab literal
            dep_paragraphed += f"<p class='dep_line'/>{line[0]}&#0009;<b>{line[1]}</b>&#0009;{line[2]}\n"
        return render_template('result.html', markup=markup_paragraphed, dep=dep_paragraphed)


if __name__ == '__main__':

    app.run(debug=True)
