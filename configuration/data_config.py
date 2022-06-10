"""
    DataConfig: Data Configuration of models
"""
import argparse


class DataConfig:
    """
        Data Configs
    """
    def __init__(self):
        """
            Data configuration
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--bbc_news_data", type=str, 
                                default="datasets/raw/bbc_news_train.csv", 
                                help='Path to bbc raw dataset')
        self.parser.add_argument("--news_category_data", type=str, 
                                default="datasets/raw/news_category_dataset_v2.json", 
                                help='Path to news category raw dataset')
        self.parser.add_argument("--topics", type=list, default=['sports', 'tech'], 
                                help='topics to consider for dataset creation')
        self.parser.add_argument("--topic_transformer", type=list,
                                default={'tech':'tech', 'sports':'sports'}, 
                                help='to consider similar topics in dataset creation')
        self.parser.add_argument("--train_path", type=str, 
                                default="datasets/preprocessed/train.csv", 
                                help='Path to preprocessed train file')
        self.parser.add_argument("--train_ners_path", type=str, 
                                default="datasets/preprocessed/train_ners.json", 
                                help='Path to train ners file')
        self.parser.add_argument("--logs", type=str, default="report/data.stats.json", 
                                help='dataset (train and test) stats path')
        self.parser.add_argument("--seed", type=int, default=422, help='random seeds')
        self.parser.add_argument("-f")

    def get_args(self):
        """
            Return parser
        :return: parser
        """
        return self.parser.parse_args()
