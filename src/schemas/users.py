from pydantic import BaseModel, ConfigDict, Field, UUID4

class BaseUser(BaseModel):
    username: str = Field(
        description="Имя пользователя (до 40 символов)",
        max_length=40,
        example="Имя"
    )
    email: str = Field(
        description="Email (до 40 символов)",
        max_length=40,
        example="test@mail.ru"
    )
    bio: str | None = Field(
        default=None,
        description="bio (до 100 символов)",
        max_length=100,
        example="test bio"
    )
    image_url: str | None = Field(
        default=None,
        description="image_url (до 100 символов)",
        max_length=100,
        example="https://www.google.com/url?sa=i&url"
    )


class ResponseUser(BaseUser):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4 = Field(
        description="Уникальный ID пользователя",
        example="550e8400-e29b-41d4-a716-446655440000"
    )

class UserLogin(BaseModel):
    email: str = Field(
        description="Email (до 40 символов)",
        max_length=40,
        example="test@mail.ru"
    )
    password: str = Field(
        description="password (до 20 символов)",
        max_length=40,
        min_length=8,
        example="12345password"
    )

class CreateUser(BaseUser):
    password: str = Field(
        description="password (до 20 символов)",
        max_length=40,
        min_length=8,
        example="12345password"
    )

class UpdateUser(CreateUser):
    pass

class ResponseToken(BaseModel):
    access_token: str = Field(
        description="access_token",
    )
    token_type: str = Field(
        description="token_type",
    )
