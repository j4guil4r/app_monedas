from ..patterns.singleton import APISingleton
from decimal import Decimal

class ExchangeService:
    def convert_currency(self, amount:float, from_curr: str, to_curr: str) -> float:
        # Obtiene la tasa del adaptador actual (Singleton)
        api = APISingleton().get_adapter()
        rate = Decimal(str(api.get_exchange_rate(from_curr, to_curr)))
        amount_decimal = Decimal(str(amount))
        return amount_decimal * rate