from fastapi import APIRouter

from controller.articles import (
    get_posts, 
    create_post, 
    get_post, 
    update_post, 
    delete_post
)
from schemas.articles import (
    ResponseArticles,
    ResponseArticle,
)


router = APIRouter(prefix="/articles", tags=["articles"])

router.get("/",response_model=ResponseArticles)(get_posts)
router.post("/", status_code=201, response_model=ResponseArticle)(create_post)
router.get("/{article_id}", response_model=ResponseArticle)(get_post)
router.put("/{article_id}", response_model=ResponseArticle)(update_post)
router.delete("/{article_id}", status_code=204)(delete_post)