from fastapi_users.authentication import JWTStrategy
#TODO: Change to RS256
SECRET = "SECRET" #Move to security place

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
	
#TODO: lifetime_seconds must be moved to security place