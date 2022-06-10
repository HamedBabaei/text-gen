from datahandler import DataReader, DataWriter
from configuration import DataConfig, ModelConfig
import json
from src import SpacyNER
from tqdm import tqdm

def get_news_category_examples(file_path):
    with open(file_path, encoding="utf-8") as json_lines_file:
        data = []
        for line in json_lines_file:
            data.append(json.loads(line))
    return data

if __name__ == '__main__':
    DATA_CONFIG = DataConfig().get_args()
    MODEL_CONFIG = ModelConfig().get_args()

    NER_MODEL = SpacyNER(model_name=MODEL_CONFIG.spacy_ner_model, ners=MODEL_CONFIG.ners)

    print("loading data ...")
    NEWS_CATEGORY_DATA = get_news_category_examples(DATA_CONFIG.news_category_data)
    TOPIC_TRANSFORMER = DATA_CONFIG.topic_transformer

    print("build dataset ...")
    DATA_DICT = {topic:[] for topic in DATA_CONFIG.topics}

    for news in tqdm(NEWS_CATEGORY_DATA):
        if news['category'].lower() in DATA_CONFIG.topics:
            text = news['headline'] + ' ' + news['short_description']
            ners = NER_MODEL.extract(news['short_description'])
            DATA_DICT[news['category'].lower()].append((news['headline'].lower(), 
                                                        news['short_description'].lower(), 
                                                        ners))

    print(f"sport:{len(DATA_DICT['sports'])},  tech:{len(DATA_DICT['tech'])}")
    
    FINAL_DATA = {'topic':[], 'title':[], 'description':[], 'ners':[]}
    NERS = []
    for topic, data in DATA_DICT.items():
        for text, description, ners in data:
            FINAL_DATA['topic'].append(topic)
            FINAL_DATA['title'].append(text)
            FINAL_DATA['description'].append(description)
            FINAL_DATA['ners'].append(ners)
            for ner in ners:
                NERS.append(ner)
    print("Size of final data is:", len(FINAL_DATA))

    print("save dataset...")
    NERS = list(set(NERS))
    DataWriter.write_csv(FINAL_DATA, DATA_CONFIG.train_path)
    DataWriter.write_json(NERS, DATA_CONFIG.train_ners_path)

    print("generate report...")
    STATS = {"# of ners":len(NERS), "# of samples":len(FINAL_DATA)}
    WHOLE = 0
    for topic, data in DATA_DICT.items():
        STATS[f"# of samples in {topic}"] = len(DATA_DICT[topic])
        WHOLE += len(DATA_DICT[topic])
    STATS['whole number of samples'] = WHOLE
    DataWriter.write_json(STATS, DATA_CONFIG.logs)
