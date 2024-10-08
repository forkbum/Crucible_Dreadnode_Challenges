import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

###
# variables
#
CRUCIBLE_API_KEY = CRUCIBLE_API_KEY # my API key

CHALLENGE = "bear2"
CRUCIBLE_URL = "https://crucible.dreadnode.io"
CHALLENGE_URL = "https://bear2.crucible.dreadnode.io"

input_data = {"hunger": 1}
results = {}


###
# function to submit input data to retrieve flag
#
def query(input_data):
    payload = {"data": input_data}
    headers = {"Authorization": CRUCIBLE_API_KEY}
    response = requests.post(
        "https://bear2.crucible.dreadnode.io/score",
        headers=headers,
        json=input_data
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

for h in range(101):
    response = query({"hunger": h})
    results[h] = response['outputs'][0]
    print("..........")

df = pd.DataFrame(list(results.items()), columns=['Hunger', 'Happiness'])

# Plotting Hunger vs. Happiness
plt.figure(figsize=(10, 6))
plt.scatter(df['Hunger'], df['Happiness'], alpha=0.6)
plt.title('Hunger vs. Happiness Analysis')
plt.xlabel('Hunger Level')
plt.ylabel('Happiness Score')
plt.grid(True)
plt.show()

# Model replication
lr = LinearRegression()
lr.fit(df[['Hunger']], df['Happiness'])
print("coef: ", lr.coef_)

coef_data = {"coef": "{:.1f}".format(float(lr.coef_))}
print(coef_data)

response = query(coef_data)
print("flag: ", response['flag'])
submit_flag(response['flag'])

