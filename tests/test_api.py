import requests
import uuid
import os
import json
import time

API_IP = 'localhost'
API_PORT = 5000

PYTEST_DIR = os.path.dirname(__file__)
ROOT = os.path.dirname(PYTEST_DIR)


def test_dense_net_complex(mloc_env):
    mloc_env.start()

    endpoint = 'users'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    data = {'username': str(uuid.uuid4().hex), 'password': 'secret'}
    r = requests.post(url, json=data)
    assert r.json()['_status'] == 'OK'

    endpoint = 'login'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    r = requests.post(url, json=data)
    assert 'token' in r.json()

    headers = {'Authorization': 'token {}'.format(r.json()['token'])}

    endpoint = 'networks'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'dense', 'densenet.json')
    data = json.load(open(path, 'r'))
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    network = r.json()

    endpoint = 'fits'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'dense', 'densefit.json')
    data = json.load(open(path, 'r'))
    data['network_id'] = network['_id']
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    fit = r.json()

    while True:
        time.sleep(1)
        endpoint = 'fits'
        url = 'http://{}:{}/{}/{}'.format(
            API_IP, API_PORT, endpoint, fit['_id'])
        r = requests.get(url, headers=headers)
        if r.json()['state'] == 'finished':
            break

    endpoint = 'evaluations'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'dense', 'denseeval.json')
    data = json.load(open(path, 'r'))
    data['fit_id'] = fit['_id']
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    evaluation = r.json()

    while True:
        time.sleep(1)
        endpoint = 'evaluations'
        url = 'http://{}:{}/{}/{}'.format(
            API_IP, API_PORT, endpoint, evaluation['_id'])
        r = requests.get(url, headers=headers)
        if r.json()['state'] == 'finished':
            break

    endpoint = 'predictions'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'dense', 'densepredict.json')
    data = json.load(open(path, 'r'))
    data['fit_id'] = fit['_id']
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    prediction = r.json()

    while True:
        time.sleep(1)
        endpoint = 'predictions'
        url = 'http://{}:{}/{}/{}'.format(
            API_IP, API_PORT, endpoint, prediction['_id'])
        r = requests.get(url, headers=headers)
        if r.json()['state'] == 'finished':
            break

    mloc_env.stop()


def test_conv_net_complex(mloc_env):
    mloc_env.start()

    endpoint = 'users'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    data = {'username': str(uuid.uuid4().hex), 'password': 'secret'}
    r = requests.post(url, json=data)
    assert r.json()['_status'] == 'OK'

    endpoint = 'login'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    r = requests.post(url, json=data)

    headers = {'Authorization': 'token {}'.format(r.json()['token'])}

    endpoint = 'networks'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'conv', 'convnet.json')
    data = json.load(open(path, 'r'))
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    network = r.json()

    endpoint = 'fits'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'conv', 'convfit.json')
    data = json.load(open(path, 'r'))
    data['network_id'] = network['_id']
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    fit = r.json()

    while True:
        time.sleep(1)
        print('Waiting for model being created.')
        endpoint = 'fits'
        url = 'http://{}:{}/{}/{}'.format(
            API_IP, API_PORT, endpoint, fit['_id'])
        r = requests.get(url, headers=headers)
        if r.json()['state'] == 'finished':
            break

    endpoint = 'evaluations'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'conv', 'conveval.json')
    data = json.load(open(path, 'r'))
    data['fit_id'] = fit['_id']
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    evaluation = r.json()

    while True:
        time.sleep(1)
        endpoint = 'evaluations'
        url = 'http://{}:{}/{}/{}'.format(
            API_IP, API_PORT, endpoint, evaluation['_id'])
        r = requests.get(url, headers=headers)
        if r.json()['state'] == 'finished':
            break

    endpoint = 'predictions'
    url = 'http://{}:{}/{}'.format(API_IP, API_PORT, endpoint)
    path = os.path.join(ROOT, 'examples', 'conv', 'convpredict.json')
    data = json.load(open(path, 'r'))
    data['fit_id'] = fit['_id']
    r = requests.post(url, json=data, headers=headers)
    assert r.json()['_status'] == 'OK'
    prediction = r.json()

    while True:
        time.sleep(1)
        endpoint = 'predictions'
        url = 'http://{}:{}/{}/{}'.format(
            API_IP, API_PORT, endpoint, prediction['_id'])
        r = requests.get(url, headers=headers)
        print(r.json())
        if r.json()['state'] == 'finished':
            break

    mloc_env.stop()
