import requests
import certifi

url = "https://api.themoviedb.org/3/movie/58?api_key=ec6689028c28f8828e66c8bffaa192d1&language=en-US"
try:
    response = requests.get(url, verify=certifi.where())
    print(response.status_code, response.text)
except requests.exceptions.SSLError as e:
    print("SSL Error:", e)
