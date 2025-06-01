import requests
from .base_api import CurrencyAPI

class ExchangeRateAPI(CurrencyAPI):
    BASE_URL = "https://open.er-api.com/v6/latest"
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        response = requests.get(f"{self.BASE_URL}/{from_currency}")
        data = response.json()
        
        if data.get("result") != "success":
            raise ValueError(f"Error en ER-API: {data.get('error-type', 'Unknown error')}")
            
        return data["rates"][to_currency]