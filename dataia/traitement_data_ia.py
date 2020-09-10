import requests
# pprint is used to format the JSON response
from pprint import pprint
import os

subscription_key = "c42ac7b0e0944f748407efd276d748ff"
endpoint = "https://cs-groupe-trois.cognitiveservices.azure.com/"

liste = []

print("Sentiments :")

sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"

documents = {"documents": [
    {"id": "1", "language": "fr",
        "text": "Je suis content."},
    {"id": "2", "language": "fr",
        "text": "Cela ne me fait ni chaud, ni froid."},
    {"id": "3", "language": "fr",
        "text": "Ca me donne envie d'hurler"},
]}

for i in documents:
    liste = documents["documents"]
    liste.append({"id": "4", "language": "fr",
        "text": "Comment ça va ?"})

    """for d in documents["documents"]:
        for k, v in d.items(): 
            if (k is 'text'):
                print(v)

    print (liste)"""

"""res = [[i for i in documents[x]] for x in test_dict.keys()] 
	
# printing result 
print("Résultat : " + str(res)) """


headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(sentiment_url, headers=headers, json=documents)
sentiments = response.json()
#pprint(sentiments["documents"])

"""for d in sentiments:
    for d in sentiments["documents"]:
        for k, v in d.items(): 
            print(k, v)
            if (k == 'id'):
                print(v)"""

#for i in sentiments:
for j in sentiments["documents"]:
    print(j['id'])
    for repere, valeur in j.items(): 
        if (repere == 'sentences'):
            for k in valeur:
                for repere2, valeur2 in k.items(): 
                    if (repere2 == 'confidenceScores'):
                        for l in valeur2:
                            print(l, valeur2['positive'])
                            print(l, valeur2['neutral'])
                            print(l, valeur2['negative'])

