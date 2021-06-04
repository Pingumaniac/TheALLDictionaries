import requests

r = requests.get('https://type.fit/api/quotes')

jsonOutput = r.json()

text = []
for data in jsonOutput:
    text.append(data['text'])

print(text)
