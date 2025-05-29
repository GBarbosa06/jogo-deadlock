import threading
import time
import keyboard

anim = threading.Semaphore(1)
som = threading.Semaphore(1)

# Dicionário de teclas por jogador
controles = {
    'jogador1' :{
        'a': 'Soco',
        's': 'Chute',
        'd': 'Especial'
    },
    'jogador2' :{
        'j': 'Soco',
        'k': 'Chute',
        'l': 'Especial'
    }
}

# Agora há uma ordem fixa, sempre pega anim primeiro e depois som
def acao_jogador(nome, teclas):
    print(f"{nome} entrou no jogo!")
    while True:
        for tecla, acao in teclas.items():
            if keyboard.is_pressed(tecla):
                print(f"[{nome}] tentando executar: {acao}!")
                anim.acquire()
                print(f"[{nome}] executou: {acao}!")
                time.sleep(0.3) # Simula o tempo de execução da ação

                print(f"[{nome}] tentando pegar som para {acao}")
                som.acquire()
                print(f"[{nome}] pegou som")

                print(f"[{nome}] executando {acao}!")
                time.sleep(1)  # Simula duração da ação

                # Solta recursos na ordem inversa
                som.release()
                anim.release()
                time.sleep(0.3)  # Evita flood

# Agora ambos os jogadores seguem a mesma ordem: anim → som
# Se o anim estiver ocupado, ninguém pega o som antes

# Threads para cada jogador
j1 = threading.Thread(target=acao_jogador, args=('Jogador 1', controles['jogador1']))
j2 = threading.Thread(target=acao_jogador, args=('Jogador 2', controles['jogador2']))

# Inicia as threads
j1.start()
j2.start()

# Espera as threads terminarem (nunca vão terminar nesse caso)
j1.join()
j2.join()

