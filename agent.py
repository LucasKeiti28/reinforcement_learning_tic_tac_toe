# Imports
import matplotlib.pyplot as plt
import numpy as np
from builtins import range, input

print('Hello')
print(np.random.rand())
# 1) Decidir pela recompensa e' o inicio e um passo fundamental para a criacao do agente
# 2) Implementar a politica de recompensa, no caso usaremos Epslon Greedy
# 3) Definir a Value Function
# 4) Definir a representacao de estados
# 5) Indicar como um estado atual do agente significa para o jogo (vencer, perder, empate)
# 6) Definir a classe Environment
# 7) Definir a classe Agente

# Definindo Constantes
# Variavel que define a quantidade de estados possiveis: 3
POSSIBLE_TOTAL_STATES = 3


class Agent:
    def __init__(self, eps=0.1, alpha=0.5) -> None:
        # Probabilidade de escolher uma acao aleatoria ao inves da gananciosa
        self.eps = eps
        # Learning Rate do Agente
        self.alpha = alpha
        # Se ira mostrar os logs das acoes ou nao
        self.verbose = False
        # Lista para armazernar os estados anteriores de um episodio
        self.state_history = []

    #
    def setV(self, V):
        self.V = V

    # Defini qual o simbolo do agente -> 'x' ou 'o'
    def setSymbol(self, symbol):
        self.symbol = symbol

    # Defini se iremos mostrar cada posicao do tabuleiro ou nao
    def setVerbose(self, v):
        self.verbose = v

    def resetHistory(self):
        self.state_history = []

    def takeAction(self, env):
        # Escolhe uma acao baseada na estrategia epsilon-greedy
        randomNumber = np.random.rand()
        bestState = None

        if randomNumber < self.eps:
            # Tomar uma acao aleatoria
            if self.verbose:
                "Tomando uma acao aleatoria"

            possibleMoves = []
            for i in range(POSSIBLE_TOTAL_STATES):
                for j in range(POSSIBLE_TOTAL_STATES):
                    if env.isEmpty(i, j):
                        possibleMoves.append((i, j))
            index = np.random.choice(len(possibleMoves))
            print('index :>>', index)
            nextMove = possibleMoves[index]
            print('nextMove :>>', nextMove)
        else:
            # Escolher a melhor acao possivel, baseado em todos os estados
            # disponiveis. obtem cada valor, para descobrir o melhor possivel
            valuePosition = {}
            nextMove = None
            bestValue = -1
            for i in range(POSSIBLE_TOTAL_STATES):
                for j in range(POSSIBLE_TOTAL_STATES):
                    if env.isEmpty((i, j)):
                        # Qual o estado se fizermos esse movimento
                        env.board[i, j] = self.symbol
                        state = env.getState()
                        env.board[i, j] = 0
                        valuePosition[(i, j)] = self.V[state]
                        print('self.V[state]', self.V[state])
                        if self.V[state] > bestValue:
                            bestValue = self.V[state]
                            bestState = state
                            nextMove = (i, j)
            # Se verbose, desenha os valores de estado do tabuleiro
            if self.verbose:
                print('Tomando uma acao gananciosa')
                for i in range(POSSIBLE_TOTAL_STATES):
                    print("-----------------")
                    for j in range(POSSIBLE_TOTAL_STATES):
                        if env.isEmpty(i, j):
                            # Imprimir valor
                            print("%.2f|" % valuePosition[(i, j)], end="")
                        else:
                            print(" ", end="")
                            if env.board[i, j] == env.x:
                                print("x |", end="")
                            elif env.board[i, j] == env.o:
                                print("o |", end="")
                            else:
                                print(" |", end="")
                    print("")
                print("-----------------")

        # Realiza o movimento
        env.board[nextMove[0], nextMove[1]] = self.symbol

    def updateStateHistory(self, state):
        self.state_history.append(state)

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
        # Reset nos estados no final de cada episodio
        self.resetHistory()


class Environment:
    def __init__(self) -> None:
        self.board = np.zeros((POSSIBLE_TOTAL_STATES, POSSIBLE_TOTAL_STATES))

        # Representa o 'x' no tabulerio
        self.x = -1
        # Representa o 'o' no tabulerio
        self.o = 1

        self.winner = None
        self.ended = False
        self.num_states = 3**(POSSIBLE_TOTAL_STATES*POSSIBLE_TOTAL_STATES)

    def isEmpty(self, i, j):
        # Retorna True ou False
        return self.board[i, j] == 0

    def reward(self, sym):
        # Sem recompensa ate terminar o jogo
        if not self.game_over():
            return 0

        # Se chegar aqui, e' gameover
        return 1 if self.winner == sym else 0

    def getState(self):
        k = 0
        state = 0
        for i in range(POSSIBLE_TOTAL_STATES):
            for j in range(POSSIBLE_TOTAL_STATES):
                if self.board[i, j] == 0:
                    value = 0
                elif self.board[i, j] == self.x:
                    value = 1
                elif self.board[i.j] == self.o:
                    value = 2
                state += (3**k)*value
                k += 1
        return state

    def gameOver(self, forceRecalculate=False):
        # Retorna true se o jogo acabou (alguem ganhou ou empate). Se nao, retorna false.
        # define a variavel de exemplo 'vencedor' e a variavel de instancia 'encerrada'
        if not forceRecalculate and self.ended:
            return self.ended

        # Verificando se existe algum vencedor
        # Checando as linhas
        for i in range(POSSIBLE_TOTAL_STATES):
            for player in (self.x, self.o):
                if self.board[i].sum() == player*POSSIBLE_TOTAL_STATES:
                    self.winner = player
                    self.ended = True
                    return True

        # Checando as colunas
        for j in range(POSSIBLE_TOTAL_STATES):
            for player in (self.x, self.o):
                if self.winner[j].sum() == player*POSSIBLE_TOTAL_STATES:
                    self.winner = player
                    self.ended = True
                    return True

        # Checando as diagonais
        for player in (self.x, self.o):
            # top/left -> bottom/right
            if self.board.trace() == player*POSSIBLE_TOTAL_STATES:
                self.winner = player
                self.ended = True
                return True
            # top/right -> bottom/left
            if np.fliplr(self.board).trace() == player*POSSIBLE_TOTAL_STATES:
                self.winner = player
                self.ended = True
                return True

        # Checa se e' empate
        if np.all((self.board == 0) == False):
            self.winner = None
            self.ended = True
            return True

        # O Jogo ainda nao acabou
        self.winner = None
        return False
