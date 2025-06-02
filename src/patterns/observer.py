class TransactionObserver:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, transaction_data: dict):
        for observer in self._observers:
            observer.update(transaction_data)