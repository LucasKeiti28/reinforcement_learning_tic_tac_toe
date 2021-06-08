print('Hello')
# 1) Decidir pela recompensa e' o inicio e um passo fundamental para a criacao do agente


class Environment:
    def reward(self, sym):
        # Sem recompensa ate terminar o jogo
        if not self.game_over():
            return 0

        # Se chegar aqui, e' gameover
        return 1 if self.winner == sym else 0
