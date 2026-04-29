from src.routing.books import router as books_router
from src.routing.authors import router as authors_router
from src.routing.libraries import router as libraries_router
from src.routing.visitors import router as visitors_router
from src.routing.bl import router as bl_router
from src.routing.arrears import router as arrears_router
from src.routing.users import router as users_router
from src.routing.auth import router as auth_router

routers = [books_router, authors_router, libraries_router, visitors_router, bl_router, arrears_router, users_router, auth_router]