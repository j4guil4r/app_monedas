from ..patterns.singleton import APISingleton
from decimal import Decimal

class ExchangeService:
    def __init__(self, api_name: str = "ExchangeRateAPI"):
        self.api_name = api_name

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Decimal:
        # Cambiar adaptador según selección
        APISingleton().set_adapter(self.api_name)
        adapter = APISingleton().get_adapter()
        return Decimal(str(adapter.get_exchange_rate(from_currency, to_currency)))
    
    def convert_currency(self, amount:float, from_curr: str, to_curr: str) -> Decimal:
        # Obtiene la tasa del adaptador actual (Singleton)
        rate = self.get_exchange_rate(from_curr, to_curr)
        amount_decimal = Decimal(str(amount))
        return amount_decimal * rate