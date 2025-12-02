import sqlite3

conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    autor TEXT,
    ano_publicacao INTEGER,
    disponivel BOOLEAN
);
""")

conn.commit()
conn.close()
print("Banco criado!")
