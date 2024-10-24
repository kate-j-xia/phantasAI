import requests
import json
import datetime

url = "http://localhost:6188/users/"

user = {"name" : "Ashley J.", "date": datetime.datetime.now()}
data_json = json.dumps(user, default=str)
headers = {'Content-type': 'application/json'}

response = requests.post(url, data=data_json, headers=headers)