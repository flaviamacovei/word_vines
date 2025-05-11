import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import sys
sys.path.append(sys.path[0] + '/..')

from utils.ConfigManager import ConfigManager as CM
def main():
    print("Hello from word-vines!")
    index_path = CM().get('data.index')
    index = faiss.read_index(index_path)
    encoder = SentenceTransformer(CM().get('encoder'))
    vocab = pd.read_csv(CM().get('data.source'))

    search_text = "cat"
    search_vector = encoder.encode(search_text)
    _vector = np.array([search_vector])
    faiss.normalize_L2(_vector)

    k = 1.2
    _, distances, ann = index.range_search(_vector, k)

    num_results = len(distances)

    vecs = np.zeros((num_results, 768))
    for i, val in enumerate(range(0, num_results)):
        vecs[i, :] = index.reconstruct(val)

    results = pd.DataFrame({'distance': distances, 'ann': ann, 'embedding': vecs.tolist()})
    merged = pd.merge(results, vocab, how='left', left_on='ann', right_index=True)
    print(f"columns: {merged.columns}")
    print(merged.sort_values(by = ['distance']))


if __name__ == "__main__":
    main()
