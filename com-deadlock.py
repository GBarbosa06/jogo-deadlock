
    def atualizar_vida(self):
        self.canvas.itemconfig(self.text, text=f"{self.nome}: {self.vida} HP")

    def atacar(self, oponente):
        print(f"{self.nome} tentando atacar {oponente.nome}...")
        with self.lock:
            print(f"{self.nome} bloqueou seu próprio lock e tenta bloquear {oponente.nome}")
            time.sleep(1)  # Simula tempo de ataque
            with oponente.lock:
                print(f"{self.nome} atacou {oponente.nome}!")
                oponente.vida -= 10
                oponente.atualizar_vida()

def luta(lutador1, lutador2):
    for _ in range(5):
        lutador1.atacar(lutador2)
        time.sleep(0.1)

def iniciar_luta():
    btn_iniciar.config(state='disabled')
    t1 = threading.Thread(target=luta, args=(lutador1, lutador2))
    t2 = threading.Thread(target=luta, args=(lutador2, lutador1))
    t1.start()
    t2.start()

# Interface gráfica
root = tk.Tk()
root.title("Deadlock na Luta")

canvas = Canvas(root, width=400, height=200, bg="white")
canvas.pack()

lutador1 = Lutador("Lutador 1", 100, 50, canvas)
lutador2 = Lutador("Lutador 2", 300, 50, canvas)

btn_iniciar = tk.Button(root, text="Iniciar Luta", command=iniciar_luta)
btn_iniciar.pack(pady=10)

root.mainloop()
