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

def acao_jogador(nome, teclas, primeiro_recurso, segundo_recurso):
    print(f"{nome} entrou no jogo!")
    while True:
        for tecla, acao in teclas.items():
            if keyboard.is_pressed(tecla):
                print(f"[{nome}] tentando executar: {acao}!")
                primeiro_recurso.acquire()
                print(f"[{nome}] executou: {acao}!")
                time.sleep(0.5) # Simula o tempo de execução da ação

                print(f"[{nome}] tentando pegar {segundo_recurso} para {acao}")
                segundo_recurso.acquire()
                print(f"[{nome}] pegou {segundo_recurso}")

                print(f"[{nome}] executando {acao}!")
                time.sleep(1)  # Simula duração da ação

                # Solta recursos na ordem inversa
                segundo_recurso.release()
                primeiro_recurso.release()
                time.sleep(0.3)  # Evita flood

#threads para cada jogador
j1 = threading.Thread(target=acao_jogador, args=('Jogador 1', controles['jogador1'], anim, som))
j2 = threading.Thread(target=acao_jogador, args=('Jogador 2', controles['jogador2'], som, anim))

# Iniciaas threads
j1.start()
j2.start()

# Espera as threads terminarem (nunca vão terminar nesse caso)
j1.join()
j2.join()