"""
agente_jogo_velha.py
Implementação de um agente de jogo da velha (tic-tac-toe) usando o algoritmo
Minimax com poda Alfa-Beta. O agente é projetado para nunca perder, jogando
como 'X' ou 'O', dependendo da configuração inicial.

Responsabilidades cobertas:
- Função de busca Minimax
- Poda Alfa-Beta
- Função de avaliação/heurística
- Teste de tomada de decisão (agente nunca perde)

Representação de estado adotada:
- Uma lista de 9 posições (índices 0 a 8), representando o tabuleiro assim:

    0 | 1 | 2
    3 | 4 | 5
    6 | 7 | 8

- Cada posição contém 'X', 'O' ou ' ' (espaço vazio).

"""

from typing import List, Optional

Tabuleiro = List[str]

# Todas as combinações de índices que formam uma linha vitoriosa
LINHAS_VITORIA = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
    (0, 4, 8), (2, 4, 6),             # diagonais
]


def verificar_vencedor(tab: Tabuleiro) -> Optional[str]:
    """
    Verifica o estado atual do tabuleiro.
    Retorna:
        'X'      -> se X venceu
        'O'      -> se O venceu
        'Empate' -> se o tabuleiro está cheio e ninguém venceu
        None     -> se o jogo ainda não terminou
    """
    for a, b, c in LINHAS_VITORIA:
        if tab[a] != ' ' and tab[a] == tab[b] == tab[c]:
            return tab[a]

    if ' ' not in tab:
        return 'Empate'

    return None


def jogadas_disponiveis(tab: Tabuleiro) -> List[int]:
    """Retorna os índices das casas vazias (o espaço de ações do agente)."""
    return [i for i, casa in enumerate(tab) if casa == ' ']


def avaliar(tab: Tabuleiro, profundidade: int) -> int:
    """
    Função de avaliação/heurística.

    Convenção: o agente (IA) sempre joga como 'X' (maximizador).
    O adversário joga como 'O' (minimizador).

    +10 - profundidade  -> X venceu (quanto mais rápido a vitória, melhor,
                             por isso subtraímos a profundidade)
    -10 + profundidade  -> O venceu (quanto mais rápido a derrota, pior)
    0                    -> empate ou jogo não terminado

    Usar a profundidade na pontuação é o que faz o agente preferir vencer
    o quanto antes e, quando a derrota é inevitável, adiá-la o máximo
    possível (útil contra um adversário que erra).
    """
    resultado = verificar_vencedor(tab)
    if resultado == 'X':
        return 10 - profundidade
    elif resultado == 'O':
        return -10 + profundidade
    else:
        return 0


def minimax(tab: Tabuleiro, profundidade: int, é_maximizando: bool,
            alfa: float, beta: float) -> int:
    """
    Algoritmo Minimax com poda Alfa-Beta.

    - é_maximizando=True  -> é a vez do agente ('X'), ele quer o MAIOR valor
    - é_maximizando=False -> é a vez do adversário ('O'), ele quer o MENOR valor

    alfa: melhor valor já garantido para o maximizador nesse ramo
    beta: melhor valor já garantido para o minimizador nesse ramo
    Quando beta <= alfa, o resto do ramo é ignorado (poda), porque o
    adversário nunca deixaria o jogo chegar até ali.
    """
    resultado = verificar_vencedor(tab)
    if resultado is not None:
        return avaliar(tab, profundidade)

    if é_maximizando:
        melhor_valor = float('-inf')
        for jogada in jogadas_disponiveis(tab):
            tab[jogada] = 'X'
            valor = minimax(tab, profundidade + 1, False, alfa, beta)
            tab[jogada] = ' '  # desfaz a jogada (backtracking)
            melhor_valor = max(melhor_valor, valor)
            alfa = max(alfa, melhor_valor)
            if beta <= alfa:
                break  # poda beta
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for jogada in jogadas_disponiveis(tab):
            tab[jogada] = 'O'
            valor = minimax(tab, profundidade + 1, True, alfa, beta)
            tab[jogada] = ' '
            melhor_valor = min(melhor_valor, valor)
            beta = min(beta, melhor_valor)
            if beta <= alfa:
                break  # poda alfa
        return melhor_valor


def melhor_jogada(tab: Tabuleiro, jogador: str) -> int:
    """
    Ponto de entrada principal para a interface (Integrante 2 vai chamar
    esta função). Recebe o tabuleiro atual e de quem é a vez ('X' ou 'O'),
    e retorna o ÍNDICE (0-8) da melhor jogada possível.
    """
    é_maximizando = (jogador == 'X')
    melhor_valor = float('-inf') if é_maximizando else float('inf')
    jogada_escolhida = -1

    for jogada in jogadas_disponiveis(tab):
        tab[jogada] = jogador
        valor = minimax(tab, 0, not é_maximizando, float('-inf'), float('inf'))
        tab[jogada] = ' '

        if é_maximizando and valor > melhor_valor:
            melhor_valor = valor
            jogada_escolhida = jogada
        elif not é_maximizando and valor < melhor_valor:
            melhor_valor = valor
            jogada_escolhida = jogada

    return jogada_escolhida


# ---------------------------------------------------------------------------
# TESTE: garantir que o agente NUNCA perde, jogando contra todas as
# respostas possíveis de um adversário (simulação exaustiva, não só alguns
# jogos aleatórios).
# ---------------------------------------------------------------------------

def _simular_todos_os_jogos(tab: Tabuleiro, jogador_atual: str,
                             agente: str) -> List[str]:
    """
    Gera recursivamente TODAS as partidas possíveis (o adversário tenta
    todas as jogadas dele, não só uma), com o agente sempre respondendo
    via melhor_jogada. Retorna a lista de resultados finais encontrados.
    """
    resultado = verificar_vencedor(tab)
    if resultado is not None:
        return [resultado]

    resultados = []
    if jogador_atual == agente:
        # agente joga com a IA
        jogada = melhor_jogada(tab, agente)
        tab[jogada] = agente
        proximo = 'O' if agente == 'X' else 'X'
        resultados += _simular_todos_os_jogos(tab, proximo, agente)
        tab[jogada] = ' '
    else:
        # adversário testa TODAS as jogadas possíveis dele
        adversario = 'O' if agente == 'X' else 'X'
        for jogada in jogadas_disponiveis(tab):
            tab[jogada] = adversario
            resultados += _simular_todos_os_jogos(tab, agente, agente)
            tab[jogada] = ' '

    return resultados


def testar_agente():
    """
    Executa a simulação exaustiva com o agente começando como 'X' e depois
    como 'O', e imprime um resumo. Se aparecer qualquer resultado de
    derrota do agente, o teste falha.
    """
    for agente in ('X', 'O'):
        tab = [' '] * 9
        inicia = 'X'  # X sempre começa, por convenção do jogo da velha
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
