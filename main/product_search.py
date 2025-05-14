import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import streamlit as st





# === 1. Cached resource loaders ===

@st.cache_resource(show_spinner="🔄 Loading embedding model...")
def load_embedding_model():
    with open("embedding_model_used.txt") as f:
        model_name = f.read().strip()
    return SentenceTransformer(model_name)


@st.cache_resource(show_spinner="🔄 Loading FAISS index...")
def load_faiss_index():
    return faiss.read_index("faiss_product_index.index")


@st.cache_data(show_spinner="🔄 Loading product catalog...")
def load_catalog():
    return pd.read_pickle("product_catalog_with_embeddings.pkl")







# === 2. Semantic product search per shopping item ===

def match_shopping_plan_to_products(shopping_plan, top_k=3):
    """
    shopping_plan: list of dicts like
        [
            { "item": "plastic cups", "purchase_quantity": "1 pack (10 pcs)" },
            { "item": "snacks", "purchase_quantity": "1 big pack" },
        ]
    Returns: list of DataFrames (1 per item), each with top_k product matches
    """
    model = load_embedding_model()
    index = load_faiss_index()
    df = load_catalog()

    # Step 1: Combine item + quantity as search queries
    queries = [f"{item['item']} {item['purchase_quantity']}" for item in shopping_plan]
    print("Queries: ", queries)
    # Step 2: Embed + normalize all at once
    query_embeddings = model.encode(queries)
    query_embeddings = normalize(query_embeddings, norm='l2')

    # Step 3: Search FAISS
    D, I = index.search(query_embeddings, top_k)

    # Step 4: Prepare results
    results = []
    for idx, query in enumerate(queries):
        matched_items = df.iloc[I[idx]].copy()
        matched_items["similarity"] = D[idx]
        matched_items["query"] = query
        results.append(matched_items[["query", "Product_ID", "name", "subcategory", "price", "similarity"]])

    return results
