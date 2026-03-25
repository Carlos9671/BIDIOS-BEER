import customtkinter as ctk

def vermelho():
    janelapag.configure(fg_color="#8B0000")

def branco():
    janelapag.configure(fg_color="#F5F5F5")

ctk.set_default_color_theme("blue")

janelapag = ctk.CTk()
janelapag.title("Forma de pagamento")
janelapag.geometry("1600x900")

titulo = ctk.CTkLabel(
    janelapag,
    text="Forma de pagamento",
    font=("Arial", 60, "bold")
)
titulo.pack(pady=40)

texto1 = ctk.CTkLabel(
    janelapag,
    text="Escolha sua forma de pagamento",
    font=("Arial", 40, "bold")
)
texto1.pack(pady=100)

botao1 = ctk.CTkButton(
    janelapag,
    text="PIX",
    command=vermelho,
    font=("Arial", 70, "bold"),
    width=600,
    height=400,
    corner_radius=20
)
botao1.place(x=100, y=375)

botao2 = ctk.CTkButton(
    janelapag,
    text="Cartão"
         "\n BIDIO'S BEER",
    command=branco,
    font=("Arial", 70, "bold"),
    width=600,
    height=400,
    corner_radius=20
)
botao2.place(x=900, y=375)
