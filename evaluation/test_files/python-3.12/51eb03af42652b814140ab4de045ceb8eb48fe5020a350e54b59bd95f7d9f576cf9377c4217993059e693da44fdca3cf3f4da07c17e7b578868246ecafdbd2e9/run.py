from flask import Flask, request, render_template
import main
from flask_cors import CORS
app = Flask(__name__)

@app.route('/<string:sentences>/')
def getSentences(sentences):
    return main.loadModel(sentences)

@app.route('/', methods=['GET', 'POST'])
@app.route('/train/')
def train():
    main.trainModel()
app.debug = False
app.run()