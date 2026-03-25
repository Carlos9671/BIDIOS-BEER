import tkinter as tk


def vermelho():
    janela.configure(background="red")
    botao1.configure(background="red")
    botao2.configure(background="red")
    texto.configure(background="red")
def branco():
    janela.configure(background="white")
    botao1.configure(background="white")
    botao2.configure(background="white")
    texto.configure(background="white")
janela = tk.Tk()
janela.title("BIDIO'S BEER")
janela.geometry("1600x900")
texto = tk.Label(janela, text="Escolha a cor desejada", font=("Arial", 40))
texto.pack()
botao1 = tk.Button(janela, text="Vermelho", command=vermelho, font=("Arial", 80), bd=0)
botao1.place(x=100, y= 375, width=600, height=400)
botao2 = tk.Button(janela, text="Branco", command=branco, font=("Arial", 80),bd=0 )
botao2.place(x=900, y=375, width=600, height=400)
janela.mainloop()

