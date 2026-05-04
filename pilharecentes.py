class PilhasRecentes:
    def __init__(self, limite = 20):
        self.dados = []
        self.limite = limite
        
    def push(self, jogo):
        # Remove ocorrências anteriores do mesmo jogo para que ele fique no topo
        self.dados = [item for item in self.dados if item.id_jogo != jogo.id_jogo]
        self.dados.append(jogo)
        if len(self.dados) > self.limite:
            self.dados.pop(0)
            
    def pop(self):
        if self.is_empty():
            return None
        return self.dados.pop()
    
    def topo(self):
        if self.is_empty():
            return None
        return self.dados[-1]
    
    def is_empty(self):
        return len(self.dados) == 0
    
    def tamanho(self):
        return len(self.dados)
    
    def mostrar(self):
        if self.is_empty():
            print('Nenhum jogo recente.')
            return
        print('Jogos recentes (do mais recente ao mais antigo):')
        for i in range(len(self.dados)-1, -1, -1):
            self.dados[i].exibir()