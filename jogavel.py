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
        
        self.pode_atacar1 = True
        self.pode_atacar2 = True

        self.barra_cd1 = self.canvas.create_rectangle(90, 250, 190, 260, fill="green")
        self.barra_cd2 = self.canvas.create_rectangle(510, 250, 610, 260, fill="green")


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

    def atualizar_barra_cooldown(self, lutador, duracao, barra_id):
        start_time = time.time()
        end_time = start_time + duracao

        while time.time() < end_time:
            elapsed = time.time() - start_time
            proporcao = elapsed / duracao
            if proporcao > 1:
                proporcao = 1

            if lutador == self.lutador1:
                self.canvas.coords(barra_id, 90, 250, 90 + 100 * proporcao, 260)
            else:
                self.canvas.coords(barra_id, 510, 250, 510 + 100 * proporcao, 260)

            self.canvas.update()
            time.sleep(0.01)

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

    # ... (mantenha todas as suas imports e classes Lutador e JogoLutaGUI acima)

    def iniciar_luta(self):
        self.btn_iniciar.config(state='disabled')
        self.lutador1.resetar()
        self.lutador2.resetar()
        self.atualizar_vidas()

        # Começa a contagem
        threading.Thread(target=self.contagem_inicio).start()

    def contagem_inicio(self):
        textos = ["3", "2", "1", "LUTA!"]
        texto_id = None

        for txt in textos:
            if texto_id:
                self.canvas.delete(texto_id)
            texto_id = self.canvas.create_text(300, 50, text=txt, font=("Helvetica", 32, "bold"), fill="red")
            self.canvas.update()
            time.sleep(1)
        print("=== LUTA INICIADA ===\n")

        self.canvas.delete(texto_id)

        # Ativa os controles
        self.root.bind("<a>", self.ataque_lutador1)
        self.root.bind("<l>", self.ataque_lutador2)


    def ataque_lutador1(self, event):
        if self.pode_atacar1 and self.lutador1.vida > 0 and self.lutador2.vida > 0:
            self.pode_atacar1 = False
            self.executar_ataque(self.lutador1, self.lutador2, direcao=10, acao='ataque')
            cooldown = random.uniform(0.3, 0.8)
            threading.Timer(cooldown, lambda: setattr(self, 'pode_atacar1', True)).start()
            cooldown = random.uniform(0.3, 0.8)
            threading.Thread(target=self.atualizar_barra_cooldown, args=(self.lutador1, cooldown, self.barra_cd1)).start()


    def ataque_lutador2(self, event):
        if self.pode_atacar2 and self.lutador1.vida > 0 and self.lutador2.vida > 0:
            self.pode_atacar2 = False
            acao = random.choice(['ataque1', 'ataque2'])
            self.executar_ataque(self.lutador2, self.lutador1, direcao=-10, acao=acao)
            cooldown = random.uniform(0.3, 0.8)
            threading.Timer(cooldown, lambda: setattr(self, 'pode_atacar2', True)).start()
            cooldown = random.uniform(0.3, 0.8)
            threading.Thread(target=self.atualizar_barra_cooldown, args=(self.lutador2, cooldown, self.barra_cd2)).start()



    def executar_ataque(self, atacante, defensor, direcao, acao):
        def animar():
            self.mover_e_acao(atacante, direcao, acao)
            self.trocar_imagem(defensor, 'apanhando')
            time.sleep(0.2)
            dano = atacante.atacar(defensor)
            self.atualizar_vidas()
            self.trocar_imagem(defensor, 'defesa')
            print(f"{atacante.nome} causou {dano} de dano em {defensor.nome}!")
            print(f"{defensor.nome} agora tem {max(0, defensor.vida)} HP\n")

            if defensor.vida <= 0:
                atacante.vitorias += 1
                self.atualizar_placar()
                print(f"{atacante.nome} venceu este round!")
                print(f"Placar: {self.lutador1.nome} {self.lutador1.vitorias} x {self.lutador2.vitorias} {self.lutador2.nome}\n")

                if atacante.vitorias == 2:
                    self.fim_de_jogo(atacante)
                else:
                    self.root.unbind("<a>")
                    self.root.unbind("<l>")
                    self.canvas.create_text(300, 50, text="Round Encerrado!", font=("Helvetica", 24, "bold"), fill="blue")
                    self.canvas.update()
                    time.sleep(2)
                    self.canvas.delete("all")
                    self.lutador1.image_obj = self.canvas.create_image(self.lutador1.x, self.lutador1.y, image=self.lutador1.current_image)
                    self.lutador2.image_obj = self.canvas.create_image(self.lutador2.x, self.lutador2.y, image=self.lutador2.current_image)
                    self.barra_cd1 = self.canvas.create_rectangle(90, 250, 190, 260, fill="green")
                    self.barra_cd2 = self.canvas.create_rectangle(510, 250, 610, 260, fill="green")
                    self.lutador1.resetar()
                    self.lutador2.resetar()
                    self.atualizar_vidas()
                    self.iniciar_luta()


        threading.Thread(target=animar).start()


if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoLutaGUI(root)
    root.mainloop()


# Esse jogo agora funciona usando A e L para atacar os lutadores, e inclui uma contagem regressiva antes do início da luta.