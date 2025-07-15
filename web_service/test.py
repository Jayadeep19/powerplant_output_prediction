import requests

conditions = d = {'AT':[20],
        'V':[50],
        'AP': [1015],
        'RH': [75]}

url = "http://localhost:9696/predict"
response = requests.post(url, json=conditions)
print(response.json())