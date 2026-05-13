import json
import requests
import pandas as pd

url = 'http://localhost:5000/movimentos/power/4/600'
json_url = requests.get(url)
data = json.loads(json_url.text)
#print(data)
df = pd.DataFrame(data['content'])
print(df)