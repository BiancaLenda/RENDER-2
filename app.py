from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'agenda-contatos-secret'

DB_PATH = 'agenda.db'


def get_db():
    """Abre conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # resultados como dicionário
    return conn


def init_db():
    """Cria a tabela de contatos se ainda não existir."""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nome    TEXT    NOT NULL,
                email   TEXT,
                telefone TEXT,
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


# ── Rotas ──────────────────────────────────────────────────────

@app.route('/')
def index():
    """Lista todos os contatos."""
    busca = request.args.get('busca', '').strip()
    with get_db() as conn:
        if busca:
            contatos = conn.execute(
                "SELECT * FROM contatos WHERE nome LIKE ? ORDER BY nome",
                (f'%{busca}%',)
            ).fetchall()
        else:
            contatos = conn.execute(
                "SELECT * FROM contatos ORDER BY nome"
            ).fetchall()
    return render_template('index.html', contatos=contatos, busca=busca)


@app.route('/novo', methods=['GET', 'POST'])
def novo():
    """Exibe formulário e salva novo contato."""
    if request.method == 'POST':
        nome     = request.form['nome'].strip()
        email    = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        if not nome:
            flash('O nome é obrigatório.', 'erro')
            return render_template('form.html', contato=None)

        with get_db() as conn:
            conn.execute(
                "INSERT INTO contatos (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone)
            )
            conn.commit()

        flash(f'Contato "{nome}" adicionado com sucesso!', 'ok')
        return redirect(url_for('index'))

    return render_template('form.html', contato=None)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Exibe formulário preenchido e salva edição."""
    with get_db() as conn:
        contato = conn.execute(
            "SELECT * FROM contatos WHERE id = ?", (id,)
        ).fetchone()

    if contato is None:
        flash('Contato não encontrado.', 'erro')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome     = request.form['nome'].strip()
        email    = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        if not nome:
            flash('O nome é obrigatório.', 'erro')
            return render_template('form.html', contato=contato)

        with get_db() as conn:
            conn.execute(
                "UPDATE contatos SET nome=?, email=?, telefone=? WHERE id=?",
                (nome, email, telefone, id)
            )
            conn.commit()

        flash(f'Contato "{nome}" atualizado!', 'ok')
        return redirect(url_for('index'))

    return render_template('form.html', contato=contato)


@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    """Remove um contato."""
    with get_db() as conn:
        contato = conn.execute(
            "SELECT nome FROM contatos WHERE id = ?", (id,)
        ).fetchone()
        if contato:
            conn.execute("DELETE FROM contatos WHERE id = ?", (id,))
            conn.commit()
            flash(f'Contato "{contato["nome"]}" removido.', 'ok')
        else:
            flash('Contato não encontrado.', 'erro')
    return redirect(url_for('index'))


# ── Inicialização ──────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
