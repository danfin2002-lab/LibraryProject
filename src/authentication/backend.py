from src.authentication.transport import bearer_transport
from src.authentication.strategy import get_jwt_strategy
from fastapi_users.authentication import AuthenticationBackend

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)