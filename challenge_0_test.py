import requests
import json

###
# variables
#
CRUCIBLE_API_KEY = CRUCIBLE_API_KEY # my API key

CHALLENGE = "test"
CRUCIBLE_URL = "https://crucible.dreadnode.io"
CHALLENGE_URL = "https://test.crucible.dreadnode.io"

###
# send request to retrieve flag
#
def query(input_data):
    response = requests.post(
        f"{CHALLENGE_URL}/score",
        headers={"Authorization": CRUCIBLE_API_KEY},
        json={"data": input_data}
    )
    return response.json()

###
# send request to submit flag
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

submit_flag(query("flag please?")['flag'])


