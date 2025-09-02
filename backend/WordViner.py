import numpy as np
import gensim.downloader as api
from umap import UMAP
import pickle
import os

class WordViner:
    def __init__(self):
        self.SMALL_DIM = 2
        self.NUM_NEIGHBOURS = 10
        self.TOLERANCE = 0.8
        # centre of current display
        self.offset = np.zeros(self.SMALL_DIM)
        # if the origin is the position of a word then that is saved in current_word, otherwise it is None
        self.current_word = None

        # relative positions of neighbouring words (in SMALL_DIM dimensions)
        self.synonyms_pos_rel = None
        # absolute positions of neighbouring words (in SMALL_DIM dimensions)
        self.synonyms_pos_abs = None
        # decodings of neighbouring words
        self.synonyms = []

        self.embeddings_path = 'data/w2v_projection.pkl'
        self.w2v = api.load('word2vec-google-news-300')
        # available models: print(list(gensim.downloader.info()['models'].keys()))
        self.projector = self.load_or_save_embeddings()

    def load_or_save_embeddings(self):
        if os.path.exists(self.embeddings_path):
            with open(self.embeddings_path, 'rb') as f:
                return pickle.load(f)
        else:
            print("Saved embeddings not found, performing umap...")
            umap = UMAP(n_components = 2, init = 'random', random_state = 0)
            projector = umap.fit(self.w2v.vectors)
            with open(self.embeddings_path, 'wb') as f:
                pickle.dump(projector, f)
            return projector

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
        print(f"offset: {self.offset}")
        self.recalculate_synonyms()

    def project(self, big_embeddings):
        small_embeddings = self.projector.transform(big_embeddings)
        return small_embeddings

    def recalculate_synonyms(self):
        # get synonyms from word2vec
        synonyms_dict = self.w2v.most_similar(positive = [self.current_word], topn = self.NUM_NEIGHBOURS)
        # prune distant words
        filter(lambda item: item[1] <= self.TOLERANCE, synonyms_dict)
        # still to do:
        # - remove redundant words (eg capitalised and non-capitalised)
        # - remove words that aren't in some accepted vocabulary of actual words <- is this a preprocessing step?
        # extract words
        self.synonyms = [item[0] for item in synonyms_dict]
        big_embeddings = np.stack([self.w2v[word] for word in self.synonyms])
        self.synonyms_pos_abs = self.project(big_embeddings)

        # normalise positions
        # centre
        self.synonyms_pos_rel = self.synonyms_pos_abs - self.offset
        # scale
        scale_factor = np.max(np.abs(self.synonyms_pos_rel))

        self.synonyms_pos_rel = self.synonyms_pos_rel / scale_factor

    def get_synonyms(self):
        return self.synonyms

    def get_positions(self):
        return self.synonyms_pos_rel
