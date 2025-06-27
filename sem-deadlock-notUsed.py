import threading
import time
import random
import tkinter as tk
from tkinter import Canvas, PhotoImage, messagebox

class Lutador:
    def __init__(self, nome, vida, x, y, imagens):
        self.nome = nome
        self.vida = vida
        self.x = x
        self.y = y
        self.imagens = imagens
        self.current_image = self.imagens['defesa']
        self.image_obj = None
        self.vitorias = 0

    def resetar(self):
        self.vida = 100
        self.current_image = self.imagens['defesa']

    def atacar(self, oponente):
        dano = random.randint(10, 30)
        oponente.vida -= dano
        return dano

class JogoLutaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Luta - Melhor de 3")

        self.canvas = Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack()

        imagens_l1 = {
            'defesa': PhotoImage(file="jogadordaesquerdaemposicaodefensiva-removebg-preview.png"),
            'ataque': PhotoImage(file="jogadordaesquerdaemposicaodesoco-removebg-preview.png"),
            'apanhando': PhotoImage(file="jogadordaesquerdapanhandolimpo-removebg-preview.png")
        }

        imagens_l2 = {
            'defesa': PhotoImage(file="Share_Your_3-removebg-preview.png"),
            'ataque1': PhotoImage(file="Share_Your_Sprites_ataque_1-removebg-preview.png"),
            'ataque2': PhotoImage(file="Share_Your_Sprites_ataque_2-removebg-preview.png"),
            'apanhando': PhotoImage(file="jogadordadireitapanando21-removebg-preview.png")
        }

        self.lutador1 = Lutador("Lutador 1", 100, 100, 150, imagens_l1)
        self.lutador2 = Lutador("Lutador 2", 100, 500, 150, imagens_l2)

        self.lutador1.image_obj = self.canvas.create_image(self.lutador1.x, self.lutador1.y, image=self.lutador1.current_image)
        self.lutador2.image_obj = self.canvas.create_image(self.lutador2.x, self.lutador2.y, image=self.lutador2.current_image)

        self.label_vida1 = tk.Label(root, text=f"{self.lutador1.nome}: {self.lutador1.vida} HP")
        self.label_vida1.pack()

        self.label_vida2 = tk.Label(root, text=f"{self.lutador2.nome}: {self.lutador2.vida} HP")
        self.label_vida2.pack()

        self.label_placar = tk.Label(root, text=f"Placar - {self.lutador1.nome}: 0 | {self.lutador2.nome}: 0")
        self.label_placar.pack()

        self.btn_iniciar = tk.Button(root, text="Iniciar Luta", command=self.iniciar_luta)
        self.btn_iniciar.pack(pady=10)

        self.btn_reiniciar = tk.Button(root, text="Reiniciar Jogo", command=self.reiniciar_jogo)
        self.btn_reiniciar.pack(pady=10)
        self.btn_reiniciar.config(state='disabled')

    def atualizar_vidas(self):
        self.label_vida1.config(text=f"{self.lutador1.nome}: {max(0, self.lutador1.vida)} HP")
        self.label_vida2.config(text=f"{self.lutador2.nome}: {max(0, self.lutador2.vida)} HP")

    def atualizar_placar(self):
        self.label_placar.config(
            text=f"Placar - {self.lutador1.nome}: {self.lutador1.vitorias} | {self.lutador2.nome}: {self.lutador2.vitorias}"
        )

    def trocar_imagem(self, lutador, acao):
        lutador.current_image = lutador.imagens[acao]
        self.canvas.itemconfig(lutador.image_obj, image=lutador.current_image)
        self.canvas.update()

    def mover_e_acao(self, lutador, direcao, acao):
        self.trocar_imagem(lutador, acao)
        for _ in range(10):
            self.canvas.move(lutador.image_obj, direcao, 0)
            self.canvas.update()
            time.sleep(0.02)
        for _ in range(10):
            self.canvas.move(lutador.image_obj, -direcao, 0)
            self.canvas.update()
            time.sleep(0.02)
        self.trocar_imagem(lutador, 'defesa')

    def luta(self, atacante, defensor):
        while self.lutador1.vida > 0 and self.lutador2.vida > 0:
            direcao = 10 if atacante == self.lutador1 else -10

            if atacante == self.lutador2:
                acao = random.choice(['ataque1', 'ataque2'])
            else:
                acao = 'ataque'

            self.mover_e_acao(atacante, direcao, acao)

            self.trocar_imagem(defensor, 'apanhando')
            time.sleep(0.2)

            dano = atacante.atacar(defensor)
            print(f"{atacante.nome} causou {dano} de dano em {defensor.nome}!")
            self.atualizar_vidas()

            self.trocar_imagem(defensor, 'defesa')

            if defensor.vida <= 0:
                atacante.vitorias += 1
                print(f"{atacante.nome} venceu a luta!")
                self.atualizar_placar()
                break

            atacante, defensor = defensor, atacante
            time.sleep(0.5)

        if self.lutador1.vitorias == 2:
            self.fim_de_jogo(self.lutador1)
        elif self.lutador2.vitorias == 2:
            self.fim_de_jogo(self.lutador2)
        else:
            self.lutador1.resetar()
            self.lutador2.resetar()
            self.atualizar_vidas()
            self.btn_iniciar.config(state='normal')

    def fim_de_jogo(self, vencedor):
        msg = f"{vencedor.nome} é o Campeão!"
        print(msg)
        messagebox.showinfo("Fim de Jogo", msg)
        self.btn_iniciar.config(state='disabled')
        self.btn_reiniciar.config(state='normal')

    def reiniciar_jogo(self):
        self.lutador1.vitorias = 0
        self.lutador2.vitorias = 0
        self.lutador1.resetar()
        self.lutador2.resetar()
        self.atualizar_vidas()
        self.atualizar_placar()
        self.btn_iniciar.config(state='normal')
        self.btn_reiniciar.config(state='disabled')

    def iniciar_luta(self):
        self.btn_iniciar.config(state='disabled')

        if random.choice([True, False]):
            atacante = self.lutador1
            defensor = self.lutador2
        else:
            atacante = self.lutador2
            defensor = self.lutador1

        thread_luta = threading.Thread(target=self.luta, args=(atacante, defensor))
        thread_luta.start()

if __name__ == "__main__":
    resposta = input("Quer começar a luta? (s/n): ").strip().lower()
    if resposta != 's':
        print("Jogo não iniciado. Até a próxima!")
    else:
        root = tk.Tk()
        jogo = JogoLutaGUI(root)
        root.mainloop()
