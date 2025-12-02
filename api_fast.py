# api_fast.py
# API FastAPI para CRUD completo da tabela livros
# Implementa GET, POST, PUT, DELETE conforme a atividade AV2

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3

DB = "biblioteca.db"
app = FastAPI(title="API Biblioteca Universitária")

class Livro(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    disponivel: bool

def conectar():
    """Cria conexão com SQLite."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/livros")
def listar():
    """Lista todos os livros."""
    conn = conectar()
    rows = conn.execute("SELECT * FROM livros").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/livros/{id}")
def obter(id: int):
    """Obtém um livro específico."""
    conn = conectar()
    row = conn.execute("SELECT * FROM livros WHERE id = ?", (id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    return dict(row)

@app.post("/livros", status_code=status.HTTP_201_CREATED)
def adicionar(livro: Livro):
    """Adiciona novo livro."""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO livros (titulo, autor, ano_publicacao, disponivel)
        VALUES (?,?,?,?)
    """, (livro.titulo, livro.autor, livro.ano_publicacao, int(livro.disponivel)))
    
    conn.commit()
    novo_id = cur.lastrowid
    conn.close()

    return obter(novo_id)

@app.put("/livros/{id}")
def atualizar(id: int, livro: Livro):
    """Atualiza um livro existente (endpoint obrigatório)."""
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE livros
        SET titulo = ?, autor = ?, ano_publicacao = ?, disponivel = ?
        WHERE id = ?
    """, (livro.titulo, livro.autor, livro.ano_publicacao, int(livro.disponivel), id))

    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    conn.close()
    return {"mensagem": "Livro atualizado com sucesso", "id": id}

@app.delete("/livros/{id}")
def excluir(id: int):
    """Exclui livro por ID."""
    conn = conectar()
    cur = conn.cursor()

    cur.execute("DELETE FROM livros WHERE id = ?", (id,))
    conn.commit()
    apagou = cur.rowcount
    conn.close()

    if apagou == 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    return {"mensagem": "Livro excluído com sucesso"}
