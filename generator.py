import numpy as np
import torch
from src import get_tokenier, get_model, get_special_tokens
# from src import SpacyNER, CommentGeneratorDataset

class TextGenerator:

    def __init__(self, model_config, deploy_config):
        self.inf_model = deploy_config.inf_model
        # self.ner_model = SpacyNER(model_name=model_config.spacy_ner_model, 
        #                           ners=model_config.ners)
        self.device = torch.device('cuda' if deploy_config.cuda else 'cpu')
        self.num_beams = model_config.num_beams
        self.max_length = model_config.max_length
        self.repetition_penalty = model_config.repetition_penalty
        self.early_stopping = model_config.early_stopping
        self.special_tokens = get_special_tokens()
        if self.inf_model == 'main':
            print("The MAIN model is loaded...")
            self.tokenizer = get_tokenier(model_path=model_config.path_to_main_model)
            self.model = get_model(model_path=model_config.path_to_main_model,
                                  tokenizer=self.tokenizer,
                                  cuda=deploy_config.cuda)
        else:
            print("The TRAINED model is loaded...")
            self.tokenizer = get_tokenier(model_path=model_config.path_to_main_model,
                                          special_tokens=self.special_tokens)
            self.model = get_model(model_path=model_config.path_to_main_model,
                                  tokenizer=self.tokenizer,
                                  cuda=deploy_config.cuda,
                                  special_tokens=self.special_tokens,
                                  load_model_path=model_config.path_to_finetuned_model)

        self.model.eval()
    
    def generate(self, text, ners, num_return_sequences=1):
    # def generate(self, text, num_return_sequences=1):
        # ners = self.ner_model.extract(text)
        # ners = CommentGeneratorDataset.join_ners(ners, randomize=False)
        if self.inf_model == 'main':
            prompt = text + ' ' + ners
        else:
            prompt = self.special_tokens['bos_token'] + ners + \
                     self.special_tokens['sep_token'] + text + \
                     self.special_tokens['eos_token']

        generated = torch.tensor(self.tokenizer.encode(prompt)).unsqueeze(0)
        generated = generated.to(self.device)

        sample_outputs = self.model.generate(generated, 
                                            do_sample=True,   
                                            max_length=self.max_length,
                                            num_beams=self.num_beams,
                                            repetition_penalty=self.repetition_penalty,
                                            early_stopping=self.early_stopping,
                                            num_return_sequences=num_return_sequences)
        results = []
        for i, sample_output in enumerate(sample_outputs):
            gen = self.tokenizer.decode(sample_output, skip_special_tokens=True)
            results.append(gen[len(text)+1:])
            # print("{}: {}\n\n".format(i, gen[len(text):]))
        return results
