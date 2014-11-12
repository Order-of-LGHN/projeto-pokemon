#!/usr/bin/env python3

from flask import Flask, Response, request

app = Flask(__name__)


@app.route("/battle", methods=["POST"])
def inicia_batalha(battle_state):
    pass


### <TESTES> ###

@app.route('/')
def hello_world():
    x = input("Digite o nº do ataque: ")
    return "Hello World!"


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')

### </TESTES> ###



if __name__ == '__main__':
    app.debug = True
    app.run()  # Usar host='0.0.0.0' para server público
