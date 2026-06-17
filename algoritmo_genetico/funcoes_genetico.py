import random
import pandas as pd
from treinamento import Treinamento
from frases_classe import frases_selecionadas

class Genetico():
    def __init__(self, 
                 quantidade_linhas, 
                 dataset,
                 modelo_original,
                 frases_avaliar):
            self.quantidade_linhas = quantidade_linhas
            self.df = pd.read_csv(dataset, on_bad_lines='skip')
            self.treinamento = Treinamento(modelo_original, frases_avaliar)
            
    def geracao_de_individuo(self,id):
        qntd = self.quantidade_linhas
        frases = pd.DataFrame()
        auxdf = self.df.copy()
        
        # Seleciona frases aleatórias para conjunto de dados do individuo.
        for _ in range(0, qntd):        
            linha_aleatoria = auxdf.sample(n=1)
            auxdf.drop(linha_aleatoria.index, inplace=True)
            frases = pd.concat([frases, linha_aleatoria], ignore_index=True)
        
        individuo = frases_selecionadas(frases, id)
        individuo = self.treinamento.iniciar(individuo)
        
        return individuo

    def gerar_populacao(self, n):
        return [self.geracao_de_individuo(i) for i in range(n)]

    def mutacao(self, individuoOg):
        qntd_alterar = (random.randint(1, int(self.quantidade_linhas/3))) 
        linhas = random.sample(range(0, self.quantidade_linhas), qntd_alterar)
        auxdf = self.df.copy()
        
        # Duplicação do individuo original.
        individuo = frases_selecionadas(individuoOg.frases.copy(),f"{individuoOg.id}-m")
        
        for i in range(0, qntd_alterar):
            linha_aleatoria = auxdf.sample(n=1)
            auxdf.drop(linha_aleatoria.index, inplace=True)         
            encontrado  = False
            for k in individuo.frases.values:
                if(k[0] == linha_aleatoria.values[0][0]):
                    encontrado = True  
            
            if(not encontrado):
                    individuo.frases.iloc[linhas[i]] = linha_aleatoria
            else:
                i -= 1
        
        individuo = self.treinamento.iniciar(individuo)  
        return individuo

    def loopDeMutacao(self, populacao, qntdMutacao):
        arrMutacao = random.sample(range(0, len(populacao)), k=qntdMutacao)
        
        for i in arrMutacao:
            populacao.append(self.mutacao(populacao[i]))
        
        return populacao 
    
    def selecao(self, populacao, tamPop):
        delet = len(populacao) - tamPop
        i = 0
       
        # Deleta os piores individuos, até que a nova população tenha a mesma quantidade de individuos da original.
        while(i < delet):
            populacao.pop()
            i = i+1
        return populacao

    def cruzamento(self, individuo1, individuo2,id):
        
        frases = pd.DataFrame()
        frases = pd.concat([frases, individuo1.frases.iloc[:len(individuo1.frases)//2]], ignore_index=True) 
        frases = pd.concat([frases, individuo2.frases.iloc[:len(individuo2.frases)//2:]], ignore_index=True) 
        frases.drop_duplicates()
        
        if(len(frases) < self.quantidade_linhas):
            juntar = pd.DataFrame()
            juntar =pd.concat([individuo1.frases, individuo2.frases], ignore_index=True)
            juntar.drop_duplicates()
            merged = juntar.merge(frases, how='left', indicator=True)
            unicas = merged[merged['_merge'] == 'left_only']
            embaralhadas = unicas.sample(frac=1).reset_index(drop=True)
            tam = self.quantidade_linhas - len(frases) 
            linha_aleatorias = embaralhadas.sample(n=tam)  
            frases = pd.concat([frases, linha_aleatorias], ignore_index=True)     
            
        filho = frases_selecionadas(frases,id)
        filho = self.treinamento.iniciar(filho)
        return filho

    def loopDeCruzamento(self, populacao, qntdCruzamento,id):
        arrayCruzamento = random.sample(range(0, len(populacao)), k=qntdCruzamento)
        i = 0
        
        while(i < qntdCruzamento):
            id += 1
            populacao.append(self.cruzamento(populacao[arrayCruzamento[i]], populacao[arrayCruzamento[i+1]], id))
            i += 2
            
        return populacao,id