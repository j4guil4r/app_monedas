from decimal import Decimal
from ..database.session import SessionLocal
from ..database.models import Account

class AccountService:
    def __init__(self):
        self.db = SessionLocal()

    ## obviemos la insersión de dinero xd
    def create_account(self, user_id: int, currency: str, balance: float = 0.0):
        try:
            account = Account(
                user_id=user_id,
                currency=currency.upper(),
                balance=Decimal(str(balance))
            )
            self.db.add(account)
            self.db.commit()
            return account
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al crear cuenta: {str(e)}")
        finally:
            self.db.close()