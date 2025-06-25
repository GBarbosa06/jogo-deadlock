import threading
import time

# Classe que representa um lutador
class Lutador:
    def __init__(self, nome):
        # Inicializa o nome, vida e um lock para controle de acesso
        self.nome = nome
        self.vida = 100
        self.lock = threading.Lock()

    def atacar(self, oponente):
        # Método para atacar outro lutador
        print(f"{self.nome} tentando atacar {oponente.nome}...")

        # Bloqueia o próprio lock antes de tentar atacar
        with self.lock:
            print(f"{self.nome} bloqueou SEU PRÓPRIO lock.")
            time.sleep(1)  # Simula um atraso no golpe

            # Tenta bloquear o lock do oponente
            print(f"{self.nome} tentando bloquear o lock de {oponente.nome}...")
            with oponente.lock:  # Deadlock ocorre se o oponente já tiver bloqueado este lock
                print(f"{self.nome} ATACOU {oponente.nome}!")
                oponente.vida -= 10  # Reduz a vida do oponente
                print(f"{oponente.nome} agora tem {oponente.vida} de vida.")

# Função para iniciar a luta entre dois lutadores
def iniciar_luta(lutador1, lutador2):
    # Cria duas threads, uma para cada lutador atacar o outro
    t1 = threading.Thread(target=lutador1.atacar, args=(lutador2,))
    t2 = threading.Thread(target=lutador2.atacar, args=(lutador1,))

    # Inicia as threads
    t1.start()
    t2.start()

    # Aguarda as threads terminarem com um timeout
    t1.join(timeout=5)
    t2.join(timeout=5)

    # Mensagem final indicando que deadlock pode ter ocorrido
    print("Verificação final: Deadlock detectado se o programa travar ou não finalizar.")

# Ponto de entrada do programa
if __name__ == "__main__":
    # Cria dois lutadores
    lutador1 = Lutador("Lutador 1")
    lutador2 = Lutador("Lutador 2")

    # Inicia a luta entre os lutadores
    iniciar_luta(lutador1, lutador2)
