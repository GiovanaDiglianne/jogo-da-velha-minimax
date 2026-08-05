import time
import os

from agente_jogo_velha import melhor_jogada, verificar_vencedor, jogadas_disponiveis

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tabuleiro(tab):
    print("\nTabuleiro Atual:")
    for i in range(3):
        linha = []
        for j in range(3):
            indice = i * 3 + j

            if tab[indice] == ' ':
                linha.append(str(indice + 1))
            else:
                linha.append(tab[indice])
        
        print(f" {linha[0]} | {linha[1]} | {linha[2]} ")
        if i < 2:
            print("---+---+---")
    print()

def ler_jogada_humano(tab) -> int:
    while True:
        try:
            escolha = int(input("Sua vez! Escolha uma posição (1-9): "))
            indice = escolha - 1
            
            if indice < 0 or indice > 8:
                print("Posição inválida! Escolha um número de 1 a 9.")
            elif indice not in jogadas_disponiveis(tab):
                print("Essa casa já está ocupada! Escolha outra.")
            else:
                return indice
        except ValueError:
            print("Entrada inválida! Por favor, digite um número.")

def jogar():
    limpar_tela()
    print("=======================================")
    print("      JOGO DA VELHA - MINIMAX          ")
    print("=======================================")
    print("Escolha o modo de jogo:")
    print("1. Você ('X') vs Agente IA ('O')")
    print("2. Agente IA ('X') vs Você ('O')")
    print("3. Agente IA ('X') vs Agente IA ('O')")
    
    modo = ""
    while modo not in ['1', '2', '3']:
        modo = input("Digite a opção desejada (1, 2 ou 3): ")

    # Configuração dos jogadores baseada no modo escolhido
    jogador_X_is_ia = False
    jogador_O_is_ia = False

    if modo == '1':
        jogador_O_is_ia = True
    elif modo == '2':
        jogador_X_is_ia = True
    elif modo == '3':
        jogador_X_is_ia = True
        jogador_O_is_ia = True

    # Inicia o tabuleiro vazio
    tabuleiro = [' '] * 9
    jogador_atual = 'X'
    
    while True:
        limpar_tela()
        print(f"Modo escolhido: Opção {modo}")
        imprimir_tabuleiro(tabuleiro)
        
        is_ia_turn = (jogador_atual == 'X' and jogador_X_is_ia) or \
                     (jogador_atual == 'O' and jogador_O_is_ia)
        
        if is_ia_turn:
            print(f"Agente IA ({jogador_atual}) está " + ("pensando..." if modo != '3' else "calculando..."))
            if modo == '3':
                time.sleep(1)
            
            jogada = melhor_jogada(tabuleiro, jogador_atual)
        else:
            print(f"Vez do Humano ({jogador_atual})")
            jogada = ler_jogada_humano(tabuleiro)

        tabuleiro[jogada] = jogador_atual

        resultado = verificar_vencedor(tabuleiro)
        if resultado is not None:
            limpar_tela()
            imprimir_tabuleiro(tabuleiro)
            print("=======================================")
            if resultado == 'Empate':
                print("O jogo terminou em EMPATE!")
            else:
                print(f"Temos um vencedor: JOGADOR '{resultado}'!")
            print("=======================================")
            break

        jogador_atual = 'O' if jogador_atual == 'X' else 'X'




# Executa jogo
while True:
    jogar()
    jogar_novamente = input("\nDeseja jogar novamente? (s/n): ").strip().lower()
    if jogar_novamente != 's':
        print("Obrigado por jogar! Encerrando...")
        break