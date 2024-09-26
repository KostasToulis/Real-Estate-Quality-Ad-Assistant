import pandas as pd
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s\n')


# Assuming the Groq API is correctly installed and set up.
from groq import Groq



def paraphrase(text,API_key):
    client = Groq(api_key=API_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a real estate ad paraphraser AI tool. Paraphrase the ad descriptions given, maintaining all information.
                Use a different style of language.
                Mix the information sequence.
                Do not add or remove any information. 
                Return only the rephrased ad, no introductory sentences.""",
            },
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-groq-70b-8192-tool-use-preview"
    )

    return chat_completion.choices[0].message.content

def multiple_paraphrase(text):
    a = paraphrase(text,"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")
    print(a)
    print('\nDone 1\n')
    time.sleep(1.5)
    b = paraphrase(text,'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')
    print(b)
    print('\nDone 2\n')
    time.sleep(1.5)
    c = paraphrase(text,'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')
    print(c)
    print('\nDone 3\n')
    time.sleep(1.5)
    print('\nDone All\n')
    return [a, b, c]

# Load the CSV file
df = pd.read_excel("C:\\Users\\jtsou\\Documents\\University\\MSc Business Analytics\\3rd Semester\\Machine Learning and Content Analytics\\Project\\ads_final.xlsx")

# Store the new paraphrased descriptions
new_descriptions = []

data = df['Description'].astype(str)

# data = data.iloc[0:3,]

l = 0
for i in data:
    paraphrased_ads = multiple_paraphrase(i)
    new_descriptions.append(paraphrased_ads)
    l += 1
    print(f'\nElement {l} done!\n')
    time.sleep(1)

# Convert the list of paraphrases into a DataFrame
paraphrased_df = pd.DataFrame(new_descriptions, columns=['Paraphrase1', 'Paraphrase2', 'Paraphrase3'])

# Save the paraphrased descriptions to a new CSV file
paraphrased_df.to_csv("C:\\Users\\jtsou\\Desktop\\paraphrased_ads.csv", index=False)

print('Results written to paraphrased_ads.csv')
