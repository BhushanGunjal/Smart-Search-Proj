
# ----------------------------------------------------------------------------------------------------------------------
# -----------THIS CODE WAS USED TO CREATE CONCATENATED EXCEL FILE FROM MULTIPLE SHEETS IN A SINGLE WORKBOOK--------------
# -----------------------------------------------------------------------------------------------------------------------


# import pandas as pd

# # Path to your input Excel file
# input_file = 'D:\Reliance\Rel\datasets\zepto_scraped_data.xlsx'

# # Read all sheets into a dictionary of DataFrames
# sheets = pd.read_excel(input_file, sheet_name=None)

# # Concatenate all sheet DataFrames into one
# combined_df = pd.concat(sheets.values(), ignore_index=True)

# # Export to new Excel file
# combined_df.to_excel('combined_output.xlsx', index=False)

# print("✅ All sheets combined into 'combined_output.xlsx'")


# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------TO CHECK PD FILE--------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

import pandas as pd

df = pd.read_pickle("product_catalog_with_embeddings.pkl")

print(df.head())

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------TEMP FILE FOR EMBEDDINGS--------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


# import pandas as pd
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer
# from sklearn.preprocessing import normalize

# # === 1. Load all components once ===
# df = pd.read_pickle("product_catalog_with_embeddings.pkl")
# index = faiss.read_index("faiss_product_index.index")

# with open("embedding_model_used.txt") as f:
#     model_name = f.read().strip()

# model = SentenceTransformer(model_name)

# # === 2. Search Function ===
# def smart_meaning_search(user_query, k=50, max_per_subcategory=1, max_total=10):
#     # Encode and normalize the query
#     query_embedding = model.encode([user_query])
#     query_embedding = normalize(query_embedding, norm='l2')

#     # Top-N raw matches from FAISS
#     D, I = index.search(query_embedding, k)

#     # Build initial result frame
#     results = df.iloc[I[0]].copy()
#     results["similarity"] = D[0]

#     # Group by subcategory and take top N per group
#     grouped = results.groupby("subcategory").head(max_per_subcategory)

#     # Trim to max total number of results (optional)
#     final_results = grouped.head(max_total)

#     return final_results[["Product_ID", "name", "subcategory", "price", "similarity"]]




# def match_shopping_plan_to_products(shopping_plan, top_k=3):
#     """
#     shopping_plan: list of dicts like
#         [
#             { "item": "plastic cups", "purchase_quantity": "1 pack (10 pcs)" },
#             { "item": "snacks", "purchase_quantity": "1 big pack" },
#         ]
#     Returns: dict with top_k matches per item
#     """
#     # Step 1: Create search queries like "plastic cups 1 pack (10 pcs)"
#     queries = [f"{item['item']} {item['purchase_quantity']}" for item in shopping_plan]

#     # Step 2: Embed all queries at once
#     query_embeddings = model.encode(queries)
#     query_embeddings = normalize(query_embeddings, norm='l2')

#     # Step 3: Search FAISS for each query
#     D, I = index.search(query_embeddings, top_k)

#     # Step 4: Format results
#     results = []
#     for idx, query in enumerate(queries):
#         matched_items = df.iloc[I[idx]].copy()
#         matched_items["similarity"] = D[idx]
#         matched_items["query"] = query
#         results.append(matched_items[["query", "Product_ID", "name", "subcategory", "price", "similarity"]])

#     return results  # list of dataframes (one per item)


# # === 3. Interactive CLI Loop ===
# if __name__ == "__main__":
#     while True:
#         user_query = input("\n🧠 Enter your search query (or 'exit'): ")
#         if user_query.lower() == "exit":
#             break

#         results = smart_meaning_search(user_query)
#         print("\n🎯 Top meaning-based results:")
#         print(results.to_string(index=False))



# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


