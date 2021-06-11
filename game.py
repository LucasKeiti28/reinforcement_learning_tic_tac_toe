# Algoritmo de aprendizagem por reforço simples para aprender a jogar o tic-tac-toe

# Value Function: é a medida que considera a probabilidade de todas as possíveis recompensas de um estado.
# A Value Function é uma forma eficiente e rápida de buscar a árvore do jogo em busca do melhor caminho para chegar a recompensa.
# Update rule: V(s) = V(s) + alpha*(V(s') - V(s))
# s  = estado corrente
# s' = próximo estado
# s representa cada estado que nós encontramos em um episódio e por isso precisamos do histórico de estados em um episódio
# Estados terminais não são atualizados, uma vez que não existe próximo estado
# Treinamos o algoritmo sobre vários episódios até encontrar o melhor valor de alpha
# A fórmula acima é similar à fórmula do gradient descent em aprendizagem supervisionada

# Epsilon-greedy policy:
#   action|s = argmax[sobre todas as ações possíveis do estado s]{ V(s) }  if rand > epsilon
#   action|s = selecione ação aleatória de possíveis ações do estado s if rand < epsilon
#
# Algumas dicas de melhorias no algoritmo:
#
# Atualmente, ambos os agentes usam a mesma estratégia de aprendizagem enquanto jogam um contra o outro.
# E se eles tiverem diferentes taxas de aprendizado?
# E se eles tiverem diferentes epsilons? (probabilidade de explorar)
# Quem convergirá mais rápido?
# E se um agente não aprender?
# Uma pergunta filosófica interessante: se não há ninguém para desafiá-lo, você pode alcançar seu potencial máximo?
from agent import Agent
from environment import Environment
from human import Human
from builtins import range, input
import numpy as np

# Imports

# Variável para ajudar a definir o total de estados possíveis
LENGTH = 3

# Função recursiva que retornará todos os estados possíveis (como ints) e quem é o vencedor correspondente para esses estados (se houver)
# (i, j) se refere à próxima célula no tabuleiro para permutar (precisamos tentar -1, 0, 1)
# jogos impossíveis são ignorados, ou seja, 3x e 3o em uma linha simultaneamente, pois isso nunca acontecerá em um jogo real


def get_state_hash_and_winner(env, i=0, j=0):
    results = []

    for v in (0, env.x, env.o):
        env.board[i, j] = v
        if j == 2:
            if i == 2:
                state = env.get_state()
                ended = env.game_over(force_recalculate=True)
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += get_state_hash_and_winner(env, i + 1, 0)
        else:
            results += get_state_hash_and_winner(env, i, j + 1)

    return results

# Inicializa os estados de x com a função valor


def initialV_x(env, state_winner_triples):
    # if x wins, V(s) = 1
    # if x loses or draw, V(s) = 0
    # otherwise, V(s) = 0.5
    V = np.zeros(env.num_states)
    for state, winner, ended in state_winner_triples:
        if ended:
            if winner == env.x:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V

# Inicializa os estados de o com a função valor


def initialV_o(env, state_winner_triples):
    V = np.zeros(env.num_states)
    for state, winner, ended in state_winner_triples:
        if ended:
            if winner == env.o:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V

# Loop até o jogo terminar


def play_game(p1, p2, env, draw=False):
    current_player = None
    while not env.game_over():
        # Alternar entre jogadores
        # p1 sempre começa primeiro
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        # Desenha o tabuleiro antes que o usuário faça um movimento
        if draw:
            if draw == 1 and current_player == p1:
                env.draw_board()
            if draw == 2 and current_player == p2:
                env.draw_board()

        # Jogador atual faz um movimento
        current_player.take_action(env)

        # Atualiza estados
        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)

    if draw:
        env.draw_board()

    # Atualiza a função valor
    p1.update(env)
    p2.update(env)


if __name__ == '__main__':
    # Treina o agente
    p1 = Agent()
    p2 = Agent()

    # Configura initial V para p1 e p2
    env = Environment()
    state_winner_triples = get_state_hash_and_winner(env)

    Vx = initialV_x(env, state_winner_triples)
    p1.setV(Vx)
    Vo = initialV_o(env, state_winner_triples)
    p2.setV(Vo)

    # Define o símbolo de cada jogador
    p1.set_symbol(env.x)
    p2.set_symbol(env.o)

    T = 10000
    for t in range(T):
        if t % 200 == 0:
            print(t)
        play_game(p1, p2, Environment())

    # Jogando: Humano x Agente
    human = Human()
    human.set_symbol(env.o)
    while True:
        p1.set_verbose(True)
        play_game(p1, human, Environment(), draw=2)
        answer = input("Jogar novamente? [Y/n]: ")
        if answer and answer.lower()[0] == 'n':
            break
