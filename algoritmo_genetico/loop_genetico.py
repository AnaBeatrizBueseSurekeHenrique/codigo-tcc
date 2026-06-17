from funcoes_genetico import Genetico

class LoopGenetico():    
    def __init__(self, 
                 caminho_dataset, 
                 caminho_frases_avaliar,
                 modelo_original,
                 tamanho_populacao, 
                 geracoes, 
                 porcentagemCruzamento, 
                 porcentagemMutacao, 
                 maxPaciencia, 
                 quantidade_linhas):
        
        self.genetico = Genetico(quantidade_linhas, caminho_dataset, modelo_original, caminho_frases_avaliar)
        self.tam = tamanho_populacao
        self.id = tamanho_populacao
        self.qntdGeracao = geracoes
        self.populacao = self.genetico.gerar_populacao(self.tam)
        self.porcentagemCruzamento = porcentagemCruzamento
        self.porcentagemMutacao = porcentagemMutacao
        self.maxPaciencia = maxPaciencia
                
    def loop(self):
        # Organiza a população em ordem descrescente.
        self.populacao = sorted(self.populacao, key=lambda s: s.fitness, reverse=True)
        self.qntdCruzamento = self.qntdCruzamento-1 if self.qntdCruzamento%2 == 1 else self.qntdCruzamento
        
        antigoBestFit = self.populacao[0].fitness
        piorIndividuo = self.populacao[self.tam-1]
        
        qntdMutacao = int((len(self.populacao)*self.porcentagemMutacao))    
        qntdCruzamento = int((len(self.populacao)*self.porcentagemCruzamento))
        paciencia = 0
        
        while((geracao < self.qntdGeracao) and (paciencia < self.maxPaciencia)):
            
            print("Iniciando Mutação...")
            self.populacao = self.genetico.loopDeMutacao(self.populacao, qntdMutacao)    
            
            print('Iniciando Cruzamento...')
            self.populacao, id = self.genetico.loopDeCruzamento(self.populacao, qntdCruzamento, id)
            
            print("Iniciando Seleção...")
            self.populacao = sorted(self.populacao, key=lambda s: s.fitness, reverse=True)
            self.populacao = self.genetico.selecao(self.populacao,self.tam)
            
            # Caso haja a população atual seja menor que o tamanho declarado da população, novos individuos serão gerados.
            if(self.tam - len(self.populacao) > 0):
                auxPop = self.genetico.gerar_populacao(self.tam - len(self.populacao))
                self.populacao += auxPop
                self.populacao = self.populacao.sort(key=lambda p: p.fitness)   
            
            print(f"Geração {geracao+1}/{self.qntdGeracao}")
            
            for i, individuo in enumerate(self.populacao, 1):
                print(f"\n--- Individuo {individuo.id} ---")
                print(f'Fitness Score: {individuo.fitness}')
                
            if(piorIndividuo.fitness > self.populacao[self.tam-1].fitness):
                piorIndividuo = self.populacao[self.tam-1]
            
            if(antigoBestFit == self.populacao[0].fitness):
                self.paciencia += 1
            else:
                antigoBestFit = self.populacao[0].fitness
                self.paciencia = 0
            geracao +=1
    
    
        if(paciencia >= self.maxPaciencia):
            print(f"Não houve evolução, algoritmo terminado na geração {geracao}.")
            
        # Mostra os melhores individuos, seus respectivos fitness e salva seu conjunto de dados.
        for i in range(0,5):
            print(f"---    Individuo {self.populacao[i].id}: fitness. {self.populacao[i].fitness}   ---")
            self.paciencia[i].salva()

        print(f"Pior: {piorIndividuo.id}:   fitness: {piorIndividuo.fitness}")