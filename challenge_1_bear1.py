import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # For data visualization

###
# variables
#
CRUCIBLE_API_KEY = CRUCIBLE_API_KEY # my API key

CHALLENGE = "bear1"
CRUCIBLE_URL = "https://crucible.dreadnode.io"
CHALLENGE_URL = "https://bear1.crucible.dreadnode.io"

###
# function to submit input data to retrieve flag
#
def query(input_data):
    response = requests.post(
        f"{ CHALLENGE_URL }/score",
        headers={"Authorization": CRUCIBLE_API_KEY},
        json={"data": input_data}
    )
    return response.json()

###
# function to submit flag
#
def submit_flag(flag):
    url = f"{CRUCIBLE_URL}/api/submit-flag"
    headers = {"Authorization": CRUCIBLE_API_KEY}
    payload = {"challenge": CHALLENGE, "flag": flag}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        if response.json().get("correct") is True:
            print("The flag was correct. Congrats!")
        else:
            print("The flag was incorrect. Keep trying!")
    else:
        print("There was an error submitting your flag")
        print(response.text)

###

# load CSV into a pandas DataFrame
df = pd.read_csv('data/bear.csv')

# display data types and any missing info
print(df.info())

# data analysis on a plot
df['tune'].plot(kind='hist', bins=25, title='Distribution of `tune` Feature')
plt.xlabel('Tune Value')
plt.ylabel('Frequency')
plt.show()

# displaying unique characters in the 'val' column
unique_values = df['val'].unique()
print("\nUnique characters in the 'val' column:", unique_values)

# group by the bear type and aggregate to the average `tune` value
mean_tunes = df.groupby('bear')['tune'].mean()
print("\nBear types with average 'tune' values", mean_tunes)

# sorting the DataFrame by 'tune' in descending order to see the top values
top_tunes = df.sort_values('tune').head(5)
print("\nSort by 'tune' in descending order", top_tunes)

# filtering to find entries where 'tune' values are above a certain threshold
high_tune_bears = df[df['tune'] > 90]
print("\nFilter for 'tune' values above a threshold", high_tune_bears.head(5))

# applying multiple conditions to find a specific subset of data
specific_bears = df[(df['tune'] > 50) & (df['bear'] == 'Kodiak')]
print("\nIdentify subset of data", specific_bears.head(5))

# Sorting the data by 'tune' in descending order to focus on the highest values
sorted_data = df.sort_values('tune', ascending=False)
sorted_data.head()

# Grouping by 'bear' type and taking the top entry for each group based on 'tune' value
top_bears = df.sort_values('tune', ascending=False).groupby('bear').head(1)
top_bears = top_bears.sort_values('bear')  # Sorting by bear type for easier visualization
print("\nSorted by type and top 'tune' values", top_bears)

# Extracting characters from the 'val' column
characters = top_bears['val'].tolist()
secret_word = ''.join(characters)
# print("Secret Word:", secret_word)
secret_word = [c for c in secret_word if c not in ['{','}',' ']]
secret_word = ''.join(secret_word)
print("Secret Word:", secret_word)


response = query(secret_word)
print("flag: ", response['flag'])
submit_flag(response['flag'])
