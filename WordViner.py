import numpy as np
import gensim.downloader as api
from sklearn.manifold import Isomap

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

        # word2vec model with vocab size 3_000_000, dimensions 300
        self.w2v = api.load('word2vec-google-news-300')
        self.isomap = Isomap(radius = 10, n_neighbors = None, n_components = self.SMALL_DIM, path_method = 'auto', metric = 'minkowski', p = 2)
        self.w2v_small_vectors = self.isomap.fit_transform(self.w2v.vectors)
        print(f"w2v_small: {self.w2v_small_vectors.shape}")

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
        self.offset = self.project(big_embedding[None]) # add batch dimension of size 1
        self.recalculate_synonyms()

    def project(self, big_embedding):
        batch_size = big_embedding.shape[0]
        small_embedding = np.random.rand(batch_size, self.SMALL_DIM)
        return small_embedding

    def recalculate_synonyms(self):
        pass

    def get_synonyms(self):
        return self.neighbouring_words

    def get_positions(self):
        return self.neighbouring_positions_rel