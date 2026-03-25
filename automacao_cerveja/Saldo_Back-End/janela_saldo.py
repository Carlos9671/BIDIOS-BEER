import customtkinter as ctk
import mysql.connector

conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Futebol@1",
    database="saldocartao"
)

cursor = conexao.cursor()

id_cartao = "98451234"
sql = "SELECT Saldo FROM Saldo WHERE idCartão = %s"
cursor.execute(sql, (id_cartao,))
resultado = cursor.fetchone()

saldo = int(resultado[0]) if resultado else 0  # Se não achar, começa com 0

conexao.close()  # Fecha a conexão depois de buscar

def diminuir_saldo():
    global saldo
    saldo = saldo - 1
    titulosaldo.configure(text=f"Saldo restante: {saldo}")
    if saldo <= 0:
        janelasemsaldo.tkraise()
        #fazer mais coisas que agora não da pra botar


def saldo_restante():
    conexao2 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Futebol@1",
        database="saldocartao"
    )
    cursor2 = conexao2.cursor()
    sql = "UPDATE Saldo SET Saldo = %s WHERE idCartão = %s"
    cursor2.execute(sql, (saldo, "98451234"))
    conexao2.commit()
    conexao2.close()

def trocar_tela():
    saldo_restante()  # Salva no banco antes de trocar de tela
    textotelafinal.configure(text=f"Obrigado por comprar nosso Chopp\nSeu saldo restante ficou em: {saldo}")
    janelafinal.tkraise()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


janela = ctk.CTk()
janela.title("SALDO")
janela.geometry("1600x900")

janelasaldo = ctk.CTkFrame(janela)
janelasemsaldo = ctk.CTkFrame(janela)
janelafinal = ctk.CTkFrame(janela)

for frame in (janelasaldo, janelasemsaldo, janelafinal):
    frame.place(relwidth=1, relheight=1)

titulosaldo = ctk.CTkLabel(
    janelasaldo,
    text=f"Saldo restante {saldo}",
)
titulosaldo.pack()

botaosaldo = ctk.CTkButton(
    janelasaldo,
    command=diminuir_saldo,
    text="pulso",
    width=600,
    height=400,
    corner_radius=20
)
botaosaldo.pack()

botaoparar = ctk.CTkButton(
    janelasaldo,
    command=trocar_tela,
    text="PARAR",
    width=200,
    height=200,
)
botaoparar.pack(pady=200)

titulosemsaldo = ctk.CTkLabel(
    janelasemsaldo,
    text=f"SALDO INSUFICIENTE",
    font=("Arial", 80),
)
titulosemsaldo.pack(pady=400)

textotelafinal = ctk.CTkLabel(
    janelafinal,
    text=f"",
    font=("Arial", 14),
)
textotelafinal.pack(pady=400)

janelasaldo.tkraise()
janela.mainloop()