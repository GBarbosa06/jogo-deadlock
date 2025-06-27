import threading
import time
import random
import tkinter as tk
from tkinter import Canvas, PhotoImage

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
        self.lock = threading.Lock()  # Lock para proteger acesso à variável vida

    def resetar(self):
        with self.lock:  # Bloqueia para garantir que só uma thread modifique vida por vez
            self.vida = 100
            self.current_image = self.imagens['defesa']

    def atacar(self, oponente, semaforo):
        # Semáforo controla a vez de atacar
        # acquire() tenta "pegar" o semáforo. Se já estiver com outra thread, espera.
        semaforo.acquire()
        try:
            # Quando chega aqui, essa thread tem permissão exclusiva para atacar
            dano = random.randint(10, 30)

            # Lock para garantir que a vida do oponente seja alterada sem interferência
            with oponente.lock:
                oponente.vida -= dano
                if oponente.vida < 0:
                    oponente.vida = 0

            print(f"{self.nome} causou {dano} de dano em {oponente.nome}!")
            return dano
        finally:
            # Libera o semáforo para a outra thread poder atacar
            semaforo.release()

class JogoLutaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Luta - Semáforo e Threads")

        self.canvas = Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack()

        # Imagens dos lutadores (aqui só o caminho, tem que ter no seu diretório)
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

        # Cria o semáforo para controlar acesso exclusivo aos ataques
        # Valor 1 significa que só uma thread pode "segurar" o semáforo por vez
        self.semaforo = threading.Semaphore(1)

        # Evento para sinalizar o fim da luta e parar as threads de ataque
        self.fim_luta = threading.Event()

    def atualizar_vidas(self):
        self.label_vida1.config(text=f"{self.lutador1.nome}: {self.lutador1.vida} HP")
        self.label_vida2.config(text=f"{self.lutador2.nome}: {self.lutador2.vida} HP")

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

    def thread_atacar(self, atacante, defensor, direcao):
        # Enquanto a luta não terminar, os lutadores continuam tentando atacar
        while not self.fim_luta.is_set():
            # Faz a animação do ataque
            self.mover_e_acao(atacante, direcao, 'ataque' if atacante == self.lutador1 else random.choice(['ataque1', 'ataque2']))
            self.trocar_imagem(defensor, 'apanhando')
            time.sleep(0.2)

            # Tenta atacar — aqui é onde o semáforo entra
            dano = atacante.atacar(defensor, self.semaforo)
            self.atualizar_vidas()

            self.trocar_imagem(defensor, 'defesa')

            # Se vida do defensor zerar, acaba a luta
            if defensor.vida <= 0:
                atacante.vitorias += 1
                print(f"{atacante.nome} venceu a luta!")
                self.atualizar_placar()
                self.fim_luta.set()  # Sinaliza fim da luta para as threads
                break

            time.sleep(0.5)

    def iniciar_luta(self):
        self.btn_iniciar.config(state='disabled')
        self.fim_luta.clear()

        self.lutador1.resetar()
        self.lutador2.resetar()
        self.atualizar_vidas()

        direcao1 = 10
        direcao2 = -10

        # Cria 2 threads, uma para cada lutador atacar
        t1 = threading.Thread(target=self.thread_atacar, args=(self.lutador1, self.lutador2, direcao1))
        t2 = threading.Thread(target=self.thread_atacar, args=(self.lutador2, self.lutador1, direcao2))

        t1.start()
        t2.start()

        # Thread que espera as outras terminarem pra liberar o botão reiniciar
        def esperar_threads():
            t1.join()
            t2.join()
            self.btn_reiniciar.config(state='normal')

        threading.Thread(target=esperar_threads).start()

    def reiniciar_jogo(self):
        # Para a luta ativa
        self.fim_luta.set()
        self.lutador1.vitorias = 0
        self.lutador2.vitorias = 0
        self.lutador1.resetar()
        self.lutador2.resetar()
        self.atualizar_vidas()
        self.atualizar_placar()
        self.btn_iniciar.config(state='normal')
        self.btn_reiniciar.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoLutaGUI(root)
    root.mainloop()
