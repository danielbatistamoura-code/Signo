import os
import sqlite3
from datetime import date, datetime
from flask import Flask, g, jsonify, render_template, request

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "signos.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

app = Flask(__name__)

ZODIAC_CATALOG = [
    {
        "key": "aries",
        "name": "Áries",
        "symbol": "♈",
        "period": "21/03 a 19/04",
        "element": "Fogo",
        "modality": "Cardinal",
        "ruler": "Marte",
        "color": "#ef4444",
        "lucky_numbers": "1, 9, 17, 21",
        "compatibility": "Leão, Sagitário, Gêmeos",
        "summary": "Iniciativa, coragem e energia pioneira.",
        "description": "Pessoas de Áries agem com determinação, entusiasmo e espírito competitivo. Costumam abrir caminhos, tomar decisões rápidas e inspirar quem está por perto pela autenticidade."
    },
    {
        "key": "touro",
        "name": "Touro",
        "symbol": "♉",
        "period": "20/04 a 20/05",
        "element": "Terra",
        "modality": "Fixo",
        "ruler": "Vênus",
        "color": "#22c55e",
        "lucky_numbers": "2, 6, 15, 24",
        "compatibility": "Virgem, Capricórnio, Câncer",
        "summary": "Consistência, lealdade e senso prático.",
        "description": "Touro valoriza segurança, constância e qualidade em tudo o que constrói. Tem paciência para resultados duradouros e grande apreciação pelas coisas boas da vida."
    },
    {
        "key": "gemeos",
        "name": "Gêmeos",
        "symbol": "♊",
        "period": "21/05 a 20/06",
        "element": "Ar",
        "modality": "Mutável",
        "ruler": "Mercúrio",
        "color": "#eab308",
        "lucky_numbers": "3, 5, 14, 23",
        "compatibility": "Libra, Aquário, Áries",
        "summary": "Curiosidade, comunicação e versatilidade.",
        "description": "Gêmeos possui raciocínio ágil, facilidade para aprender e conectar pessoas. Adapta-se rapidamente a novos contextos e traz leveza intelectual para o dia a dia."
    },
    {
        "key": "cancer",
        "name": "Câncer",
        "symbol": "♋",
        "period": "21/06 a 22/07",
        "element": "Água",
        "modality": "Cardinal",
        "ruler": "Lua",
        "color": "#38bdf8",
        "lucky_numbers": "2, 7, 11, 20",
        "compatibility": "Escorpião, Peixes, Touro",
        "summary": "Intuição, acolhimento e memória afetiva.",
        "description": "Câncer tem forte inteligência emocional, instinto protetor e sensibilidade para perceber o ambiente. Constrói vínculos profundos baseados em confiança e cuidado."
    },
    {
        "key": "leao",
        "name": "Leão",
        "symbol": "♌",
        "period": "23/07 a 22/08",
        "element": "Fogo",
        "modality": "Fixo",
        "ruler": "Sol",
        "color": "#f97316",
        "lucky_numbers": "1, 4, 10, 19",
        "compatibility": "Áries, Sagitário, Libra",
        "summary": "Criatividade, generosidade e presença marcante.",
        "description": "Leão expressa calor humano, liderança natural e coragem para assumir o protagonismo. Quando engajado, motiva equipes e transforma ideias em realizações memoráveis."
    },
    {
        "key": "virgem",
        "name": "Virgem",
        "symbol": "♍",
        "period": "23/08 a 22/09",
        "element": "Terra",
        "modality": "Mutável",
        "ruler": "Mercúrio",
        "color": "#10b981",
        "lucky_numbers": "5, 14, 23, 32",
        "compatibility": "Touro, Capricórnio, Escorpião",
        "summary": "Análise, precisão e melhoria contínua.",
        "description": "Virgem observa detalhes que passam despercebidos pela maioria. Usa lógica, método e senso de utilidade para organizar processos e resolver problemas complexos."
    },
    {
        "key": "libra",
        "name": "Libra",
        "symbol": "♎",
        "period": "23/09 a 22/10",
        "element": "Ar",
        "modality": "Cardinal",
        "ruler": "Vênus",
        "color": "#ec4899",
        "lucky_numbers": "6, 9, 15, 24",
        "compatibility": "Gêmeos, Aquário, Leão",
        "summary": "Diplomacia, equilíbrio e senso estético.",
        "description": "Libra busca harmonia nas relações, justiça nas escolhas e clareza na troca de ideias. Tem talento natural para mediar conflitos e construir parcerias."
    },
    {
        "key": "escorpiao",
        "name": "Escorpião",
        "symbol": "♏",
        "period": "23/10 a 21/11",
        "element": "Água",
        "modality": "Fixo",
        "ruler": "Plutão",
        "color": "#be123c",
        "lucky_numbers": "8, 11, 18, 22",
        "compatibility": "Câncer, Peixes, Virgem",
        "summary": "Profundidade, foco e poder de transformação.",
        "description": "Escorpião investiga além da superfície e entrega intensidade total ao que escolhe. Possui resiliência rara para se reinventar diante de qualquer desafio."
    },
    {
        "key": "sagitario",
        "name": "Sagitário",
        "symbol": "♐",
        "period": "22/11 a 21/12",
        "element": "Fogo",
        "modality": "Mutável",
        "ruler": "Júpiter",
        "color": "#a855f7",
        "lucky_numbers": "3, 9, 12, 21",
        "compatibility": "Áries, Leão, Aquário",
        "summary": "Expansão, otimismo e busca por significado.",
        "description": "Sagitário enxerga o horizonte amplo, ama aprender, viajar e explorar novas filosofias. Contagia os outros com entusiasmo, franqueza e visão de futuro."
    },
    {
        "key": "capricornio",
        "name": "Capricórnio",
        "symbol": "♑",
        "period": "22/12 a 19/01",
        "element": "Terra",
        "modality": "Cardinal",
        "ruler": "Saturno",
        "color": "#64748b",
        "lucky_numbers": "4, 8, 13, 22",
        "compatibility": "Touro, Virgem, Peixes",
        "summary": "Estratégia, disciplina e realização sólida.",
        "description": "Capricórnio planeja a longo prazo com maturidade, foco e responsabilidade. Sabe transformar ambição em conquistas concretas passo a passo."
    },
    {
        "key": "aquario",
        "name": "Aquário",
        "symbol": "♒",
        "period": "20/01 a 18/02",
        "element": "Ar",
        "modality": "Fixo",
        "ruler": "Urano",
        "color": "#06b6d4",
        "lucky_numbers": "4, 7, 11, 29",
        "compatibility": "Gêmeos, Libra, Sagitário",
        "summary": "Inovação, independência e visão coletiva.",
        "description": "Aquário questiona padrões antigos para criar soluções originais. Valoriza liberdade intelectual, amizade e ideias capazes de melhorar o futuro."
    },
    {
        "key": "peixes",
        "name": "Peixes",
        "symbol": "♓",
        "period": "19/02 a 20/03",
        "element": "Água",
        "modality": "Mutável",
        "ruler": "Netuno",
        "color": "#14b8a6",
        "lucky_numbers": "3, 7, 12, 16",
        "compatibility": "Câncer, Escorpião, Capricórnio",
        "summary": "Empatia, imaginação e sensibilidade artística.",
        "description": "Peixes conecta intuição, criatividade e compaixão de forma fluida. Compreende nuances humanas profundas e transforma sentimentos em expressão."
    },
]


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()


def detect_sign(birth: date) -> dict:
    m, d = birth.month, birth.day
    if (m == 3 and d >= 21) or (m == 4 and d <= 19):
        return ZODIAC_CATALOG[0]
    if (m == 4 and d >= 20) or (m == 5 and d <= 20):
        return ZODIAC_CATALOG[1]
    if (m == 5 and d >= 21) or (m == 6 and d <= 20):
        return ZODIAC_CATALOG[2]
    if (m == 6 and d >= 21) or (m == 7 and d <= 22):
        return ZODIAC_CATALOG[3]
    if (m == 7 and d >= 23) or (m == 8 and d <= 22):
        return ZODIAC_CATALOG[4]
    if (m == 8 and d >= 23) or (m == 9 and d <= 22):
        return ZODIAC_CATALOG[5]
    if (m == 9 and d >= 23) or (m == 10 and d <= 22):
        return ZODIAC_CATALOG[6]
    if (m == 10 and d >= 23) or (m == 11 and d <= 21):
        return ZODIAC_CATALOG[7]
    if (m == 11 and d >= 22) or (m == 12 and d <= 21):
        return ZODIAC_CATALOG[8]
    if (m == 12 and d >= 22) or (m == 1 and d <= 19):
        return ZODIAC_CATALOG[9]
    if (m == 1 and d >= 20) or (m == 2 and d <= 18):
        return ZODIAC_CATALOG[10]
    return ZODIAC_CATALOG[11]


@app.route("/")
def index():
    return render_template("index.html", catalog=ZODIAC_CATALOG)


@app.route("/api/descobrir", methods=["POST"])
def descobrir():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    birthdate_raw = str(data.get("birthdate", "")).strip()

    if len(name) < 2:
        return jsonify({"error": "Informe um nome com pelo menos 2 caracteres."}), 400

    try:
        birth = datetime.strptime(birthdate_raw, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Data de nascimento inválida. Use o formato AAAA-MM-DD."}), 400

    if birth > date.today():
        return jsonify({"error": "A data de nascimento não pode estar no futuro."}), 400

    sign = detect_sign(birth)

    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO submissions (
            name, birthdate, sign_key, sign_name, element,
            modality, ruler, lucky_numbers, compatibility, description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            birthdate_raw,
            sign["key"],
            sign["name"],
            sign["element"],
            sign["modality"],
            sign["ruler"],
            sign["lucky_numbers"],
            sign["compatibility"],
            sign["description"],
        ),
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM submissions WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()

    return jsonify({
        "id": row["id"],
        "name": row["name"],
        "birthdate": row["birthdate"],
        "created_at": row["created_at"],
        "sign": sign,
    }), 201


@app.route("/api/historico", methods=["GET"])
def historico():
    db = get_db()
    rows = db.execute(
        """
        SELECT id, name, birthdate, sign_key, sign_name, element,
               modality, ruler, lucky_numbers, compatibility, description, created_at
        FROM submissions
        ORDER BY id DESC
        LIMIT 20
        """
    ).fetchall()

    items = []
    for r in rows:
        sign_meta = next((s for s in ZODIAC_CATALOG if s["key"] == r["sign_key"]), ZODIAC_CATALOG[0])
        items.append({
            "id": r["id"],
            "name": r["name"],
            "birthdate": r["birthdate"],
            "sign_name": r["sign_name"],
            "symbol": sign_meta["symbol"],
            "color": sign_meta["color"],
            "period": sign_meta["period"],
            "element": r["element"],
            "modality": r["modality"],
            "ruler": r["ruler"],
            "lucky_numbers": r["lucky_numbers"],
            "compatibility": r["compatibility"],
            "description": r["description"],
            "created_at": r["created_at"],
        })

    return jsonify({"total": len(items), "items": items})


@app.route("/api/historico/<int:submission_id>", methods=["DELETE"])
def deletar_historico(submission_id: int):
    db = get_db()
    cur = db.execute("DELETE FROM submissions WHERE id = ?", (submission_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Registro não encontrado."}), 404
    return jsonify({"deleted": True, "id": submission_id})


init_db()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
