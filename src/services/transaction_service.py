from ..database.session import SessionLocal
from ..patterns.observer import TransactionObserver
from ..database.models import Transaction, Account
from ..services.exchange_service import ExchangeService
from decimal import Decimal

class TransactionService:
    def __init__(self):
        self.db = SessionLocal()
        self.observer = TransactionObserver()
        self.exchange_service = ExchangeService()
    
    def transfer(self, sender_id: int, receiver_id: int, amount: float, convert_currency: bool = False):
        # Lógica de transferencia
        try:
            amount_decimal = Decimal(str(amount))
            sender_account = self.db.query(Account).filter_by(id=sender_id).one()
            receiver_account = self.db.query(Account).filter_by(id=receiver_id).one()

            # Validar saldo suficiente
            if sender_account.balance < amount:
                raise ValueError("Saldo insuficiente")

            # Conversión de moneda si es necesario
            if convert_currency or sender_account.currency != receiver_account.currency:
                converted_amount = self.exchange_service.convert_currency(
                    amount, sender_account.currency, receiver_account.currency
                )
                exchange_rate = converted_amount / amount
            else:
                converted_amount = amount
                exchange_rate = 1.0

            # Actualizar saldos
            sender_account.balance -= amount_decimal
            receiver_account.balance += converted_amount

            # Registrar transacción
            transaction = Transaction(
                amount=amount,
                currency=sender_account.currency,
                sender_account_id=sender_id,
                receiver_account_id=receiver_id,
                exchange_rate=exchange_rate,
            )
            self.db.add(transaction)
            self.db.commit()
            self.observer.notify(transaction.__dict__)

            return {
                "message": "Transferencia exitosa",
                "original_amount": amount,
                "converted_amount": converted_amount,
                "exchange_rate": exchange_rate
            }

        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()