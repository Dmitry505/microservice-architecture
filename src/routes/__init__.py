from . import articles
from . import user
from . import comments

from fastapi import APIRouter

router = APIRouter()
router.include_router(articles.router)
router.include_router(user.router)
router.include_router(comments.router)