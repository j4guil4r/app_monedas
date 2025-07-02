from ..database.session import SessionLocal
from ..database.models import Transaction, Account
from ..services.exchange_service import ExchangeService
from sqlalchemy.orm.exc import NoResultFound
from decimal import Decimal

class TransactionService:
    def __init__(self):
        self.db = SessionLocal()
    
    def transfer(self, sender_id: int, receiver_id: int, amount: float, api_name: str = "ExchangeRateAPI"):
        # Lógica de transferencia
        try:
            amount_decimal = Decimal(str(amount))
            sender_account = self.db.query(Account).filter_by(id=sender_id).one()
            receiver_account = self.db.query(Account).filter_by(id=receiver_id).one()

            # Validar saldo suficiente
            if sender_account.balance < amount:
                raise ValueError("Saldo insuficiente")
            
            exchange_service = ExchangeService()

            # Conversión de moneda si es necesario
            if sender_account.currency != receiver_account.currency:
                converted_amount = exchange_service.convert_currency(
                    amount, sender_account.currency, receiver_account.currency, api_name
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

            return {
                "message": "Transferencia exitosa",
                "original_amount": amount,
                "converted_amount": converted_amount,
                "exchange_rate": exchange_rate,
                "api": api_name
            }

        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()
    
    def get_user_transactions(self, user_id: int):
        self.db = SessionLocal()
        try:
            # Busca todas las transacciones donde el sender_account pertenece al user_id
            transactions = self.db.query(Transaction).join(
                Account, Transaction.sender_account_id == Account.id
            ).filter(
                Account.user_id == user_id
            ).order_by(Transaction.timestamp.desc()).all()
            
            return transactions
        except Exception as e:
            raise ValueError(f"Error al obtener transacciones: {str(e)}")
        finally:
            self.db.close()
    
    def deposit(self, account_id: int, amount: Decimal):
        session = SessionLocal()
        try:
            account = session.query(Account).filter(Account.id == account_id).one()
            account.balance = Decimal(account.balance) + amount
            session.commit()
            return {
                "account_id": account.id,
                "new_balance": float(account.balance),
                "message": f"Se depositó {amount} a la cuenta {account.id}"
            }
        except NoResultFound:
            session.rollback()
            raise Exception(f"No se encontró la cuenta con ID {account_id}")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()