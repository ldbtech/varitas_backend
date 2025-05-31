
from keybert import KeyBERT

print("Downloading Bert... \n")
shared_model = KeyBERT(model='all-MiniLM-L6-v2')
print("Ending Downloading part \n")
class PromptAnalysis:
    def __init__(self, input_text):
        self.input_text = input_text

    def extract_keywords(self, top_n=5, diversity=False):
        keywords = shared_model.extract_keywords(
            self.input_text,
            keyphrase_ngram_range=(1, 2),
            stop_words="english",
            use_mmr=diversity,
            diversity=0.7 if diversity else None,
            top_n=top_n
        )

        return [kw[0] for kw in keywords][0]





