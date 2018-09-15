import requests
import json
import time
import uuid


API_IP = 'localhost'
API_PORT = 5000

endpoint = 'users'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = {'username': str(uuid.uuid4().hex), 'password': 'secret'}
r = requests.post(url, json=data)

endpoint = 'login'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
r = requests.post(url, json=data)

headers = {'Authorization': 'token {}'.format(r.json()['token'])}

endpoint = 'networks'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('convnet.json', 'r'))
r = requests.post(url, json=data, headers=headers)
network = r.json()

endpoint = 'fits'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('convfit.json', 'r'))
data['network_id'] = network['_id']
r = requests.post(url, json=data, headers=headers)
fit = r.json()

while True:
    time.sleep(1)
    print('Waiting for model being created.')
    endpoint = 'fits'
    url = 'http://{}:{}/{}/{}'.format(API_IP, API_PORT, endpoint, fit['_id'])
    r = requests.get(url, headers=headers)
    if r.json()['state'] == 'finished':
        break

endpoint = 'evaluations'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('conveval.json', 'r'))
data['fit_id'] = fit['_id']
r = requests.post(url, json=data, headers=headers)
evaluation = r.json()

while True:
    time.sleep(1)
    print('Waiting for evaluations')
    endpoint = 'evaluations'
    url = 'http://{}:{}/{}/{}'.format(API_IP, API_PORT, endpoint, evaluation['_id'])
    r = requests.get(url, headers=headers)
    print(r.json())
    if r.json()['state'] == 'finished':
        break

endpoint = 'predictions'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('convpredict.json', 'r'))
data['fit_id'] = fit['_id']
r = requests.post(url, json=data, headers=headers)
prediction = r.json()

while True:
    time.sleep(1)
    print('Waiting for predictions.')
    endpoint = 'predictions'
    url = 'http://{}:{}/{}/{}'.format(API_IP, API_PORT, endpoint, prediction['_id'])
    r = requests.get(url, headers=headers)
    print(r.json())
    if r.json()['state'] == 'finished':
        break