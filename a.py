import requests

url = 'https://ipinfo.io'
username = 'kpsingh'
password = 'fuqbY1-nonmeg-hevxef'

proxy = 'http://kpsingh:fuqbY1-nonmeg-hevxef@gate.dc.smartproxy.com:20000'

response = requests.get(url, proxies={'http': proxy, 'https': proxy})

print(response.text)
