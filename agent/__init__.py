import numpy as np

LENGTH = 3


class Agent:
    def __init__(self, eps=0.1, alpha=0.5):

        # Probabilidade de escolher uma ação aleatória em vez de gananciosa
        self.eps = eps

        # Learning rate
        self.alpha = alpha

        self.verbose = False
        self.state_history = []

    def setV(self, V):
        self.V = V

    def set_symbol(self, sym):
        self.sym = sym

    def set_verbose(self, v):
        # Se for verdade, imprimirá valores para cada posição no tabuleiro
        self.verbose = v

    def reset_history(self):
        self.state_history = []

    def take_action(self, env):
        # Escolhe uma ação baseada na estratégia epsilon-gananciosa
        r = np.random.rand()
        best_state = None
        if r < self.eps:
            # Toma uma ação aleatória
            if self.verbose:
                print("Tomando uma ação aleatória")

            possible_moves = []
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                        possible_moves.append((i, j))
            idx = np.random.choice(len(possible_moves))
            next_move = possible_moves[idx]
        else:
            # Escolha a melhor ação com base nos valores atuais de estados,
            # faz um loop em todos os movimentos possíveis,
            # obtém seus valores para acompanhar o melhor valor
            pos2value = {}
            next_move = None
            best_value = -1
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                        # Qual é o estado se fizermos esse movimento?
                        env.board[i, j] = self.sym
                        state = env.get_state()
                        env.board[i, j] = 0
                        pos2value[(i, j)] = self.V[state]
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i, j)

            # Se verbose, desenhe o tabuleiro com os valores
            if self.verbose:
                print("Tomando uma ação gananciosa")
                for i in range(LENGTH):
                    print("------------------")
                    for j in range(LENGTH):
                        if env.is_empty(i, j):
                            # Imprime o valor
                            print(" %.2f|" % pos2value[(i, j)], end="")
                        else:
                            print("  ", end="")
                            if env.board[i, j] == env.x:
                                print("x  |", end="")
                            elif env.board[i, j] == env.o:
                                print("o  |", end="")
                            else:
                                print("   |", end="")
                    print("")
                print("------------------")

        # Faz o movimento
        env.board[next_move[0], next_move[1]] = self.sym

    def update_state_history(self, s):
        # Não pode colocar isso em take_action, porque take_action só acontece uma vez a cada outra iteração
        # para cada histórico de estado do jogador o estado precisa ser atualizado a cada iteração s = env.get_state()
        # e não queremos fazer isso duas vezes.
        self.state_history.append(s)

    def update(self, env):
        # Queremos BACKTRACK sobre os estados, para que:
        # V(prev_state) = V(prev_state) + alpha*(V(next_state) - V(prev_state))
        # where V(next_state) = reward se for o estado mais atual
        #
        # NOTA: fazemos isso no final de um episódio

        # Aqui é onde a aprendizagem realmente acontece
        reward = env.reward(self.sym)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()
