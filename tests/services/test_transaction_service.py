import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from src.services.transaction_service import TransactionService
from src.database.models import Account, Transaction


@patch("src.services.transaction_service.ExchangeService")
@patch("src.services.transaction_service.SessionLocal")
def test_transfer_same_currency_success(mock_session_local, mock_exchange_service):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    sender = Account(id=1, balance=Decimal("100.0"), currency="USD")
    receiver = Account(id=2, balance=Decimal("50.0"), currency="USD")

    # Simular consultas
    mock_db.query.return_value.filter_by.side_effect = [
        MagicMock(one=lambda: sender),
        MagicMock(one=lambda: receiver)
    ]

    service = TransactionService()
    result = service.transfer(1, 2, Decimal("20.0"))

    assert result["message"] == "Transferencia exitosa"
    assert result["converted_amount"] == 20.0
    assert result["exchange_rate"] == 1.0
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


@patch("src.services.transaction_service.ExchangeService")
@patch("src.services.transaction_service.SessionLocal")
def test_transfer_different_currency_success(mock_session_local, mock_exchange_service):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    sender = Account(id=1, balance=Decimal("200.0"), currency="USD")
    receiver = Account(id=2, balance=Decimal("100.0"), currency="PEN")

    mock_db.query.return_value.filter_by.side_effect = [
        MagicMock(one=lambda: sender),
        MagicMock(one=lambda: receiver)
    ]

    mock_exchange = MagicMock()
    mock_exchange.convert_currency.return_value = Decimal("74.0")  # Por ejemplo: 20 USD → 74 PEN
    mock_exchange_service.return_value = mock_exchange

    service = TransactionService()
    result = service.transfer(1, 2, Decimal("20.0"))

    assert result["message"] == "Transferencia exitosa"
    assert result["converted_amount"] == 74.0
    assert float(result["exchange_rate"]) == 3.7
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()


@patch("src.services.transaction_service.ExchangeService")
@patch("src.services.transaction_service.SessionLocal")
def test_transfer_insufficient_balance(mock_session_local, mock_exchange_service):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    sender = Account(id=1, balance=Decimal("10.0"), currency="USD")
    receiver = Account(id=2, balance=Decimal("50.0"), currency="USD")

    mock_db.query.return_value.filter_by.side_effect = [
        MagicMock(one=lambda: sender),
        MagicMock(one=lambda: receiver)
    ]

    service = TransactionService()

    with pytest.raises(ValueError) as excinfo:
        service.transfer(1, 2, Decimal("20.0"))

    assert "Saldo insuficiente" in str(excinfo.value)
    mock_db.rollback.assert_called_once()
    mock_db.close.assert_called_once()


@patch("src.services.transaction_service.SessionLocal")
def test_get_user_transactions_success(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_transaction = MagicMock()
    mock_db.query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_transaction]

    service = TransactionService()
    result = service.get_user_transactions(123)

    assert result == [mock_transaction]
    mock_db.close.assert_called_once()


@patch("src.services.transaction_service.SessionLocal")
def test_get_user_transactions_exception(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    # Simular error en la consulta
    mock_db.query.side_effect = Exception("DB error")

    service = TransactionService()

    with pytest.raises(ValueError) as excinfo:
        service.get_user_transactions(123)

    assert "Error al obtener transacciones" in str(excinfo.value)
    mock_db.close.assert_called_once()
