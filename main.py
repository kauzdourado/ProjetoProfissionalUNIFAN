from views.menu import menu

if __name__ == "__main__":
    menu()


    from database.conexao import conectar

conn = conectar()
cursor = conn.cursor()

cursor.execute("SELECT DATABASE(), @@hostname, @@port")
print("Banco / host / porta:", cursor.fetchone())

cursor.execute("SELECT id_cliente, nome, telefone FROM Cliente")
linhas = cursor.fetchall()
print("Total de clientes:", len(linhas))
for linha in linhas:
    print(repr(linha))

conn.close()