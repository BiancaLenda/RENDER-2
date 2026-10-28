"""Catálogo de Filmes · UC32
Sistema CRUD com Flask + SQLite, pronto para deploy no Render.
"""
import os
import sqlite3

from flask import (Flask, flash, g, redirect, render_template, request,
                   url_for)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-troque-em-producao")

# Caminho do banco: ao lado do app.py (no Render o arquivo é temporário)
DATABASE = os.environ.get(
    "DATABASE_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "filmes.db")
)

GENEROS = [
    "Ação", "Animação", "Aventura", "Comédia", "Documentário", "Drama",
    "Fantasia", "Ficção Científica", "Musical", "Romance", "Suspense", "Terror",
]
ANO_MIN, ANO_MAX = 1888, 2100


# ---------- Banco de dados ----------
def get_db():
    """Abre (uma vez por requisição) a conexão com o SQLite."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria a tabela automaticamente ao iniciar o app."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS filmes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo  TEXT    NOT NULL,
                genero  TEXT    NOT NULL,
                ano     INTEGER NOT NULL,
                nota    INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 10)
            )
            """
        )


# Roda também quando o gunicorn importa o módulo (app:app)
init_db()


# ---------- Validação ----------
def ler_formulario():
    """Lê e valida os campos. Retorna (dados, lista_de_erros)."""
    titulo = request.form.get("titulo", "").strip()
    genero = request.form.get("genero", "").strip()
    ano_txt = request.form.get("ano", "").strip()
    nota_txt = request.form.get("nota", "").strip()
    erros = []

    if not titulo:
        erros.append("Informe o título do filme.")
    elif len(titulo) > 120:
        erros.append("O título pode ter no máximo 120 caracteres.")

    if genero not in GENEROS:
        erros.append("Escolha um gênero da lista.")

    try:
        ano = int(ano_txt)
        if not ANO_MIN <= ano <= ANO_MAX:
            erros.append(f"O ano deve estar entre {ANO_MIN} e {ANO_MAX}.")
    except ValueError:
        ano = None
        erros.append("O ano de lançamento deve ser um número.")

    try:
        nota = int(nota_txt)
        if not 1 <= nota <= 10:
            erros.append("A nota deve ser de 1 a 10.")
    except ValueError:
        nota = None
        erros.append("A nota deve ser um número de 1 a 10.")

    dados = {"titulo": titulo, "genero": genero, "ano": ano_txt, "nota": nota_txt}
    return dados, erros, (titulo, genero, ano, nota)


# ---------- Rotas CRUD ----------
@app.route("/")
def index():
    """READ · lista todos os filmes."""
    filmes = get_db().execute(
        "SELECT id, titulo, genero, ano, nota FROM filmes ORDER BY id DESC"
    ).fetchall()
    total = len(filmes)
    media = round(sum(f["nota"] for f in filmes) / total, 1) if total else None
    return render_template("index.html", filmes=filmes, total=total, media=media)


@app.route("/novo", methods=["GET", "POST"])
def criar():
    """CREATE · cadastra um novo filme."""
    dados = {"titulo": "", "genero": "", "ano": "", "nota": ""}
    if request.method == "POST":
        dados, erros, valores = ler_formulario()
        if not erros:
            db = get_db()
            db.execute(
                "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
                valores,
            )
            db.commit()
            flash(f"“{valores[0]}” foi adicionado ao catálogo.", "ok")
            return redirect(url_for("index"))
        for e in erros:
            flash(e, "erro")
    return render_template("form.html", filme=dados, generos=GENEROS, editando=False)


@app.route("/editar/<int:filme_id>", methods=["GET", "POST"])
def editar(filme_id):
    """UPDATE · edita um filme existente."""
    db = get_db()
    filme = db.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,)).fetchone()
    if filme is None:
        flash("Filme não encontrado.", "erro")
        return redirect(url_for("index"))

    dados = dict(filme)
    if request.method == "POST":
        dados, erros, valores = ler_formulario()
        if not erros:
            db.execute(
                "UPDATE filmes SET titulo = ?, genero = ?, ano = ?, nota = ? WHERE id = ?",
                (*valores, filme_id),
            )
            db.commit()
            flash(f"“{valores[0]}” foi atualizado.", "ok")
            return redirect(url_for("index"))
        for e in erros:
            flash(e, "erro")
    return render_template(
        "form.html", filme=dados, generos=GENEROS, editando=True, filme_id=filme_id
    )


@app.route("/excluir/<int:filme_id>", methods=["POST"])
def excluir(filme_id):
    """DELETE · remove um filme (somente via POST)."""
    db = get_db()
    filme = db.execute("SELECT titulo FROM filmes WHERE id = ?", (filme_id,)).fetchone()
    if filme is None:
        flash("Filme não encontrado.", "erro")
    else:
        db.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))
        db.commit()
        flash(f"“{filme['titulo']}” foi removido.", "ok")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
