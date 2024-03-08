from flask import Flask, render_template, request, redirect
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB("data/caminhos.json")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/novo")
def novo():
    return render_template("novo.html")

@app.route("/criar", methods=["POST"])
def criar():
    x = request.form["x"].split(", ")
    y = request.form["y"].split(",")
    z = request.form["z"].split(", ")
    r = request.form["r"].split(", ")
    nome = request.form["nome"]
    if len(x) == len(y) == len(z) == len(r):
        db.insert({"id":len(db)+1,"nome": nome, "pontos" : {"x": x, "y": y, "z": z, "r": r}})
        return redirect("/")
    else:
        return render_template("erro_pos.html")

@app.route("/pegar_caminho")
def pegar_caminho():
    return render_template("pegar_caminho.html")

@app.route("/listar", methods=["POST"])
def listar():
    id_caminho = request.form["id"]
    db_id = Query()
    caminho = db.search(db_id.id == int(id_caminho))
    pontos = caminho[0]["pontos"]
    arr_pontos = [(pontos["x"][i], pontos["y"][i], pontos["z"][i], pontos["r"][i]) for i in range(len(pontos["x"]))]
    return render_template("listar.html", pontos=arr_pontos, id_cam=id_caminho)

@app.route("/listas_caminhos")
def listas_caminhos():
    caminhos = db.all()
    return render_template("listas_caminhos.html", caminhos=caminhos)

@app.route("/atualizar")
def atualizar():
    return render_template("atualizar.html")

@app.route("/atualizar_ponto", methods=["POST"])
def atualizar_ponto():
    id_caminho = request.form["id"]
    db_id = Query()
    caminho = db.search(db_id.id == int(id_caminho))
    pontos = caminho[0]["pontos"]
    return render_template("atualizar_ponto.html", id_cam=id_caminho)

@app.route("/atualizacao", methods=["POST"])
def atualizacao():
    id_caminho = request.form["id_cam"]
    x = request.form["x"].split(", ")
    y = request.form["y"].split(",")
    z = request.form["z"].split(", ")
    r = request.form["r"].split(", ")
    query = Query()
    if len(x) == len(y) == len(z) == len(r):
        db.update({"pontos" : {"x": x, "y": y, "z": z, "r": r}}, query.id == int(id_caminho))
        return redirect("/")
    else:
        return render_template("erro_pos.html")

@app.route("/deletar")
def deletar():
    return render_template("deletar.html")

@app.route("/remover", methods=["POST"])
def remover():
    id_caminho = request.form["id"]
    db_id = Query()
    db.remove(db_id.id == int(id_caminho))
    return redirect("/")

app.run(host="0.0.0.0", port="3000")