import unittest
import numpy as np
import psycopg2
from configuration import ModelConfig, DeployConfig
from generator import TextGenerator
from src import (SpacyNER, 
                 CommentGeneratorDataset,
                 PostgreSQLDatabase)
import keys

model_config = ModelConfig().get_args()
deploy_config = DeployConfig().get_args()
model = TextGenerator(model_config, deploy_config)
ner_model =  SpacyNER(model_name=model_config.spacy_ner_model, ners=model_config.ners)

def get_artificial_data_for_db(index = 0):
    query = f"this a test query {index}"
    ners = ','.join([f"q{index} ner1", f"q{index} ner2"])
    result = [f"q{index} gen1", f"q{index} gen2"]
    return query, ners, result


class TestDataHandlerMethods(unittest.TestCase):

    def test_text_generator(self):
        print("test text generator")
        text = "trump posthumously pardons boxer jack johnson"
        ners = ner_model.extract(text)
        ners = CommentGeneratorDataset.join_ners(ners, randomize=False)
        result = model.generate(text=text, ners=ners, num_return_sequences=3)
        self.assertEqual(len(result), 3)

    def test_deploy_model_config(self):
        print("test deploy config")
        self.assertEqual(deploy_config.inf_model, "main")
        self.assertNotEqual(deploy_config.inf_model, "finetuned")
    
    def test_ner_model(self):
        print("test ner model")
        text = "trump posthumously pardons boxer jack johnson"
        ners = ner_model.extract(text)
        self.assertEqual(len(ners), 1)    
    
    def test_db_connection(self):
        print("test db connection")
        conn = psycopg2.connect(database=keys.DATABASE, 
                                user=keys.USER, 
                                password=keys.PASSWORD, 
                                host=keys.HOST, 
                                port=keys.PORT)
        cursor = conn.cursor()
        cursor.execute("select version()")
        data = cursor.fetchone()
        self.assertNotEqual(len(str(data)), 0)
        conn.close()
    
    def test_db_insert_delete_display(self):
        print("test db insert, delete and display")
        db = PostgreSQLDatabase(database=keys.DATABASE, 
                                user=keys.USER, 
                                password=keys.PASSWORD, 
                                host=keys.HOST, 
                                port=keys.PORT)
        data = db.display(get=True)
        self.assertNotEqual(len(data), 0)
        db.delete()
        data = db.display(get=True)
        self.assertEqual(len(data), 0)
        query, ners, results = get_artificial_data_for_db()
        db.instert(query, ners, results)
        data = db.display(get=True)
        self.assertEqual(len(data), 2)

if __name__ == '__main__':
    unittest.main()
