class FilaBacklog:
    def __init__(self):
        self.dados = []
        
    def enqueue(self,jogo):
        self.dados.append(jogo)
        
    def dequeue(self):
        if self.is_empty():
            return None
        return self.dados.pop(0)
    
    def is_empty(self):
        return len(self.dados) == 0
    
    def mostrar(self):
        if self.is_empty():
            print('Backlog vazio')
            return
        for i,jogo in enumerate(self.dados, start=1):
            print(f'ID: {i}')
            jogo.exibir()
            
    def tamanho(self):
        return len(self.dados)
    
    def contem(self, id):
        for jogo in self.dados:
            if jogo.id_jogo == id:
                return True
        return False