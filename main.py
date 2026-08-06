import time

from agente_jogo_velha import melhor_jogada, verificar_vencedor, jogadas_disponiveis

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text

console = Console()

def limpar_tela():
    console.clear()

def imprimir_tabuleiro(tab):
    # Cria estrutura da tabela
    table = Table(show_header=False, show_lines=True, border_style="bright_black")
    
    table.add_column(justify="center", width=5)
    table.add_column(justify="center", width=5)
    table.add_column(justify="center", width=5)

    # Preenche a tabela iterando sobre as linhas e colunas
    for i in range(3):
        linha = []
        for j in range(3):
            indice = i * 3 + j
            
            # Formata a o jogo da velha baseado na ocupação da casa
            if tab[indice] == ' ':
                linha.append(f"[dim white]{indice + 1}[/dim white]")
            elif tab[indice] == 'X':
                linha.append("[bold red]X[/bold red]")
            else:
                linha.append("[bold cyan]O[/bold cyan]")
        table.add_row(*linha)
    
    painel = Panel(table, title="[bold green]Tabuleiro Atual[/bold green]", expand=False, border_style="green")
    console.print(painel)

def ler_jogada_humano(tab, jogador_atual) -> int:
    while True:
        opcoes_disponiveis = [str(i + 1) for i in jogadas_disponiveis(tab)]
        opcoes_formatadas = ", ".join(opcoes_disponiveis)
        
        texto_prompt = f"[bold yellow]Sua vez ({jogador_atual})![/bold yellow] Posições disponíveis ([cyan]{opcoes_formatadas}[/cyan])"
        escolha = IntPrompt.ask(texto_prompt)
        indice = escolha - 1
        
        # Valida se a escolha do usuário está entre as opções mapeadas
        if str(escolha) not in opcoes_disponiveis:
            if indice < 0 or indice > 8:
                console.print("[bold red]Erro:[/bold red] Posição inválida! Escolha um dos números listados.")
            else:
                console.print("[bold red]Erro:[/bold red] Essa casa já está ocupada! Escolha outra.")
        else:
            return indice

def jogar():
    limpar_tela()
    
    titulo = Text("JOGO DA VELHA - MINIMAX", justify="center", style="bold magenta")
    console.print(Panel(titulo, expand=False, border_style="magenta"))
    
    # Menu de seleção dos modos
    console.print("\n[bold]Escolha o modo de jogo:[/bold]")
    console.print("1. Você ([bold red]'X'[/bold red]) vs Agente IA ([bold cyan]'O'[/bold cyan])")
    console.print("2. Agente IA ([bold red]'X'[/bold red]) vs Você ([bold cyan]'O'[/bold cyan])")
    console.print("3. Agente IA ([bold red]'X'[/bold red]) vs Agente IA ([bold cyan]'O'[/bold cyan])")
    
    modo = Prompt.ask("\n[bold]Digite a opção desejada[/bold]", choices=["1", "2", "3"])

    usar_poda_input = Prompt.ask("\n[bold]Deseja utilizar a Poda Alfa-Beta na IA?[/bold]", choices=["s", "n"], default="s")
    usar_poda = (usar_poda_input == 's')

    # Configuração dos jogadores com base no modo selecionado
    jogador_X_is_ia = False
    jogador_O_is_ia = False

    if modo == '1':
        jogador_O_is_ia = True
    elif modo == '2':
        jogador_X_is_ia = True
    elif modo == '3':
        jogador_X_is_ia = True
        jogador_O_is_ia = True

    tabuleiro = [' '] * 9
    jogador_atual = 'X'
    
    # Turnos da partida
    while True:
        limpar_tela()
        status_poda = "[bold green]Ativada[/bold green]" if usar_poda else "[bold red]Desativada[/bold red]"
        console.print(f"[bold]Modo:[/bold] Opção {modo} | [bold]Poda Alfa-Beta:[/bold] {status_poda}\n")
        
        imprimir_tabuleiro(tabuleiro)
        
        # Verifica se o turno atual pertence a um agente de IA
        is_ia_turn = (jogador_atual == 'X' and jogador_X_is_ia) or \
                     (jogador_atual == 'O' and jogador_O_is_ia)
        
        cor_jogador = "[bold red]" if jogador_atual == 'X' else "[bold cyan]"
        
        if is_ia_turn:
            # Turno da Inteligência Artificial
            acao = "pensando" if modo != '3' else "calculando"
            console.print(f"{cor_jogador}Agente IA ({jogador_atual})[/] está {acao}...")
            
            # Marca o tempo
            tempo_inicio = time.perf_counter()
            jogada = melhor_jogada(tabuleiro, jogador_atual, usar_poda)
            tempo_fim = time.perf_counter()
            
            tempo_gasto = tempo_fim - tempo_inicio
            console.print(f"⏱️  Tempo de cálculo: [bold yellow]{tempo_gasto:.4f}[/bold yellow] segundos")
            
            if modo == '3':
                time.sleep(2.5)
            else:
                time.sleep(2.5)
        else:
            # Turno do jogador humano
            jogada = ler_jogada_humano(tabuleiro, jogador_atual)

        # Aplica a ação escolhida (IA ou Humano) no tabuleiro
        tabuleiro[jogada] = jogador_atual

        # Verifica se o jogo chegou ao fim
        resultado = verificar_vencedor(tabuleiro)
        if resultado is not None:
            limpar_tela()
            imprimir_tabuleiro(tabuleiro)
            console.print("\n" + "="*40)
            
            if resultado == 'Empate':
                console.print("[bold yellow]🤝 O jogo terminou em EMPATE![/bold yellow]")
            else:
                cor_vencedor = "red" if resultado == 'X' else "cyan"
                console.print(f"[bold {cor_vencedor}]🏆 Temos um vencedor: JOGADOR '{resultado}'![/]")
            console.print("="*40 + "\n")
            break

        # Alternância de turnos
        jogador_atual = 'O' if jogador_atual == 'X' else 'X'


while True:
    jogar()
    jogar_novamente = Prompt.ask("[bold]Deseja jogar novamente?[/bold]", choices=["s", "n"], default="s")
    if jogar_novamente != 's':
        console.print("[bold magenta]Obrigado por jogar! Encerrando...[/bold magenta]")
        break