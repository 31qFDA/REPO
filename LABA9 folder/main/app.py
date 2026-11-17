from flask import (Flask, jsonify, request, render_template, redirect, url_for)
from registry import Registry
from people import AnketaError, Student, Teacher
app = Flask(__name__)
INPUT_FILE = "anketa.txt"

zhurnal = Registry()
if not zhurnal.load(INPUT_FILE):
    print("ВНИМАНИЕ: файл не найден, журнал пуст")

def anketa_to_dict(nomer, person):
    return {
        "nomer": nomer,
        "tip": "s" if person.role() == "студент" else "t",
        "fio": person.fio,
        "mail": person.mail,
        "phone": person.phone,
        "extra": person.extra(),
        "rol": person.role(),
    }

def vse_ankety():
    return [anketa_to_dict(i, p) for i, p in enumerate(zhurnal.good, 1)]

def sozdat_personu(tip, fio, mail, phone, extra):
    tip = (tip or "").strip().lower()
    if tip == "s":
        return Student(fio, mail, phone, extra)
    if tip == "t":
        return Teacher(fio, mail, phone, extra)
    raise AnketaError(f"неизвестный тип анкеты: {tip}")

@app.route("/")
def index():
    return render_template(
        "index.html",
        anketi=vse_ankety(),
        prinyato=len(zhurnal.good),
        otkloneno=len(zhurnal.bad),
    )

@app.route("/anketi/<int:nomer>")
def anketa_stranica(nomer):
    if nomer < 1 or nomer > len(zhurnal.good):
        return render_template(
            "oshibka.html",
            soobshenie=f"Анкеты с номером {nomer} нет в журнале",
        ), 404
    person = zhurnal.good[nomer - 1]
    return render_template(
        "anketa.html",
        nomer=nomer,
        chelovek=person,
        rol=person.role(),
        dopolnitelno=person.extra(),
    )

@app.route("/gruppa/<nazvanie>")
def gruppa(nazvanie):
    gruppa_norm = nazvanie.replace(" ", "").lower()
    otbor = [
        anketa_to_dict(i, p)
        for i, p in enumerate(zhurnal.good, 1)
        if p.role() == "студент" and p.extra() == gruppa_norm
    ]
    return render_template(
        "index.html",
        anketi=otbor,
        prinyato=len(zhurnal.good),
        otkloneno=len(zhurnal.bad),
        zagolovok=f"Студенты группы {gruppa_norm}",
        gruppa=gruppa_norm,
    )

@app.route("/statistika")
def statistika():
    return render_template(
        "statistika.html",
        po_rolyam=zhurnal.stats_by_role(),
        po_gruppam=zhurnal.stats_by_group(),
        brak=zhurnal.bad,
        prinyato=len(zhurnal.good),
        otkloneno=len(zhurnal.bad),
    )

@app.route("/dobavit", methods=["GET", "POST"])
def dobavit_stranica():
    if request.method == "GET":
        return render_template("dobavit.html", dannye={}, oshibka=None)

    dannye = {
        "tip": request.form.get("tip", ""),
        "fio": request.form.get("fio", ""),
        "mail": request.form.get("mail", ""),
        "phone": request.form.get("phone", ""),
        "extra": request.form.get("extra", ""),
    }
    try:
        person = sozdat_personu(
            dannye["tip"], dannye["fio"], dannye["mail"],
            dannye["phone"], dannye["extra"],
        )
    except AnketaError as e:
        return render_template(
            "dobavit.html", dannye=dannye, oshibka=str(e)
        ), 400
    zhurnal.add(person)
    zhurnal.good.sort()
    nomer = zhurnal.good.index(person) + 1
    return redirect(url_for("anketa_stranica", nomer=nomer))

@app.route("/api/anketi", methods=["GET"])
def api_anketi():
    rol = request.args.get("rol")
    dannye = vse_ankety()
    if rol:
        dannye = [a for a in dannye if a["rol"] == rol]
    return jsonify(dannye)

@app.route("/api/anketi/<int:nomer>", methods=["GET"])
def api_anketa(nomer):
    if nomer < 1 or nomer > len(zhurnal.good):
        return jsonify({"oshibka": "нет такой анкеты"}), 404
    return jsonify(anketa_to_dict(nomer, zhurnal.good[nomer - 1]))

@app.route("/api/statistika", methods=["GET"])
def api_statistika():
    return jsonify({
        "prinyato": len(zhurnal.good),
        "otkloneno": len(zhurnal.bad),
        "po_rolyam": zhurnal.stats_by_role(),
        "po_gruppam": zhurnal.stats_by_group(),
    })

@app.route("/api/brak", methods=["GET"])
def api_brak():
    return jsonify([
        {"nomer_stroki": ln, "tekst": line, "prichina": reason}
        for ln, line, reason in zhurnal.bad
    ])

@app.route("/api/anketi", methods=["POST"])
def api_dobavit():
    dannye = request.get_json(silent=True)
    if not dannye:
        return jsonify({"oshibka": "пустой JSON"}), 400
    try:
        person = sozdat_personu(
            dannye.get("tip"), dannye.get("fio", ""),
            dannye.get("mail", ""), dannye.get("phone", ""),
            dannye.get("gruppa") or dannye.get("kafedra") or dannye.get("extra", ""),
        )
    except AnketaError as e:
        return jsonify({"oshibka": str(e)}), 400
    zhurnal.add(person)
    zhurnal.good.sort()
    nomer = zhurnal.good.index(person) + 1
    return jsonify(anketa_to_dict(nomer, person)), 201

@app.errorhandler(404)
def net_stranicy():
    if request.path.startswith("/api/"):
        return jsonify({"oshibka": "Такого адреса нет"}), 404
    return render_template(
        "oshibka.html", soobshenie="Такого адреса нет"
    ), 404

app.run(debug=True)