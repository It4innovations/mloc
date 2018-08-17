import requests
import json
import time

API_IP = 'localhost'
API_PORT = 5000

endpoint = 'networks'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('densenet.json', 'r'))
r = requests.post(url, json=data)
network = r.json()

endpoint = 'fits'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('densefit.json', 'r'))
data['network_id'] = network['_id']
r = requests.post(url, json=data)
fit = r.json()

while True:
    time.sleep(1)
    print('Waiting for model being created.')
    endpoint = 'fits'
    url = 'http://{}:{}/{}/{}'.format(API_IP, API_PORT, endpoint, fit['_id'])
    r = requests.get(url)
    if r.json()['state'] == 'finished':
        break

endpoint = 'evaluations'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('denseeval.json', 'r'))
data['fit_id'] = fit['_id']
r = requests.post(url, json=data)
evaluation = r.json()

endpoint = 'predictions'
url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
data = json.load(open('densepredict.json', 'r'))
data['fit_id'] = fit['_id']
r = requests.post(url, json=data)
prediction = r.json()
