JOGO DA VELHA COM IA (MINIMAX E PODA ALFA-BETA)
​Documentacao do projeto de Inteligencia Artificial para o jogo da velha imbativel.
​=============================================
​RECURSOS PRINCIPAIS
=============================================

​Agente Imbatível: Garantia matemática de vitória ou empate em qualquer cenário de jogo.

​Poda Alfa-Beta Opcional: Permite ativar ou desativar a poda para comparar o tempo de processamento entre o Minimax puro e a versão otimizada.

​Métricas de Desempenho: Exibição em tempo real do tempo de cálculo (em segundos) que a IA leva para tomar uma decisão.
​Múltiplos Modos de Jogo:
​Opcao 1: Humano (X) vs Agente IA (O)
​Opcao 2: Agente IA (X) vs Humano (O)
​Opcao 3: Agente IA (X) vs Agente IA (O)
​Interface via Terminal: Tabuleiro estilizado com cores, painéis e validação de entradas humanas.

​Bateria de Testes Automatizada: Script de testes que simula exaustivamente todas as partidas possíveis para provar a invencibilidade do agente.

​=============================================

2. PRÉ-REQUISITOS
​Python 3.8 ou superior
​Gerenciador de pacotes pip

​=============================================

3. INSTALAÇÃO E CONFIGURAÇÃO


​Passo 1: Clonar ou baixar o repositório
git clone https://github.com/GiovanaDiglianne/jogo-da-velha-minimax.git

cd jogo-da-velha-minimax

​Passo 2: Criar e ativar um ambiente virtual (Opcional, mas recomendado)

​No Linux ou macOS:
python3 -m venv venv
source venv/bin/activate

​No Windows:
python -m venv venv
venv\Scripts\activate

​Passo 3: Instalar as dependências
pip install rich

​=============================================

4. ESTRUTURA DO PROJETO

​agente_jogo_velha.py : Logica do jogo, algoritmo Minimax, Poda Alfa-Beta e Testes

main.py              : Interface grafica no terminal (Rich) e loop principal

README.md            : Documentacao do projeto

​=============================================

5. COMO EXECUTAR O JOGO

​Para iniciar o jogo interativo no terminal, execute o comando:
​python main.py

​Fluxo durante a execucao:

​Escolha o modo de jogo (Opcao 1, 2 ou 3).

​Selecione se deseja usar a Poda Alfa-Beta ('s' para sim / 'n' para nao).

​No turno do Humano: Digite o numero da posicao desejada (de 1 a 9).

​No turno da IA: O sistema exibira o tempo exacto de calculo da jogada.

​=============================================

6. EXECUTANDO OS TESTES AUTOMATIZADOS


​Para rodar o teste de sanidade e simular todas as combinações de jogadas possíveis:
​python agente_jogo_velha.py

​Resultado esperado:
Agente jogando como 'X': 1312 vitórias, 4608 empates, 0 derrotas (de 5920 partidas simuladas)

Agente jogando como 'O': 0 vitórias, 2364 empates, 0 derrotas (de 2364 partidas simuladas)

​Teste OK: o agente nunca perde, em nenhum cenário possível.

​=============================================

7. ESTRUTURA LÓGICA DO TABULEIRO
​As posicoes para jogada correspondem aos numeros de 1 a 9:
​1 | 2 | 3
---+---+---
4 | 5 | 6
---+---+---
7 | 8 | 9

​=============================================

8. TECNOLOGIAS UTILIZADAS
​Linguagem: Python 3
​Interface CLI: Biblioteca Rich
​Algoritmos: Minimax com Poda Alfa-Beta