import pandas as pd
import numpy as np

df = pd.read_excel(r'datasets\catalog.xlsx')
print("Duplicates: ", df.duplicated().sum())    

print("Data at product_id 0: ", df.iloc[13575:13580])