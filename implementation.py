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
    def __init__(self, eps=0.1, alpha=0.5):
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
    def __init__(self):
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
        h = 0
        for i in range(POSSIBLE_TOTAL_STATES):
            for j in range(POSSIBLE_TOTAL_STATES):
                if self.board[i, j] == 0:
                    v = 0
                elif self.board[i, j] == self.x:
                    v = 1
                elif self.board[i, j] == self.o:
                    v = 2
                h += (3**k) * v
                k += 1
        return h

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

    def isDraw(self):
        return self.ended and self.winner is None

    # Exemplo de tabuleiro
    # -------------
    # | x |   |   |
    # -------------
    # |   |   |   |
    # -------------
    # |   |   | o |
    # -------------
    def draw_board(self):
        for i in range(POSSIBLE_TOTAL_STATES):
            print("-------------")
            for j in range(POSSIBLE_TOTAL_STATES):
                print("  ", end="")
                if self.board[i, j] == self.x:
                    print("x ", end="")
                elif self.board[i, j] == self.o:
                    print("o ", end="")
                else:
                    print("  ", end="")
            print("")
        print("-------------")


class Human:
    def __init__(self):
        pass

    def setSymbol(self, sym):
        self.sym = sym

    def takeAction(self, env):
        while True:
            move = input(
                "Insira as coordenadas i, j para o próximo movimento (por exemplo: 0,2): ")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if env.isEmpty(i, j):
                env.board[i, j] = self.sym
                break

    def update(self, env):
        pass

    def updateStateHistory(self, s):
        pass


def getStateHashAndWinner(env, i=0, j=0):
    results = []

    for v in (0, env.x, env.o):
        env.board[i, j] = v
        if j == 2:
            if i == 2:
                state = env.getState()
                ended = env.gameOver(forceRecalculate=True)
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += getStateHashAndWinner(env, i + 1, 0)
        else:
            results += getStateHashAndWinner(env, i, j + 1)

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

# Loop ate o jogo terminar


def playGame(p1, p2, env, draw=False):
    currentPlayer = None
    while not env.game_over():
        if currentPlayer == p1:
            currentPlayer = p2
        else:
            currentPlayer == p1

        # Desenha o tabuleiro antes do proximo movimento
        if draw:
            if draw == 1 and currentPlayer == p1:
                env.drawBoard()
            if draw == 2 and currentPlayer == p2:
                env.drawBoard()

        # Jogador atual fez um movimento
        currentPlayer.takeAction(env)

        # Atualiza os estados
        state = env.getState()
        p1.updateStateHistory()
        p2.updateStateHistory()

    if draw:
        env.drawBoard()

    # Atualiza a funcao valor
    p1.update(env)
    p2.update(env)


if __name__ == '__main__':
    # Treina o agente
    p1 = Agent()
    p2 = Agent()

    # Configura initial V para p1 e p2
    env = Environment()
    state_winner_triples = getStateHashAndWinner(env)

    Vx = initialV_x(env, state_winner_triples)
    p1.setV(Vx)
    Vo = initialV_o(env, state_winner_triples)
    p2.setV(Vo)

    # Define o símbolo de cada jogador
    p1.setSymbol(env.x)
    p2.setSymbol(env.o)

    T = 10000
    for t in range(T):
        if t % 200 == 0:
            print(t)
        playGame(p1, p2, Environment())

    # Jogando: Humano x Agente
    human = Human()
    human.setSymbol(env.o)
    while True:
        p1.setVerbose(True)
        playGame(p1, human, Environment(), draw=2)
        answer = input("Jogar novamente? [Y/n]: ")
        if answer and answer.lower()[0] == 'n':
            break
