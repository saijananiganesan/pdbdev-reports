from flask import json,Flask, flash, render_template, request, url_for, redirect,send_file
import jinja2
import os,sys
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import numpy as np

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
@app.route("/home/")
@app.route("/introduction.html")
@app.route("/home/introduction.html")
def home():
    return render_template("introduction.html")

@app.route("/definitions.html")
@app.route("/home/definitions.html")
def definitons():
    return render_template("definitions.html")

@app.route("/<id>/main.html")
def main(id):
    path=id+'/main.html'
    print (path)
    return render_template(path)

@app.route("/<id>/model_composition.html")
def model_composition(id):
    path=id+'/model_composition.html'
    print (path)
    return render_template(path)

@app.route("/<id>/data_quality.html")
def data_quality(id):
    path=id+'/data_quality.html'
    print (path)
    return render_template(path)

@app.route("/<id>/model_quality.html")
def model_quality(id):
    path=id+'/model_quality.html'
    print (path)
    return render_template(path)

@app.route("/<id>/formodeling.html")
def formodeling(id):
    path=id+'/formodeling.html'
    print (path)
    return render_template(path)

@app.route("/<id>/notformodeling.html")
def notformodeling(id):
    path=id+'/notformodeling.html'
    print (path)
    return render_template(path)

@app.route("/<id>/uncertainty.html")
def uncertainty(id):
    path=id+'/uncertainty.html'
    print (path)
    return render_template(path)

@app.route('/<id>/download')
def downloadFile (id):
    path='static/pdf/'+id+'.cif.pdf'
    return send_file(path, as_attachment=True)

@app.route('/<id>/downloadTable')
def downloadTable (id):
    path='static/pdf/Supplementary_'+id+'.cif.pdf'
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.config["CACHE_TYPE"] = "null"
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


