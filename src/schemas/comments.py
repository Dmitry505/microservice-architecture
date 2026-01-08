from pydantic import BaseModel, ConfigDict, Field, UUID4


class BaseComment(BaseModel):
    body: str = Field(
        description="Тело комментария",
        example="Комментарий"
    )

class ResponseComment(BaseComment):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4 = Field(
        description="Уникальный ID комментария",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    user_id: UUID4 = Field(
        description="Уникальный ID пользователя",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    articles_id: UUID4 = Field(
        description="Уникальный ID статьи",
        example="550e8400-e29b-41d4-a716-446655440000"
    )

class ResponseComments(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    comments: list[ResponseComment] = Field(
        description="Список rjvvtynfhbtd, [Responsecomment]"
    )

class CreateComment(BaseComment):
    pass