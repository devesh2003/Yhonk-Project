import requests
import json

def get_balance(key):
    url = "https://us1.locationiq.com/v1/balance.php"

    data = {
        'key': key
    }

    response = requests.get(url, params=data)
    data = json.loads(response.text)
    return data['balance']['day']

print(get_balance('e70d408d0bfdea'))