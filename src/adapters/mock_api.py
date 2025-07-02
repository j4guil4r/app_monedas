import time

class MockAPI:
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        print("💡 Usando MOCK API con delay")
        time.sleep(0.5)  # Simula la espera de 500ms

        if from_currency == to_currency:
            return 1.0
        return 3.5