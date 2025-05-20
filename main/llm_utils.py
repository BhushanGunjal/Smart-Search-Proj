from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import json
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


from langchain.prompts import PromptTemplate

Template1 = PromptTemplate(
    template="""
You are a smart assistant that determines whether a user's input is a valid shopping-related query for Smart Bazaar.

Your job is to classify the query in hyphens --{user_input}-- as either:

- "Valid" → if the query reflects a real shopping intent, such as:
  - buying products
  - finding ingredients
  - preparing for an event (e.g., birthday, party, pooja)
  - planning a grocery list
  - requesting product suggestions based on an occasion or dietary need

- "Invalid Query" → if the query is:
  - a question about unrelated topics
  - casual, unclear, or not focused on shopping
  - asking for help, features, or technical support

### Valid Examples:
- "pohe for 2 people"
- "birthday snacks for 10 kids"
- "weekly groceries for a diabetic"
- "buy milk and bread"
- "dry fruits under ₹300"

### Invalid Examples:
- "how does Smart Bazaar work?"
- "track my order"
- "call customer support"
- "what is the return policy?"
- "hi"

Only output one word: either **Valid** or **Invalid Query**
""",
    input_variables=["user_input"]
)





IngredientListPrompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are a smart shopping assistant.

Your task is to extract a list of essential ingredients or items based on the user’s input. 
The input may be a dish, an occasion, or a shopping intent.

The user input is: "{user_input}"

Instructions:
- Understand what items would be needed to fulfill this shopping task
- Do not include quantities or steps
- Only list the item names (in lowercase, retail-friendly names)
- Return the result as a flat JSON array

Example output:
["semolina", "onion", "green chili", "mustard seeds", "oil", "salt"]
"""
)










RetailQuantityPrompt = PromptTemplate(
    input_variables=["user_input", "items"],
    template="""
You are a smart grocery shopping assistant.

Based on the user's context: "{user_input}", convert the following item names into realistic retail purchase quantities suitable for a platform like Smart Bazaar.

Instructions:
- Suggest quantities in standard pack sizes (e.g., 100g, 500g, 1L, 6 pcs)
- Always return the **minimum viable pack size** needed
- Assume items are being purchased fresh or packaged (whichever is typical)
- Return a clean JSON list with item and purchase_quantity

Item list:
{items}

Example output:
[
  {{ "item": "onion", "purchase_quantity": "500g" }},
  {{ "item": "oil", "purchase_quantity": "1L" }},
  {{ "item": "green chili", "purchase_quantity": "100g" }}
]
"""
)




def generate_user_plan(query: str):
        

        prompt1 = Template1.invoke({"user_input": query})

        response1 = llm.invoke(prompt1)

        print("Is it a Valid Query:", response1.content)

        if response1.content != "Valid":
            return {"valid": False, "error": "Invalid Query", "ingredients": [], "shopping_plan": []}
            print("Invalid Query")

        else:

            prompt2 = IngredientListPrompt.invoke({"user_input": query})
            response2 = llm.invoke(prompt2)
            ingredients = json.loads(response2.content)
            print("LLM response: ",ingredients)

            prompt3 = RetailQuantityPrompt.invoke({"user_input": query, "items": ingredients})
            response3 = llm.invoke(prompt3)
            shopping_plan = json.loads(response3.content)
            print(shopping_plan)

        return {
        "valid": True,
        "ingredients": ingredients,
        "shopping_plan": shopping_plan
    }


op = generate_user_plan("upma for 2 people")
print(op)







