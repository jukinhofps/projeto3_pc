class SessaoJogo:
    def __init__(self, jogo, tempo_jogado, data_sessao, tempo_total, status):
        self.jogo = jogo
        self.tempo_jogado = tempo_jogado
        self.data_sessao = data_sessao
        self.tempo_total = tempo_total
        self.status = status

    def exibir(self):
        print(f'{self.jogo.titulo} | Sessão: {self.tempo_jogado}h | Total: {self.tempo_total}h | Status: {self.status} | Data: {self.data_sessao}')
