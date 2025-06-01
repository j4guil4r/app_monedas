import requests
from .base_api import CurrencyAPI

class FrankfurterAPI(CurrencyAPI):
    BASE_URL = "https://api.frankfurter.dev/v1/latest"
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        params = {
            "base": from_currency,
            "symbols": to_currency
        }
        
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        
        if response.status_code != 200:
            raise ValueError(f"Error en Frankfurter: {data.get('message', 'Unknown error')}")
        
        return data["rates"][to_currency]