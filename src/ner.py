"""
    Named Entity Recognizer models
"""
import spacy


class SpacyNER:
    """
        Spacy Named Entity Recognizer Class
    """
    def __init__(self, model_name, ners):
        """
            Init Spacy
        :param model_name: Spacy model name to load
        :param ners: valid ner labels
        :return:
        """
        self.nlp = spacy.load(model_name)
        self.ners = ners
    
    def extract(self, text):
        """
            Extract entities from text
        :param text: input text for SpacyNER
        :return: list of entities
        """
        doc = self.nlp(text)
        entities = [ent.text.lower() for ent in doc.ents if ent.label_ in self.ners]
        entities = list(set(entities))
        return entities
    