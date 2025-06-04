import requests
from .base_api import CurrencyAPI

class MoneyMorphAPI(CurrencyAPI):
    BASE_URL = "https://moneymorph.dev/api/latest"
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        params = {
            "base": from_currency,
            "symbols": to_currency
        }
        
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        
        if not data["rates"]:
            raise ValueError(f"Moneda {to_currency} no soportada por MoneyMorph")
        
        if response.status_code != 200:
            raise ValueError(f"Error en MoneyMorph: {data.get('error', 'Unknown error')}")
        
        return data["rates"][to_currency]