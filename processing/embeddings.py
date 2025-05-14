import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import faiss
import pickle

# === 1. Load your product catalog ===
input_path = r'datasets\catalog.xlsx'
df = pd.read_excel(input_path)

# === 2. Preprocess text for embeddings ===
df['name'] = df['name'].fillna('')
df['subcategory'] = df['subcategory'].fillna('')
df['text_for_embedding'] = df['name'] + ' ' + df['subcategory']

# === 3. Generate sentence embeddings ===
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['text_for_embedding'].tolist(), show_progress_bar=True)
df['embedding'] = embeddings.tolist()

# === 4. Prepare embeddings for FAISS (cosine similarity setup) ===
embedding_matrix = np.vstack(df['embedding'].to_numpy())
embedding_matrix = normalize(embedding_matrix, norm='l2')

# === 5. Create FAISS index ===
dimension = embedding_matrix.shape[1]
index = faiss.IndexFlatIP(dimension)  # IP = inner product
index.add(embedding_matrix)

# === 6. Save everything ===
df.to_pickle('product_catalog_with_embeddings.pkl')

# Save FAISS index to disk
faiss.write_index(index, 'faiss_product_index.index')

# Optional: Save embedding model name and metadata
with open('embedding_model_used.txt', 'w') as f:
    f.write('all-MiniLM-L6-v2')
