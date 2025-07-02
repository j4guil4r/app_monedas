import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from src.services.account_service import AccountService
from src.database.models import Account


@patch("src.services.account_service.SessionLocal")
def test_create_account_success(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_account = Account(id=1, user_id=1, currency="USD", balance=Decimal("100.0"))
    mock_db.add.side_effect = lambda obj: setattr(obj, "id", 1)  # simula autoincrement
    mock_db.commit.return_value = None

    service = AccountService()
    result = service.create_account(user_id=1, currency="usd", balance=100.0)

    assert isinstance(result, Account)
    assert result.currency == "USD"
    assert result.balance == Decimal("100.0")
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


@patch("src.services.account_service.SessionLocal")
def test_create_account_exception(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_db.add.side_effect = Exception("DB error")

    service = AccountService()

    with pytest.raises(ValueError) as excinfo:
        service.create_account(user_id=1, currency="usd", balance=100.0)

    assert "Error al crear cuenta" in str(excinfo.value)
    mock_db.rollback.assert_called_once()
    mock_db.close.assert_called_once()


@patch("src.services.account_service.SessionLocal")
def test_get_user_accounts_success(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_account = MagicMock()
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_account]

    service = AccountService()
    result = service.get_user_accounts(1)

    assert result == [mock_account]
    mock_db.query.assert_called_once()
    mock_db.close.assert_not_called()  # no se cierra en este método


@patch("src.services.account_service.SessionLocal")
def test_get_user_accounts_exception(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    mock_db.query.side_effect = Exception("DB error")

    service = AccountService()

    with pytest.raises(ValueError) as excinfo:
        service.get_user_accounts(1)

    assert "Error al obtener cuentas" in str(excinfo.value)
