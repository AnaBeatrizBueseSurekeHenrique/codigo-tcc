from loop_genetico import LoopGenetico

def main():
   loopGenetico = LoopGenetico(caminho_dataset='CAMINHO_DATASET',caminho_frases_avaliar= "CAMINHO_FRASES_AVALIAR", modelo_original="MODELO_ORIGINAL", tamanho_populacao=10, geracoes=10, porcentagemCruzamento=0.7,porcentagemMutacao=0.5, maxPaciencia=4, quantidade_linhas=100)
   loopGenetico.loop()
    
if __name__ == "__main__":
    main()