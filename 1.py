import requests


x = requests.delete('http://127.0.0.1:8000/api/likes/1_8')
print(x)