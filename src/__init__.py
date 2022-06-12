"""
    Make the importing much shorter
"""
from .ner import SpacyNER
from .gpt2 import get_special_tokens, get_model, get_tokenier, CommentGeneratorDataset
from .utils import make_generation
from .database import PostgreSQLDatabase
