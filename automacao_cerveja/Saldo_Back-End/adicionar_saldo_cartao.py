import mysql.connector

# conexão com banco
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Futebol@1",
    database="saldocartao"
)

cursor = conexao.cursor()

valorsaldo = int(input("Digite o valor a ser adicionado: "))
sql = """
    INSERT INTO Saldo (idCartão, Saldo) VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE Saldo = Saldo + VALUES(Saldo)
"""
cursor.execute(sql, ("98451234", valorsaldo))
conexao.commit()

# id lido do cartão
id_cartao = "98451234"

sql = "SELECT saldo FROM Saldo WHERE idCartão = %s"
cursor.execute(sql, (id_cartao,))

resultado = cursor.fetchone()

if resultado:
    print("Saldo:", resultado[0])
else:
    print("Cartão não encontrado")