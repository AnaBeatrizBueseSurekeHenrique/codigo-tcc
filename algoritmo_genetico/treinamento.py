from datasets import DatasetDict, Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
import numpy as np
import evaluate
import pandas as pd
import os
class Treinamento():
    def __init__(self, 
                 modeloOriginal, 
                 frases_avaliar):
        self.metricBleu = evaluate.load("sacrebleu")
        self.metricMeteor = evaluate.load("meteor")
        self.modeloOriginal = modeloOriginal
        self.frases_avaliar = frases_avaliar
        self.tokenizer = AutoTokenizer.from_pretrained(modeloOriginal)
        
    def compute_metrics(self, eval_preds):
        preds, labels = eval_preds

        if isinstance(preds, tuple):
            preds = preds[0]
        
        preds[preds == -100] = self.tokenizer.pad_token_id
        decoded_preds = self.tokenizer.batch_decode(preds, skip_special_tokens=True)

        labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id)
        decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_preds = [pred.strip() for pred in decoded_preds]
        decoded_labels = [[label.strip()] for label in decoded_labels]

        resultBleu = self.metricBleu.compute(predictions=decoded_preds, references=decoded_labels)
        resutMeteor = self.metricMeteor.compute(predictions=decoded_preds, references=decoded_labels)

        return {"bleu": resultBleu["score"], "meteor":resutMeteor["meteor"]}
    
    def preprocess_function(self,examples):
        inputs = examples["en"]
        target = examples["pt-br"]
        model_inputs = self.tokenizer(inputs,text_target=target, max_length=128, truncation=True, padding="max_length", return_tensors="pt")
        
        return model_inputs
    
    def load_dataset(self,dataset):

        dados = DatasetDict()

        dados["train"] = Dataset.from_pandas(dataset)
        tokenized_books = dados.map(self.preprocess_function, batched=True, remove_columns=dados["train"].column_names)

        ds_final = DatasetDict({
            'train': tokenized_books['train'],
        })
        
        return ds_final

    def iniciar(self, dataset):
        id = dataset.id
        print(f'Iniciando treinamento {id}')
        model = AutoModelForSeq2SeqLM.from_pretrained(self.modeloOriginal,   
                                                    use_safetensors=True)
        ds = self.load_dataset(dataset.frases)
      
        training_args = Seq2SeqTrainingArguments(
            per_device_eval_batch_size=6,
            output_dir="./results",
            learning_rate=1e-6,
            weight_decay=0.01,
            save_total_limit=3,
            num_train_epochs=3,
            predict_with_generate=True,
            save_strategy="epoch",
            bf16=True
        )
        
        trainer = Seq2SeqTrainer(
            model=model,
            args=training_args,
            train_dataset=ds["train"],
            processing_class=self.tokenizer,
            compute_metrics=self.compute_metrics,
        )
        
        trainer.train()
        
        df = pd.read_csv(self.frases_avaliar)
        dados = self.load_dataset(df)
        val = trainer.evaluate(dados["train"])
        
        dataset.fitness = (val["eval_bleu"]/100 + val["eval_meteor"])
        
        print(f"Fitness{dataset.fitness}")
        print("------------------------")
        
        return dataset