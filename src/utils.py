"""
    Generation Main Engine for API
"""


def clean_text(text):
    """
        Clean texts
    """
    text = text.lower()
    text = text.replace("'", "")
    return text

def make_generation(generator_model, ner_model, dataset, input_text, database, num_sequences):
    """
        Method to making generations with help of database in the
        following steps:
            1. ner extraction
            2. geting unique number of generated text from model
            3. store them in database
            4. return the list
    """
    results = []
    num_return_sequences = num_sequences
    # 1. get ner, concatenate the ners, and do cleaning
    ners = ner_model.extract(input_text)
    ners = dataset.join_ners(ners, randomize=False)
    ners = clean_text(ners)
    # 2. gen num_sequences unique generations
    while True:
        # 2.1 generate texts
        generated_texts = generator_model.generate(text=input_text, 
                                                   ners=ners, 
                                                   num_return_sequences=num_return_sequences)
        # 2.2 check each generated texts to see if they are unique
        for text in generated_texts:
            # 2.2.1 preprocess the results
            text = clean_text(text)   
            # 2.2.2 find which textgen is exist in database and ignore it
            if not database.is_exist(textgen=text):
                results.append(text)
        # 2.3 check if we obtain the num_sequences unique generations
        #     if not continue the loop with 
        #     num_return_sequences = num_sequences - len(results)
        if len(results) == num_sequences:
            break
        num_return_sequences = num_sequences - len(results)
    # 3. store the data into database and then return it to the user
    database.instert(query=input_text, ners=ners, results=results)
    # 4. return the results
    return results
