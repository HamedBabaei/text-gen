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
        
        self.parser.add_argument("-f")

    def get_args(self):
        """
            Return parser
        :return: parser
        """
        return self.parser.parse_args()
