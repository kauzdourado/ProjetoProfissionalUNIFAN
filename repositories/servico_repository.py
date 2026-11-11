from database.conexao import conectar
from models.servico import Servico


def _para_objeto(linha):
    return Servico(id=linha["id_servico"], nome=linha["nome"], preco=linha["preco"])


def listar():
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Servico ORDER BY id_servico")
        return [_para_objeto(l) for l in cursor.fetchall()]
    finally:
        conn.close()


def buscar_por_id(id_servico):
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Servico WHERE id_servico = %s", (id_servico,))
        linha = cursor.fetchone()
    finally:
        conn.close()
    return _para_objeto(linha) if linha else None


def inserir(servico):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Servico (nome, preco) VALUES (%s, %s)",
            (servico.nome, servico.preco),
        )
        conn.commit()
        servico.id = cursor.lastrowid
    finally:
        conn.close()


def atualizar(servico):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Servico SET nome = %s, preco = %s WHERE id_servico = %s",
            (servico.nome, servico.preco, servico.id),
        )
        conn.commit()
    finally:
        conn.close()


def excluir(id_servico):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Servico WHERE id_servico = %s", (id_servico,))
        conn.commit()
    finally:
        conn.close()