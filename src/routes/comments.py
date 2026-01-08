from controller.comments import create_comment, delete_comment, get_comments
from schemas.comments import ResponseComment, ResponseComments

from fastapi import APIRouter


router = APIRouter(prefix="/articles", tags=["comments"])

router.post("/{article_id}/comments", response_model=ResponseComment)(create_comment)
router.get("/{article_id}/comments", response_model=ResponseComments)(get_comments)
router.delete("/{article_id}/comments/{comment_id}", status_code=204)(delete_comment)