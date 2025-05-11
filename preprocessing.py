import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import sys
sys.path.append(sys.path[0] + '/..')
from utils.ConfigManager import ConfigManager as CM

SOURCEFILE = CM().get('data.source')
DESTFILE = CM().get('data.index')

df = pd.read_csv(SOURCEFILE)["word"].to_frame()

text = df["word"]
encoder = SentenceTransformer(CM().get('encoder'))
vectors = encoder.encode(text)

df['vectors'] = vectors.tolist()

vector_dimension = vectors.shape[1]
index = faiss.IndexFlatL2(vector_dimension)
faiss.normalize_L2(vectors)
index.add(vectors)

faiss.write_index(index, DESTFILE)
