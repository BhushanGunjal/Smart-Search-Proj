import streamlit as st
import pandas as pd
from llm_utils import generate_user_plan
from product_search import match_shopping_plan_to_products

st.set_page_config(page_title="Smart Assistant", layout="centered")

st.title("🧠 Smart Bazaar Assistant")


user_query = st.text_input("What do you want to prepare or shop for?", placeholder="e.g., Upma for 2 people")




if user_query:
    with st.spinner("🧠 Thinking..."):
        result = generate_user_plan(user_query)

    if not result["valid"]:
        st.error("❌ Invalid query. Please try something shopping-related.")
    else:
        st.subheader("🛒 Smart Shopping Plan")
        for item in result["shopping_plan"]:
            col1, col2, col3 = st.columns([4, 2, 2])
            col1.markdown(f"**{item['item'].title()}**")
            col2.markdown(f"{item['purchase_quantity']}")
            col3.button("Find Products", key=item["item"])





    result2 = match_shopping_plan_to_products(result["shopping_plan"])
    print(result2)
    # st.write(result2)
    for i in range (len(result2)):
        recommendation = result2[i]
        st.subheader("Product Recommendation for " + result["ingredients"][i].title())
        for idx, row in recommendation.iterrows():
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"**{row['name']}**")
            col2.markdown(f"Price: ₹{row['price']}")
            st.button("Add to Cart", key=row["Product_ID"])









# # Step 2: Simulate product search page
# if "search_term" in st.session_state:
#     st.subheader(f"🔍 Products for: {st.session_state['search_term']}")
#     # You’ll replace this with FAISS results later
#     st.write("➡️ (Here you'd show product cards from FAISS search)")
