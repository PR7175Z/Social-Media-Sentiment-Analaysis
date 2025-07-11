import requests

url = 'http://127.0.0.1:2000/predict'

data = {'text': "This is not nice. I hate it."}
response = requests.post(url, json=data)

print(response.json())