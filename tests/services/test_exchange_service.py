import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from src.services.exchange_service import ExchangeService


@patch("src.services.exchange_service.APISingleton")
def test_get_exchange_rate(mock_api_singleton):
    # Simular el adaptador que retorna una tasa
    mock_adapter = MagicMock()
    mock_adapter.get_exchange_rate.return_value = 3.75

    # Simular singleton y su adaptador
    instance = MagicMock()
    instance.get_adapter.return_value = mock_adapter
    mock_api_singleton.return_value = instance

    service = ExchangeService()
    rate = service.get_exchange_rate("USD", "PEN", api_name="FakeAPI")

    assert isinstance(rate, Decimal)
    assert rate == Decimal("3.75")
    instance.set_adapter.assert_called_once_with("FakeAPI")
    instance.get_adapter.assert_called_once()


@patch("src.services.exchange_service.APISingleton")
def test_convert_currency(mock_api_singleton):
    # Simular adaptador que retorna una tasa
    mock_adapter = MagicMock()
    mock_adapter.get_exchange_rate.return_value = 3.5

    # Simular singleton
    instance = MagicMock()
    instance.get_adapter.return_value = mock_adapter
    mock_api_singleton.return_value = instance

    service = ExchangeService()
    result = service.convert_currency(10.0, "USD", "PEN", api_name="FakeAPI")

    assert isinstance(result, Decimal)
    assert result == Decimal("35.0")
    instance.set_adapter.assert_called_once_with("FakeAPI")
