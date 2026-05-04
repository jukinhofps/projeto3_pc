class Jogo:
    def __init__(self,id_jogo,titulo,console,genero,publisher,developer,critic_score,total_vendas,vendas_an,vendas_jp,vendas_eu,outras_vendas,data_lanc):
        self.id_jogo = id_jogo
        self.titulo = titulo
        self.console = console
        self.genero = genero
        self.publisher = publisher
        self.developer = developer
        self.critic_score = critic_score
        self.total_vendas = total_vendas
        self.vendas_an = vendas_an
        self.vendas_jp = vendas_jp
        self.vendas_eu = vendas_eu
        self.outras_vendas = outras_vendas
        self.data_lanc = data_lanc
        
    def exibir(self):
        print(f'{self.id_jogo}, {self.titulo}, {self.console}, {self.genero}, {self.publisher}, {self.developer}, {self.critic_score}, {self.total_vendas}, {self.vendas_an}, {self.vendas_jp}, {self.vendas_eu}, {self.outras_vendas}, {self.data_lanc} ')
        
    def linha_backlog(self):
        return f'{self.id_jogo}, {self.titulo}, {self.console}'
    
    def linha_recentes(self):
        return f'{self.id_jogo}, {self.titulo}, {self.console}'
    
    
        