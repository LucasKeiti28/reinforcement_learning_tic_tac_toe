import numpy as np
LENGTH = 3


class Environment:

    # Construtor
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))

        # Representa um x no tabuleiro, jogador 1
        self.x = -1

        # Representa um o no tabuleiro, jogador 2
        self.o = 1

        self.winner = None
        self.ended = False
        self.num_states = 3**(LENGTH*LENGTH)

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def reward(self, sym):
        # Sem recompensa até terminar o jogo
        if not self.game_over():
            return 0

        # Se chegamos aqui, game is over
        return 1 if self.winner == sym else 0

    def get_state(self):
        # Retorna o estado atual, representado como um int de 0 ... | S | -1, onde S = conjunto de todos os estados possíveis
        # | S | = 3 ^ (TAMANHO DO TABULEIRO), uma vez que cada célula pode ter 3 valores possíveis - vazio, x, o - alguns estados não são possíveis,
        # p. Ex. todas as células são x, mas ignoramos esse detalhe, é como encontrar o número inteiro representado por um número base-3
        k = 0
        h = 0
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i, j] == 0:
                    v = 0
                elif self.board[i, j] == self.x:
                    v = 1
                elif self.board[i, j] == self.o:
                    v = 2
                h += (3**k) * v
                k += 1
        return h

    def game_over(self, force_recalculate=False):
        # Retorna verdadeiro se o jogo acabou (um jogador ganhou ou é um empate), de outra forma, retorna falso
        # também define a variável de exemplo 'vencedor' e a variável de instância 'encerrada'
        if not force_recalculate and self.ended:
            return self.ended

        # Verifica se há vencedor

        # Checa as linhas
        for i in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[i].sum() == player*LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # Checa as colunas
        for j in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[:, j].sum() == player*LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # Checa as diagonais
        for player in (self.x, self.o):
            # top-left -> bottom-right diagonal
            if self.board.trace() == player*LENGTH:
                self.winner = player
                self.ended = True
                return True
            # top-right -> bottom-left diagonal
            if np.fliplr(self.board).trace() == player*LENGTH:
                self.winner = player
                self.ended = True
                return True

        # Checa se é empate
        if np.all((self.board == 0) == False):
            self.winner = None
            self.ended = True
            return True

        # O jogo ainda não acabou
        self.winner = None
        return False

    def is_draw(self):
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
        for i in range(LENGTH):
            print("-------------")
            for j in range(LENGTH):
                print("  ", end="")
                if self.board[i, j] == self.x:
                    print("x ", end="")
                elif self.board[i, j] == self.o:
                    print("o ", end="")
                else:
                    print("  ", end="")
            print("")
        print("-------------")
