import requests
import time

url = "http://localhost:8000/api/exchange/rate"
params = {
    "from_curr": "USD",
    "to_curr": "PEN",
    "api": "ExchangeRateAPI"
}

start = time.time()
response = requests.get(url, params=params)
end = time.time()

print(f"⏱ Tiempo total: {end - start:.3f} segundos")
print("Respuesta:", response.json())