import spacy

class SpacyNER:

    def __init__(self, model_name, ners):
        self.nlp = spacy.load(model_name)
        self.ners = ners
    
    def extract(self, text):
        doc = self.nlp(text)
        entities = [ent.text.lower() for ent in doc.ents if ent.label_ in self.ners]
        entities = list(set(entities))
        return entities
    