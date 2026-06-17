class frases_selecionadas():
    def __init__(self, 
                 frases, 
                 id_corpus):
        self.frases = frases
        self.id = id_corpus
        self.fitness = 0
        
    def salva(self):
        self.frases.to_csv(f"melhor_conjunto21-{self.id}.csv",",", index=False)