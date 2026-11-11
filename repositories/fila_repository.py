from database.conexao import conectar


def cliente_na_fila(id_cliente):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM Lista_Espera WHERE id_cliente = %s AND status = 'Aguardando'",
            (id_cliente,),
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def entrar(id_cliente):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Lista_Espera (id_cliente) VALUES (%s)", (id_cliente,))
        conn.commit()
    finally:
        conn.close()


def listar():
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT e.id_espera, c.nome "
            "FROM Lista_Espera e "
            "INNER JOIN Cliente c ON c.id_cliente = e.id_cliente "
            "WHERE e.status = 'Aguardando' "
            "ORDER BY e.data_entrada, e.id_espera"
        )
        return cursor.fetchall()
    finally:
        conn.close()


def chamar_proximo():
    """Marca o primeiro da fila como 'Chamado' e devolve o nome (ou None)."""
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT e.id_espera, c.nome "
            "FROM Lista_Espera e "
            "INNER JOIN Cliente c ON c.id_cliente = e.id_cliente "
            "WHERE e.status = 'Aguardando' "
            "ORDER BY e.data_entrada, e.id_espera LIMIT 1"
        )
        proximo = cursor.fetchone()
        if proximo is None:
            return None
        cursor.execute(
            "UPDATE Lista_Espera SET status = 'Chamado' WHERE id_espera = %s",
            (proximo["id_espera"],),
        )
        conn.commit()
        return proximo["nome"]
    finally:
        conn.close()