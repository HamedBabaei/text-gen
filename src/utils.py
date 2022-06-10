
def make_generation(model, text, num_sequences):
    results = model.generate(text, num_sequences)
    return results