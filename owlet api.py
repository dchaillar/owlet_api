# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 21:42:56 2023

@author: dchaillar
"""

import requests, json, time 
from datetime import datetime

secret_json = r"secret_file.json"

r = requests.post(
    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={}".format(secret_json['google_api_key']),
    data=json.dumps(
        {
            "email": secret_json['email'],
            "password": secret_json['pw'],
            "returnSecureToken": True,
        }
    ),
    headers={
        "X-Android-Package": "com.owletcare.owletcare",
        #found this online and put it in the secret file
        "X-Android-Cert": secret_json['android_cert'],
    },
)
print(r.status_code)
id_token = r.json()['idToken']

r = requests.get(
                "https://ayla-sso.owletdata.com/mini/",
                headers={"Authorization": id_token},
            )
print(r.status_code)
mini_token = r.json()['mini_token']

r = requests.post(
    "https://user-field-1a2039d9.aylanetworks.com/api/v1/token_sign_in",
    json={
        "app_id": "sso-prod-3g-id",
        "app_secret": "sso-prod-UEjtnPCtFfjdwIwxqnC0OipxRFU",
        "provider": "owl_id",
        "token": mini_token,
    },
)

print(r.status_code)
auth_token = r.json()['access_token']
refresh_token = r.json()['refresh_token']


device_url = 'https://ads-field-1a2039d9.aylanetworks.com/apiv1/devices.json'
r = requests.get(
    device_url,
    headers={"Authorization": "auth_token " + auth_token}
)
print(r.status_code)

device_number = r.json()[0]['device']['dsn']

for i in range(0,360):
    r = requests.get(
        f"https://ads-field-1a2039d9.aylanetworks.com/apiv1/dsns/{device_number}/properties.json",
        headers={"Authorization": "auth_token " + auth_token}
    )
    device_properties = {"DSN":device_number}
    
    for prop in r.json():
        device_properties[prop["property"]["name"]] = prop["property"]
        
    vitals = json.loads(device_properties["REAL_TIME_VITALS"]["value"])
    print('At ' +str(datetime.now()) + ' Heartrate is ' + str(vitals['hr']) + ' Ox is ' + str(vitals['ox']) + ' Movement is ' + str(vitals['mv']))
    time.sleep(10)




