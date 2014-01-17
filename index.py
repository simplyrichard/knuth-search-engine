#!/usr/bin/env python

"""
    knuth
    =====

    A document repository with browsing, storage and indexing capabilities.

    (C) 10.12.25, 2013, Lukas Prokop, Andi
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from database import Document
from database import Metadata
from database import db

import os.path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1445@localhost/knuth_db';

db.init_app(app)


@app.route('/faq')
def faq():
    return render_template('faq.html', page='faq')


@app.route('/impressum')
def impressum():
    return render_template('impressum.html', page='impressum')


@app.route('/syntax')
def info():
    return render_template('syntax.html', page='info')


@app.route('/create')
def create(methods=['GET', 'POST']):
    return render_template('create.html', page='create')


@app.route('/browse')
@app.route('/list/', defaults={'page' : 0})
@app.route('/list/<int:page>')
def list(page=0, methods=['GET']):
    # 1. request data from DB
    documents = Document.query.all()
    
    document_dict = {}
    for doc in documents:
        document_dict[str(doc.id)] = doc
        
    # 2. provide data to template engine
    return render_template('list.html', **{'documents' : document_dict, 'page' : 'list'})


@app.route('/update')
def update(methods=['POST', 'PUT']):
    return render_template('doc.html', page='update')


@app.route('/delete/<int:doc_id>')
def delete(doc_id, methods=['DELETE']):
    return render_template('doc.html', doc_id=doc_id, page='delete')


@app.route('/news')
def news():
    return ''


@app.route('/doc/<int:doc_id>')
def doc(doc_id):
    document = Document.query.filter_by(id=doc_id).first()
    metadata = Metadata.query.filter_by(document=doc_id).all()

    doc_filename = ''
    for filename in os.listdir('data'):
        if filename.startswith(str(doc_id) + '.'):
            doc_filename = filename
            break
    if not doc_filename:
        abort(404)
    
    return render_template('doc.html', **{'document' : document, 'metadata' : metadata, 'doc_id' : doc_id, 'filepath' : doc_filename, 'page': 'doc'})


@app.route('/')
@app.route('/search')
def main():
    return render_template('index.html', page='main')


if __name__ == '__main__':
    # TODO: change to debug=False for production
    app.run(debug=True, port=5000)
