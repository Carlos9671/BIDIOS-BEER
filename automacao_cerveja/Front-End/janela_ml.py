import customtkinter as ctk
import tkinter as tk
from customtkinter import CTk
import requests
import base64
from PIL import Image, ImageTk
import io


def pagar_com_pix():
    dados = {
        "valor": 15.00,
        "email": "teste@email.com"
    }

    resposta = requests.post(
        "http://localhost:5000/criar_pix",
        json=dados
    )

    print("STATUS:", resposta.status_code)
    print("TEXTO:", resposta.text)

    if resposta.status_code != 200:
        return

    pix_data = resposta.json()

    img_data = base64.b64decode(pix_data["qr_code_base64"])
    img = Image.open(io.BytesIO(img_data))

    qr = ctk.CTkImage(light_image=img, size=(400, 400))

    label_qr.configure(image=qr)
    label_qr.image = qr

    pix_copia = pix_data["qr_code"]

    campo_pix.delete("1.0", "end")
    campo_pix.insert("1.0", pix_copia)

    janelaqrcode.tkraise()
    verificar_pagamento()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


janela = ctk.CTk()
janela.title("BIDIO'S BEER")
janela.geometry("1600x900")


janelaml = ctk.CTkFrame(janela)
janelapag = ctk.CTkFrame(janela)
janelaqrcode = ctk.CTkFrame(janela)
janelaconcluido = ctk.CTkFrame(janela)

for frame in (janelaml, janelapag, janelaqrcode, janelaconcluido):
    frame.place(relwidth=1, relheight=1)

def pagamento():
    janelapag.tkraise()

def voltar():
    janelaml.tkraise()

def verificar_pagamento():

    resposta = requests.get("http://localhost:5000/status_pagamento").json()

    if resposta["pago"]:
        janelaconcluido.tkraise()
        return
    else:
        janela.after(2000, verificar_pagamento)

voltarml = ctk.CTkButton(
    janelaml,
    text="Voltar ao início",
    command=voltar,
    font=("Arial", 16, "bold"),
    width=60,
    height=40
)
voltarml.place(x=40, y=40)

texto1ml = ctk.CTkLabel(
    janelaml,
    text="BIDIO'S BEER",
    font=("Arial", 60, "bold"),
)
texto1ml.pack(pady=60)

texto2ml = ctk.CTkLabel(
    janelaml,
    text="Escolha a quantidade desejada:",
    font=("Arial", 40, "bold")
)
texto2ml.pack(pady=60)

botao1ml = ctk.CTkButton(
    janelaml,
    text="300ml",
    command=pagamento,
    font=("Arial", 70, "bold"),
    width=600,
    height=400,
    corner_radius=20
)
botao1ml.place(x=100, y=375)

botao2ml = ctk.CTkButton(
    janelaml,
    text="500ml",
    command=pagamento,
    font=("Arial", 70, "bold"),
    width=600,
    height=400,
    corner_radius=20
)
botao2ml.place(x=900, y=375)

voltarpag = ctk.CTkButton(
    janelapag,
    text="Voltar ao início",
    command=voltar,
    font=("Arial", 16, "bold"),
    width=60,
    height=40
)
voltarpag.place(x=40, y=40)

titulopag = ctk.CTkLabel(
    janelapag,
    text="Forma de pagamento",
    font=("Arial", 60, "bold")
)
titulopag.pack(pady=40)

texto1pag = ctk.CTkLabel(
    janelapag,
    text="Escolha sua forma de pagamento",
    font=("Arial", 40, "bold")
)
texto1pag.pack(pady=100)

botao1pag = ctk.CTkButton(
    janelapag,
    text="PIX",
    command=pagar_com_pix,
    font=("Arial", 70, "bold"),
    width=600,
    height=400,
    corner_radius=20
)
botao1pag.place(x=100, y=375)

botao2pag = ctk.CTkButton(
    janelapag,
    text="Cartão"
         "\n BIDIO'S BEER",
    command=pagar_com_pix,
    font=("Arial", 70, "bold"),
    width=600,
    height=400,
    corner_radius=20
)
botao2pag.place(x=900, y=375)

voltarqrcode = ctk.CTkButton(
    janelaqrcode,
    text="Voltar ao início",
    command=voltar,
    font=("Arial", 16, "bold"),
    width=60,
    height=40
)
voltarqrcode.place(x=40, y=40)

titulo_qr_code = ctk.CTkLabel(
    janelaqrcode,
    text="Aproxime se celular e leia o QRCODE",
    font=("Arial", 40, "bold")
)
titulo_qr_code.pack(pady=100)

label_qr = ctk.CTkLabel(janelaqrcode, text="")
label_qr.pack()

campo_pix = ctk.CTkTextbox(
    janelaqrcode,
    width=800,
    height=80,
)
campo_pix.pack(pady=40)

tituloconcluido = ctk.CTkLabel(
    janelaconcluido,
    text="PAGAMENTO CONCLUÍDO! \n Agora é só aproveitar \n a melhor cerveja da região",
    font=("Arial", 60, "bold")
)
tituloconcluido.pack(pady=200)


janelaml.tkraise()
janela.mainloop()



