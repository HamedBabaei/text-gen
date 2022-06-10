"""
    ModelConfig: Data Configuration of models
"""
import argparse


class ModelConfig:
    """
        Model Configs
    """
    def __init__(self):
        """
            Model configuration
        """
        ners_default = ['ORG', 'LOC', 'PERSON', 'DATE']

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--test_size", type=float, default=0.2, help='test set size')
        self.parser.add_argument("--ners", type=list, default=ners_default, help='ner default list')
        self.parser.add_argument("--spacy_ner_model", type=str, default='en_core_web_sm', help='Spacy NER model name')
        self.parser.add_argument("--path_to_finetuned_model", type=str, default='assets/trained-gpt-2/pytorch_model.bin', help='path to finetuned model')
        self.parser.add_argument("--path_to_main_model", type=str, default='gpt2', help='path to finetuned model')
        self.parser.add_argument("--num_beams", type=int, default=5, help="number of beem search")
        self.parser.add_argument("--max_length", type=int, default=40, help="max length of texts")
        self.parser.add_argument("--repetition_penalty", type=float, default=5.0, help="repetition penalty")
        self.parser.add_argument("--early_stopping", type=bool, default=True, help="early stopping in generation")
        self.parser.add_argument("-f")

    def get_args(self):
        """
            Return parser
        :return: parser
        """
        return self.parser.parse_args()
