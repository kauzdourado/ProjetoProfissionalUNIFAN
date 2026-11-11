from database.conexao import conectar
from models.cliente import Cliente


def inserir(cliente):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Cliente (nome, telefone, email, data_nascimento, problema_quimico) "
            "VALUES (%s, %s, %s, %s, %s)",
            (cliente.nome, cliente.telefone, cliente.email,
             cliente.nascimento, cliente.problema_quimico),
        )
        conn.commit()
        cliente.id = cursor.lastrowid
    finally:
        conn.close()


def buscar_por_telefone(telefone):
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Cliente WHERE telefone = %s", (telefone,))
        linha = cursor.fetchone()
    finally:
        conn.close()

    if linha is None:
        return None
    return Cliente(
        id=linha["id_cliente"],
        nome=linha["nome"],
        telefone=linha["telefone"],
        email=linha["email"],
        nascimento=linha["data_nascimento"],
        problema_quimico=linha["problema_quimico"],
    )