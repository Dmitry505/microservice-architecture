from fastapi import APIRouter

from typing import Any

from controller.users import create_user, get_current_user_db, login_user, update_user
from schemas.users import ResponseToken, ResponseUser



router = APIRouter(prefix="/user", tags=["user"])

router.get("/", response_model=ResponseUser)(get_current_user_db)
router.post("/", response_model=ResponseUser)(create_user)
router.post("/login", response_model=ResponseToken)(login_user)
router.put("/", response_model=ResponseUser)(update_user)

