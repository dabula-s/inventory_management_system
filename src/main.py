from fastapi import Depends
from fastapi import FastAPI

from api.inventory.category.endpoints import router as category_router
from api.inventory.item.endpoints import router as item_router
from api.users.auth import auth_backend, current_active_user, fastapi_users
from api.users.schemas import UserRead, UserCreate, UserUpdate
from db.postgresql import User

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


app.include_router(item_router)
app.include_router(category_router)
