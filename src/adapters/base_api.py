from abc import ABC, abstractmethod

class CurrencyAPI(ABC):
    @abstractmethod
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        pass