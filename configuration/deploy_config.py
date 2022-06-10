"""
    DeployConfig: Deployment Configuration
"""
import argparse
import os


class DeployConfig:
    """
        Deployment Configs
    """

    def __init__(self):
        """
            Deployment configuration
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--inf_model", type=str, default="main", help='which model to use in deploy [main, finetuned]')
        self.parser.add_argument("--cuda", type=bool, default=False, help='Cuda Utilization')
        self.parser.add_argument("-f")

    def get_args(self):
        """
            Return parser
        :return: parser
        """
        return self.parser.parse_args()
