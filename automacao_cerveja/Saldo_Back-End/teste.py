sql_insert = "INSERT INTO Saldo (idCartão, Saldo) VALUES (%s, %s)"
cursor.execute(sql_insert, ("98451234", 150.00))
conexao.commit()

print("Cartão inserido com sucesso!")
