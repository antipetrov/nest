import pytest
import requests
import json
from nesting.test import input_list, expected_result

WEB_BASE_URL = 'http://localhost:5000'


def test_web_request(input_list):

    session = requests.Session()
    session.auth = ('testuser', 'tes233tpassword')
    response = session.post(f'{WEB_BASE_URL}/?keys=currency,country,city', data=json.dumps(input_list))

    assert response
    assert expected_result == response.json()


def test_web_request_fail(input_list):
    session = requests.Session()
    session.auth = ('testuser', 'testpassword')

    response = session.post(f'{WEB_BASE_URL}/?keys=currency,country,city', data=json.dumps(input_list))
    assert response
    assert expected_result == response.json()
