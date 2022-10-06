import os
import sqlConnection
from flask import Flask, request, render_template, jsonify, redirect, make_response

app = Flask(__name__)

@app.route("/")
def main():
    logado = autenticar_login()
    if logado is None:
        return render_template("/index.html", erro = "")

    return render_template('index.html', logado = logado['id_conta'], mensagem = "")

@app.route("/register", methods=["GET"])
def accessRegisterPage():
    logado = autenticar_login()
    if logado is None:
        return render_template("/register.html", erro = "")
    return make_response(redirect("/"))

@app.route("/register", methods=["POST"])
def confirmRegister():
    register_accId = request.form['register-account']
    register_email = request.form['register-email']
    register_key = request.form['register-password']

    sqlConnection.sqlSv_addAccess(register_accId, register_email, register_key)
    return make_response(redirect("/login")) 

@app.route("/login", methods=["GET"])
def accessLoginPage():
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro = "")
    return make_response(redirect("/")) 

@app.route("/login", methods=["POST"])
def confirmAccess():
        register_accId = request.form['login-account']
        register_key = request.form['login-password']

        accessInfo = sqlConnection.sqlSv_access(register_accId, register_key)

        if accessInfo == None:
            return render_template("login.html", erro = "")
        else:
            resposta = make_response(redirect("/"))  
            resposta.set_cookie("id_conta", register_accId, samesite = "Strict")
            resposta.set_cookie("senha", register_key, samesite = "Strict")
            return resposta

@app.route("/logout", methods = ["POST"])
def logout():
    resposta = make_response(render_template("login.html", mensagem = ""))
    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    return resposta

def autenticar_login():
    login = request.cookies.get("id_conta", "")
    senha = request.cookies.get("senha", "")
    return sqlConnection.sqlSv_access(login, senha)

if __name__ == '__main__':
    app.run(host='localhost', port=5002, debug=True)