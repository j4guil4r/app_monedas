from ..adapters import ExchangeRateAPI, FrankfurterAPI

class APISingleton:
    # unica instancia
    _instance = None
    _current_adapter = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            # Adaptador por defecto (es el mejor creo)
            cls._current_adapter = ExchangeRateAPI()
        return cls._instance
    
    @classmethod
    def set_adapter(cls, adapter_name: str):
        
        if adapter_name == "ExchangeRateAPI":
            cls._current_adapter = ExchangeRateAPI()
        elif adapter_name == "FrankfurterAPI":
            cls._current_adapter = FrankfurterAPI()
        else:
            raise ValueError("Adaptador no válido")
    
    @classmethod
    def get_adapter(cls):
        return cls._current_adapter