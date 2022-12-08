import requests

myNumber = 'user1'

BASE_URL = 'http://127.0.0.1:8080'

data_sent = {'user': myNumber}
response = requests.post(BASE_URL + '/home', data=data_sent)
print('Server responded to get with:', response.text)
