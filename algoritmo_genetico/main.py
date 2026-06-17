from loop_genetico import LoopGenetico

def main():
   loopGenetico = LoopGenetico('..\\conjuntos_de_dados\\ptbr-en_informal.csv', "..\\conjuntos_de_dados\\ptbr-en_formal.csv", modelo_original="Helsinki-NLP/opus-mt-tc-big-en-pt", tamanho_populacao=4, geracoes=3, porcentagemCruzamento=0.7,porcentagemMutacao=0.5, maxPaciencia=4, quantidade_linhas=10)
   loopGenetico.loop()
    
if __name__ == "__main__":
    main()