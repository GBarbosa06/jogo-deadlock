import threading
import time
import random
import keyboard

# Classe que representa um lutador no jogo
class Lutador:
    def __init__(self, nome, tecla_ataque):
        # Inicializa o nome, vida, tecla de ataque, número de vitórias e um lock para sincronização
        self.nome = nome
        self.vida = 100
        self.tecla = tecla_ataque
        self.vitorias = 0
        self.lock = threading.Lock()

    def resetar(self):
        # Reseta a vida do lutador para 100, garantindo sincronização com o lock
        with self.lock:
            self.vida = 100

    def atacar(self, oponente, semaforo):
        # Tenta adquirir o semáforo para realizar o ataque
        if semaforo.acquire(blocking=False):  # Tenta atacar se for sua vez
            try:
                # Calcula um dano aleatório entre 10 e 30
                dano = random.randint(10, 30)
                # Adquire o lock do oponente para modificar sua vida
                with oponente.lock:
                    oponente.vida = max(oponente.vida - dano, 0)  # Garante que a vida não fique negativa
                print(f"\n{self.nome} acertou um golpe! -{dano} de vida em {oponente.nome}")
            finally:
                # Libera o semáforo após o ataque
                semaforo.release()
        else:
            # Caso o semáforo não esteja disponível, o lutador tentou atacar fora da vez
            print(f"{self.nome} tentou atacar fora da vez!")

# Função para exibir as vidas dos lutadores no terminal
def mostrar_vidas(l1, l2):
    print(f"\n{l1.nome}: {l1.vida} HP | {l2.nome}: {l2.vida} HP")

# Função que monitora as teclas pressionadas para realizar ataques
def monitorar_teclas(lutador, oponente, semaforo, fim_luta):
    while not fim_luta.is_set():  # Continua enquanto a luta não terminou
        if keyboard.is_pressed(lutador.tecla):  # Verifica se a tecla de ataque do lutador foi pressionada
            lutador.atacar(oponente, semaforo)  # Realiza o ataque
            mostrar_vidas(lutador, oponente)  # Mostra as vidas atualizadas
            if oponente.vida <= 0:  # Verifica se o oponente foi derrotado
                print(f"\n{lutador.nome} venceu a luta!")
                lutador.vitorias += 1  # Incrementa o número de vitórias do lutador
                fim_luta.set()  # Sinaliza o fim da luta
            time.sleep(0.5)  # Evita múltiplos ataques com uma única tecla pressionada

# Função principal que gerencia o jogo
def jogo():
    # Cria dois lutadores com nomes e teclas de ataque
    l1 = Lutador("Player 1 (A)", 'a')
    l2 = Lutador("Player 2 (L)", 'l')
    semaforo = threading.Semaphore(1)  # Semáforo para controlar a vez de ataque
    
    while True:  # Loop principal do jogo
        l1.resetar()  # Reseta a vida do Player 1
        l2.resetar()  # Reseta a vida do Player 2
        fim_luta = threading.Event()  # Evento para sinalizar o fim da luta

        print("\nNova Luta! Use 'A' para o Player 1 e 'L' para o Player 2!")
        mostrar_vidas(l1, l2)  # Exibe as vidas iniciais dos lutadores

        # Cria threads para monitorar as teclas de ataque de cada lutador
        t1 = threading.Thread(target=monitorar_teclas, args=(l1, l2, semaforo, fim_luta))
        t2 = threading.Thread(target=monitorar_teclas, args=(l2, l1, semaforo, fim_luta))
        t1.start()  # Inicia a thread do Player 1
        t2.start()  # Inicia a thread do Player 2

        t1.join()  # Aguarda o término da thread do Player 1
        t2.join()  # Aguarda o término da thread do Player 2

        # Exibe o placar após o término da luta
        print(f"\nPlacar: {l1.nome} {l1.vitorias} x {l2.vitorias} {l2.nome}")
        print("Pressione ENTER para lutar novamente ou ESC para sair.")
        while True:  # Aguarda a entrada do usuário para continuar ou sair
            if keyboard.is_pressed('enter'):  # Verifica se a tecla ENTER foi pressionada
                break  # Inicia uma nova luta
            if keyboard.is_pressed('esc'):  # Verifica se a tecla ESC foi pressionada
                print("Saindo do jogo...")
                return  # Sai do jogo
            time.sleep(0.1)  # Pequeno delay para evitar alta utilização de CPU

# Ponto de entrada do programa
if __name__ == "__main__":
    jogo()  # Inicia o jogo
