# app_flask.py
# Aplicação Flask para interface web da Biblioteca Universitária
# Exibe lista de livros, permite cadastrar novos e excluir.
# Conecta ao banco SQLite conforme solicitado na atividade.

from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "biblioteca.db"

def init_db():
    """Cria o banco de dados e tabela, caso não existam."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            disponivel INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Template HTML Jinja2 embutido
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Biblioteca Universitária</title>
<style>
    body { background-color: #121212; color: #e6e6e6; font-family: Arial; }
    .container { width: 70%; margin: auto; background-color: #1e1e1e; margin-top: 40px; padding: 25px; border-radius: 10px; }
    input { width: 98%; padding: 10px; margin: 8px 0; background-color: #2b2b2b; border: none; color: white; border-radius: 5px; }
    button { width: 100%; background-color: #6200ea; border: none; padding: 12px; color: white; cursor: pointer; border-radius: 5px; }
    button:hover { background-color: #7c34ff; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { padding: 10px; text-align: center; }
    .btn-delete { padding: 6px 10px; background-color: #d32f2f; color: white; border-radius: 5px; text-decoration: none; }
</style>
</head>
<body>
<div class="container">
<h2>📚 Biblioteca Universitária — Cadastro de Livros</h2>

<form method="POST">
  <input name="titulo" placeholder="Título" required>
  <input name="autor" placeholder="Autor" required>
  <input name="ano_publicacao" placeholder="Ano de Publicação" type="number" required>
  <input name="disponivel" placeholder="Disponível (0 ou 1)" type="number" min="0" max="1" required>
  <button type="submit">Salvar Livro</button>
</form>

<table>
<tr><th>ID</th><th>Título</th><th>Autor</th><th>Ano</th><th>Disponível</th><th>Ações</th></tr>
{% for livro in livros %}
<tr>
  <td>{{ livro[0] }}</td>
  <td>{{ livro[1] }}</td>
  <td>{{ livro[2] }}</td>
  <td>{{ livro[3] }}</td>
  <td>{{ 'Sim' if livro[4] == 1 else 'Não' }}</td>
  <td><a class="btn-delete" href="/delete/{{ livro[0] }}" onclick="return confirm('Excluir?')">Excluir</a></td>
</tr>
{% endfor %}
</table>

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Inserir novo livro
    if request.method == "POST":
        cursor.execute("""
            INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) 
            VALUES (?,?,?,?)
        """, (
            request.form["titulo"],
            request.form["autor"],
            int(request.form["ano_publicacao"]),
            int(request.form["disponivel"])
        ))
        conn.commit()

    # Listar livros
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    conn.close()

    return render_template_string(HTML, livros=livros)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM livros WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
