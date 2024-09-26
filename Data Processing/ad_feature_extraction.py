import re
from groq import Groq
import pandas as pd
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API = "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"



def ad_description_features(desc,API_key):
    client = Groq(api_key=API_key)
    chat_completion = client.chat.completions.create(
            messages=[
        {
            "role": "system",
            "content": """You are a helpful real estate assistant. You take real estate descriptions and check if they contain the features below:
            1) public transport stations (metro,bus,etc)
            2) amenities (for example: supermarkets, parks, schools, universities,Shopping centers and grocery stores, parking, A/C, not rooms like kitchen or bathroom)
            3) layout (how many and what rooms it has, size is not considered a layout)
            4) house type (apartment, full house, building, etc)
            First answer if the features are present with yes/no and then specify why.
            Don't assume information not specified in the description. 
            Don't write information not asked above.
            """
        },      
        {
            "role": "user",
            "content": desc,
        }
            ],
            model="llama3-groq-70b-8192-tool-use-preview"
        )

    
    return chat_completion.choices[0].message.content


# def ad_description_feature_list(desc):
#     features = ad_description_features(desc)
#     ls = re.search(r'\[(\d,\d,\d,\d)\]', features)
#     if ls:
#         print(features)
#         return [int(x) for x in ls.group(1).split(',')]
#     else:
#         return ad_description_features(desc) 

def update_csv(input_file, output_file,api_keys):
    df = pd.read_excel(input_file)
    
    # Convert the 'Description' column to strings
    df['Input'] = df['Input'].astype(str)
    df = df.iloc[0:638,]
    
    output_list = []

    num_keys = len(api_keys)
    
    for index, desc in enumerate(df['Input']):
        api_key = api_keys[index % num_keys]
        print('Using Key: ',api_key)
        time.sleep(0.2)
        output = ad_description_features(desc,api_key)          
        output_list.append(output)
        print(output)
        print(f"\nRow {index + 1} Done\n")
        time.sleep(1.5)
    
    features_df = pd.DataFrame(output_list, columns=['Output'])
    features_df.to_csv(output_file, index=False)
    print('Saved in ads_groq_output_test.csv')

# Usage
input_file = "C:\\Users\\jtsou\\Documents\\University\\MSc Business Analytics\\3rd Semester\\Machine Learning and Content Analytics\\Project\\ads_final.xlsx"
output_file = "C:\\Users\\jtsou\Documents\\University\\MSc Business Analytics\\3rd Semester\\Machine Learning and Content Analytics\\Project\\ads_groq_output_test.csv"
api_list = ['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',
            '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',
            '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']
update_csv(input_file, output_file,api_list)
