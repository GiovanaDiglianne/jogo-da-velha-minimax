from typing import List, Optional

Tabuleiro = List[str]

LINHAS_VITORIA = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
    (0, 4, 8), (2, 4, 6),             # diagonais
]

def verificar_vencedor(tab: Tabuleiro) -> Optional[str]:
    for a, b, c in LINHAS_VITORIA:
        if tab[a] != ' ' and tab[a] == tab[b] == tab[c]:
            return tab[a]

    if ' ' not in tab:
        return 'Empate'

    return None

def jogadas_disponiveis(tab: Tabuleiro) -> List[int]:
    return [i for i, casa in enumerate(tab) if casa == ' ']

def avaliar(tab: Tabuleiro, profundidade: int) -> int:
    resultado = verificar_vencedor(tab)
    if resultado == 'X':
        return 10 - profundidade
    elif resultado == 'O':
        return -10 + profundidade
    else:
        return 0

def minimax(tab: Tabuleiro, profundidade: int, é_maximizando: bool,
            alfa: float, beta: float, usar_poda: bool = True) -> int:
    resultado = verificar_vencedor(tab)
    if resultado is not None:
        return avaliar(tab, profundidade)

    if é_maximizando:
        melhor_valor = float('-inf')
        for jogada in jogadas_disponiveis(tab):
            tab[jogada] = 'X'
            valor = minimax(tab, profundidade + 1, False, alfa, beta, usar_poda)
            tab[jogada] = ' '
            melhor_valor = max(melhor_valor, valor)
            alfa = max(alfa, melhor_valor)
            if usar_poda and beta <= alfa:
                break 
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for jogada in jogadas_disponiveis(tab):
            tab[jogada] = 'O'
            valor = minimax(tab, profundidade + 1, True, alfa, beta, usar_poda)
            tab[jogada] = ' '
            melhor_valor = min(melhor_valor, valor)
            beta = min(beta, melhor_valor)
            if usar_poda and beta <= alfa:
                break
        return melhor_valor

def melhor_jogada(tab: Tabuleiro, jogador: str, usar_poda: bool = True) -> int:
    é_maximizando = (jogador == 'X')
    melhor_valor = float('-inf') if é_maximizando else float('inf')
    jogada_escolhida = -1

    for jogada in jogadas_disponiveis(tab):
        tab[jogada] = jogador
        valor = minimax(tab, 0, not é_maximizando, float('-inf'), float('inf'), usar_poda)
        tab[jogada] = ' '

        if é_maximizando and valor > melhor_valor:
            melhor_valor = valor
            jogada_escolhida = jogada
        elif not é_maximizando and valor < melhor_valor:
            melhor_valor = valor
            jogada_escolhida = jogada

    return jogada_escolhida

# TESTES

def _simular_todos_os_jogos(tab: Tabuleiro, jogador_atual: str,
                             agente: str) -> List[str]:
    resultado = verificar_vencedor(tab)
    if resultado is not None:
        return [resultado]

    resultados = []
    if jogador_atual == agente:
        jogada = melhor_jogada(tab, agente, True)
        tab[jogada] = agente
        proximo = 'O' if agente == 'X' else 'X'
        resultados += _simular_todos_os_jogos(tab, proximo, agente)
        tab[jogada] = ' '
    else:
        adversario = 'O' if agente == 'X' else 'X'
        for jogada in jogadas_disponiveis(tab):
            tab[jogada] = adversario
            resultados += _simular_todos_os_jogos(tab, agente, agente)
            tab[jogada] = ' '

    return resultados

def testar_agente():
    for agente in ('X', 'O'):
        tab = [' '] * 9
        inicia = 'X'
        resultados = _simular_todos_os_jogos(tab, inicia, agente)

        vitorias = resultados.count(agente)
        derrotas = resultados.count('O' if agente == 'X' else 'X')
        empates = resultados.count('Empate')

        print(f"Agente jogando como '{agente}': "
              f"{vitorias} vitórias, {empates} empates, {derrotas} derrotas "
              f"(de {len(resultados)} partidas simuladas)")

        assert derrotas == 0, f"FALHOU: agente perdeu jogando como {agente}!"

    print("\nTeste OK: o agente nunca perde, em nenhum cenário possível.")


if __name__ == "__main__":
    testar_agente()