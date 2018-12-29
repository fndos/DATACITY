# -*- coding: utf-8 -*-
import requests

def get_data():
    try:
        # Es probable que esto no funcione hasta que se ponga en produccion
        url = 'http://127.0.0.1:8000/api/'
        r = requests.get(url)
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        print('exception caught', e)
