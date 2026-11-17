from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

#Задание 1
@app.route("/")
def glavnaya():
    return "Должна показаться наша строка"

#Задание 2
@app.route("/privet/<imya>")
def privet(imya):
    return f"Здравствуйте, {imya}!"

@app.route("/kvadrat/<int:chislo>")
def kvadrat(chislo):
    return f"Число: {chislo}, квадрат: {chislo * chislo}"

#Задание 3
SPISOK = ["Иванов", "Петров", "Сидоров"]

@app.route("/spisok")
def spisok():
    return jsonify(SPISOK)

@app.route("/spisok/dlina")
def spisok_dlina():
    return jsonify({"dlina": len(SPISOK)})

#Задание 4
@app.route("/spisok/<int:nomer>")
def odin(nomer):
    if nomer < 1 or nomer > len(SPISOK):
        return jsonify({"oshibka": "такого номера нет"}), 404
    return jsonify({"nomer": nomer, "fio": SPISOK[nomer - 1]})

#Задание 5
@app.route("/dobavit", methods=["POST"])
def dobavit():
    dannye = request.get_json(silent=True)
    if not dannye or "fio" not in dannye:
        return jsonify({"oshibka": "нет поля fio"}), 400
    fio = dannye["fio"]
    SPISOK.append(fio)
    return jsonify({"soobshenie": "добавлено", "fio": fio}), 201

#Задание 6
@app.route("/stranica")
def stranica():
    return render_template("spisok.html", spisok=SPISOK)

@app.errorhandler(404)
def net_stranicy():
    return jsonify({"oshibka": "такого адреса нет"}), 404

#python razminka_app.py
app.run(debug=True)