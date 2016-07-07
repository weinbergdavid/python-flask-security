import json
import requests

r = requests.post('http://127.0.0.1:5001/login', data=json.dumps({'email':'test@example.com', 'password':'test123'}), headers={'content-type': 'application/json'})

token = r.json()['response']['user']['authentication_token']
print(token)
