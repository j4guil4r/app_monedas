import pytest
from unittest.mock import MagicMock, patch
from src.services.user_service import UserService
from src.database.models import User


@patch("src.services.user_service.SessionLocal")
def test_create_user_success(mock_session_local):
    # Preparar mocks
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    # Simulamos que el usuario ya tiene un id al hacer refresh
    def fake_refresh(user):
        user.id = 1

    mock_db.refresh.side_effect = fake_refresh

    # Instanciar el servicio y llamar al método
    service = UserService()
    result = service.create_user("Juan")

    # Verificar
    assert isinstance(result, User)
    assert result.name == "Juan"
    assert result.id == 1

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    mock_db.close.assert_called_once()


@patch("src.services.user_service.SessionLocal")
def test_create_user_exception(mock_session_local):
    # Preparar mocks
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    # Simular error en .add()
    mock_db.add.side_effect = Exception("DB error")

    # Instanciar servicio
    service = UserService()

    with pytest.raises(ValueError) as excinfo:
        service.create_user("Pedro")

    assert "Error al crear usuario" in str(excinfo.value)
    mock_db.rollback.assert_called_once()
    mock_db.close.assert_called_once()
