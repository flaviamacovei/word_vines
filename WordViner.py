import numpy as np
import gensim.downloader as api

class WordViner:
    def __init__(self):
        self.SMALL_DIM = 2
        # centre of current display
        self.offset = np.zeros(self.SMALL_DIM)
        # if the origin is the position of a word then that is saved in current_word, otherwise it is None
        self.current_word = None

        # relative positions of neighbouring words (in SMALL_DIM dimensions)
        self.neighbouring_positions_rel = None
        # absolute positions of neighbouring words (in SMALL_DIM dimensions)
        self.neighbouring_positions_abs = None
        # decodings of neighbouring words
        self.neighbouring_words = []
        self.w2v = api.load('word2vec-google-news-300')

    def in_vocab(self, word: str):
        # this might add unnecessary computation, maybe find a different way
        try:
            self.w2v[word]
            return True
        except KeyError:
            return False

    def input(self, word: str):
        big_embedding = self.w2v[word]
        self.current_word = word
        self.offset = self.project(big_embedding)
        self.recalculate_synonyms()

    def project(self, big_embedding):
        small_embedding = np.random.rand(self.SMALL_DIM)
        return small_embedding

    def recalculate_synonyms(self):
        pass

    def get_synonyms(self):
        return self.neighbouring_words

    def get_positions(self):
        return self.neighbouring_positions_rel

if __name__ == "__main__":
    word_viner = WordViner()
    word_viner.input("cat")
    print(word_viner.offset.shape)