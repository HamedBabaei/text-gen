import torch
from transformers import AutoTokenizer, AutoConfig, AutoModelForPreTraining
from torch.utils.data import Dataset, random_split, DataLoader, \
                             RandomSampler, SequentialSampler
import random

SPECIAL_TOKENS  = { "bos_token": "<|BOS|>",
                    "eos_token": "<|EOS|>",
                    "unk_token": "<|UNK|>",                    
                    "pad_token": "<|PAD|>",
                    "sep_token": "<|SEP|>"}

class CommentGeneratorDataset(Dataset):
    def __init__(self, data, tokenizer, max_length, randomize=True):

        self.title = data['title'].tolist()
        self.desc  = data['description'].tolist()
        self.ners = [eval(ners) for ners in data['ners'].tolist()]
        self.randomize = randomize
        self.tokenizer = tokenizer 
        self.max_length = max_length

    @staticmethod
    def join_ners(ners, randomize=True):
        N = len(ners)
        if randomize: 
            M = random.choice(range(N+1))
            ners = ners[:M]
            random.shuffle(ners)
        return ','.join(ners)

    def __len__(self):
        return len(self.title)
    
    def __getitem__(self, i):
        ners = self.ners[i].copy()
        ners = self.join_ners(ners, self.randomize)
        
        input = SPECIAL_TOKENS['bos_token'] + self.title[i] + \
                SPECIAL_TOKENS['sep_token'] + ners + SPECIAL_TOKENS['sep_token'] + \
                str(self.desc[i]) + SPECIAL_TOKENS['eos_token']

        encodings_dict = tokenizer(input,                                   
                                   truncation=True, 
                                   max_length=self.max_length, 
                                   padding="max_length")   
        
        input_ids = encodings_dict['input_ids']
        attention_mask = encodings_dict['attention_mask']
        
        return {'label': torch.tensor(input_ids),
                'input_ids': torch.tensor(input_ids), 
                'attention_mask': torch.tensor(attention_mask)}

def get_tokenier(model_path, special_tokens=None):
    tokenizer = AutoTokenizer.from_pretrained(model_path) 
    if special_tokens:
        tokenizer.add_special_tokens(special_tokens)
        # print("Special tokens added")
    return tokenizer


def get_model(model_path, tokenizer, cuda=False, special_tokens=None, load_model_path=None):
    if special_tokens:
        config = AutoConfig.from_pretrained(model_path, 
                                            bos_token_id=tokenizer.bos_token_id,
                                            eos_token_id=tokenizer.eos_token_id,
                                            sep_token_id=tokenizer.sep_token_id,
                                            pad_token_id=tokenizer.pad_token_id,
                                            output_hidden_states=False)
    else: 
        config = AutoConfig.from_pretrained(model_path,                                     
                                            pad_token_id=tokenizer.eos_token_id,
                                            output_hidden_states=False)    
    model = AutoModelForPreTraining.from_pretrained(model_path, config=config)
    if special_tokens:
        model.resize_token_embeddings(len(tokenizer))
    if load_model_path:
        model.load_state_dict(torch.load(load_model_path, 
                                        map_location=torch.device('cuda' if cuda else 'cpu')))
    if cuda:
        model.cuda()
    return model

def get_special_tokens():
    return SPECIAL_TOKENS