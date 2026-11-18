import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "signos.db")

SIGNOS = [
    {"name": "Áries", "symbol": "♈", "color": "#ef4444", "period": "21/03 a 19/04", "element": "Fogo", "modality": "Cardinal", "ruler": "Marte", "lucky_numbers": "1, 9, 17", "compatibility": "Leão, Sagitário, Gêmeos", "description": "Corajoso, impulsivo, cheio de energia e iniciativa para começar novos projetos."},
    {"name": "Touro", "symbol": "♉", "color": "#22c55e", "period": "20/04 a 20/05", "element": "Terra", "modality": "Fixo", "ruler": "Vênus", "lucky_numbers": "2, 6, 15", "compatibility": "Virgem, Capricórnio, Câncer", "description": "Determinado, paciente, prático e apreciador do conforto e da estabilidade."},
    {"name": "Gêmeos", "symbol": "♊", "color": "#eab308", "period": "21/05 a 20/06", "element": "Ar", "modality": "Mutável", "ruler": "Mercúrio", "lucky_numbers": "3, 5, 14", "compatibility": "Libra, Aquário, Áries", "description": "Comunicativo, curioso, versátil e sempre em busca de novas ideias e conexões."},
    {"name": "Câncer", "symbol": "♋", "color": "#38bdf8", "period": "21/06 a 22/07", "element": "Água", "modality": "Cardinal", "ruler": "Lua", "lucky_numbers": "2, 7, 11", "compatibility": "Escorpião, Peixes, Touro", "description": "Sensível, protetor, intuitivo e profundamente ligado à família e às emoções."},
    {"name": "Leão", "symbol": "♌", "color": "#f97316", "period": "23/07 a 22/08", "element": "Fogo", "modality": "Fixo", "ruler": "Sol", "lucky_numbers": "1, 4, 19", "compatibility": "Áries, Sagitário, Libra", "description": "Criativo, generoso, confiante e com brilho natural para inspirar quem está por perto."},
    {"name": "Virgem", "symbol": "♍", "color": "#84cc16", "period": "23/08 a 22/09", "element": "Terra", "modality": "Mutável", "ruler": "Mercúrio", "lucky_numbers": "5, 14, 23", "compatibility": "Touro, Capricórnio, Câncer", "description": "Analítico, organizado, prestativo e atento aos mínimos detalhes."},
    {"name": "Libra", "symbol": "♎", "color": "#ec4899", "period": "23/09 a 22/10", "element": "Ar", "modality": "Cardinal", "ruler": "Vênus", "lucky_numbers": "6, 15, 24", "compatibility": "Gêmeos, Aquário, Leão", "description": "Diplomático, sociável, justo e sempre em busca de harmonia e equilíbrio."},
    {"name": "Escorpião", "symbol": "♏", "color": "#a855f7", "period": "23/10 a 21/11", "element": "Água", "modality": "Fixo", "ruler": "Plutão", "lucky_numbers": "8, 11, 18", "compatibility": "Câncer, Peixes, Virgem", "description": "Intenso, estratégico, leal e dono de grande profundidade emocional."},
    {"name": "Sagitário", "symbol": "♐", "color": "#f59e0b", "period": "22/11 a 21/12", "element": "Fogo", "modality": "Mutável", "ruler": "Júpiter", "lucky_numbers": "3, 12, 21", "compatibility": "Áries, Leão, Aquário", "description": "Otimista, aventureiro, sincero e apaixonado por liberdade e conhecimento."},
    {"name": "Capricórnio", "symbol": "♑", "color": "#64748b", "period": "22/12 a 19/01", "element": "Terra", "modality": "Cardinal", "ruler": "Saturno", "lucky_numbers": "4, 8, 22", "compatibility": "Touro, Virgem, Escorpião", "description": "Disciplinado, ambicioso, responsável e focado em construir conquistas duradouras."},
    {"name": "Aquário", "symbol": "♒", "color": "#06b6d4", "period": "20/01 a 18/02", "element": "Ar", "modality": "Fixo", "ruler": "Urano", "lucky_numbers": "4, 7, 11", "compatibility": "Gêmeos, Libra, Sagitário", "description": "Original, independente, visionário e voltado para inovação e causas coletivas."},
    {"name": "Peixes", "symbol": "♓", "color": "#6366f1", "period": "19/02 a 20/03", "element": "Água", "modality": "Mutável", "ruler": "Netuno", "lucky_numbers": "3, 7, 12", "compatibility": "Câncer, Escorpião, Capricórnio", "description": "Empático, sonhador, criativo e conectado com a intuição e a sensibilidade."}
]

SIGNOS_MAP = {s["name"]: s for s in SIGNOS}

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birthdate TEXT NOT NULL,
            sign_name TEXT NOT NULL,
            element TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
    if count == 0:
        exemplos = [
            ("Ana Clara", "1998-04-12", "Áries", "Fogo"),
            ("Lucas Silva", "1995-08-19", "Leão", "Fogo"),
            ("Mariana Costa", "2001-11-05", "Escorpião", "Água"),
        ]
        conn.executemany("INSERT INTO submissions (name, birthdate, sign_name, element) VALUES (?, ?, ?, ?)", exemplos)
    conn.commit()
    conn.close()

def calcular_signo(dia: int, mes: int) -> dict:
    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19): return SIGNOS_MAP["Áries"]
    if (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20): return SIGNOS_MAP["Touro"]
    if (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20): return SIGNOS_MAP["Gêmeos"]
    if (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22): return SIGNOS_MAP["Câncer"]
    if (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22): return SIGNOS_MAP["Leão"]
    if (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22): return SIGNOS_MAP["Virgem"]
    if (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22): return SIGNOS_MAP["Libra"]
    if (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21): return SIGNOS_MAP["Escorpião"]
    if (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21): return SIGNOS_MAP["Sagitário"]
    if (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19): return SIGNOS_MAP["Capricórnio"]
    if (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18): return SIGNOS_MAP["Aquário"]
    return SIGNOS_MAP["Peixes"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/descobrir", methods=["POST"])
@app.route("/api/signo", methods=["POST"])
@app.route("/api/calcular", methods=["POST"])
def api_descobrir():
    dados = request.get_json(silent=True) or request.form
    name = (dados.get("name") or dados.get("nome") or "").strip()
    birthdate = (dados.get("birthdate") or dados.get("data_nascimento") or "").strip()
    if not name or not birthdate:
        return jsonify({"error": "Preencha nome e data de nascimento."}), 400
    try:
        dt = datetime.strptime(birthdate, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Data inválida."}), 400
    sign = calcular_signo(dt.day, dt.month)
    conn = get_db()
    cur = conn.execute("INSERT INTO submissions (name, birthdate, sign_name, element) VALUES (?, ?, ?, ?)", (name, birthdate, sign["name"], sign["element"]))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "name": name, "birthdate": birthdate, "sign": sign}), 201

@app.route("/api/historico", methods=["GET"])
def api_historico():
    conn = get_db()
    rows = conn.execute("SELECT id, name, birthdate, sign_name, element, created_at FROM submissions ORDER BY id DESC").fetchall()
    conn.close()
    items = []
    for r in rows:
        s = SIGNOS_MAP.get(r["sign_name"], SIGNOS[0])
        items.append({
            "id": r["id"],
            "name": r["name"],
            "birthdate": r["birthdate"],
            "sign": s,
            "sign_name": r["sign_name"],
            "sign_symbol": s["symbol"],
            "symbol": s["symbol"],
            "element": r["element"],
            "ruler": s["ruler"],
            "created_at": r["created_at"]
        })
    return jsonify({"items": items})

@app.route("/api/historico/<int:item_id>", methods=["DELETE"])
def api_delete(item_id):
    conn = get_db()
    conn.execute("DELETE FROM submissions WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
