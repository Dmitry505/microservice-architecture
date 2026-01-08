from pydantic import BaseModel, ConfigDict, Field, UUID4

from models.articles import ArticlesTags

class BaseArticle(BaseModel):
    title: str = Field(
        description="Заголовок статьи (до 40 символов)",
        max_length=40,
        min_length=3,
        example="Мой первый пост"
    )
    description: str = Field(
        description="Опсиание",
        example="Опсиание статьи"
    )
    body: str = Field(
        description="Содержание",
        example="Содержание статьи"
    )
    tag_list: list[ArticlesTags] | None = Field(
        default=None,
        description="Тэги",
        example=[ArticlesTags.BACKEND, ArticlesTags.FRONTEND]
    )

class ResponseArticle(BaseArticle):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4 = Field(
        description="Уникальный ID статьи",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    user_id: UUID4 = Field(
        description="Уникальный ID пользователя",
        example="550e8400-e29b-41d4-a716-446655440000"
    )

class ResponseArticles(BaseModel):
    articles: list[ResponseArticle] = Field(
        description="Список статей, [ResponseArticle]"
    )
    total: int = Field(
        description="кол-во статей",
    )

class CreateArticle(BaseArticle):
    pass

class UpdateArticle(BaseArticle):
    pass