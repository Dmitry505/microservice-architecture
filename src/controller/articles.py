from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from sqlalchemy import select
from uuid import UUID

from controller.users import get_current_user_db
from models.articles import Articles
from service.db import get_session
from models.users import Users
from schemas.articles import (
    ResponseArticles,
    ResponseArticle,
    CreateArticle,
    UpdateArticle,
)


async def get_posts(
    db: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 10
) -> ResponseArticles:
    result = await db.execute(
        select(Articles)
        .order_by(Articles.dt_created.desc())
        .offset(skip)
        .limit(limit)
    )
    articles = result.scalars().all()

    count_result = await db.execute(select(Articles))
    total = len(count_result.scalars().all())
    
    return ResponseArticles(articles=articles, total=total)

async def create_post(
    article: CreateArticle,
    current_user: Users = Depends(get_current_user_db),
    db: AsyncSession = Depends(get_session)
) -> ResponseArticle:
    """Создать новую статью"""
    db_article = Articles(
        title=article.title,
        body=article.body,
        description=article.description,
        user_id=current_user.id,
        tag_list=article.tag_list,
    )
    
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)
    return db_article

async def get_post(
    article_id: UUID,
    db: AsyncSession = Depends(get_session)
) -> ResponseArticle:
    result = await db.execute(
        select(Articles).filter(Articles.id == article_id)
    )
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(
            status_code=404,
            detail="Статья не найдена"
        )
    
    return article

async def update_post(
    article_id: UUID,
    article_update: UpdateArticle,
    current_user: Users = Depends(get_current_user_db),
    db: AsyncSession = Depends(get_session)
) -> ResponseArticle:
    result = await db.execute(
        select(Articles).filter(Articles.id == article_id)
    )
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(
            status_code=404,
            detail="Статья не найдена"
        )
    
    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="У вас нет прав для редактирования этой статьи"
        )
    
    update_data = article_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(article, field, value)
    
    await db.commit()
    await db.refresh(article)
    return article

async def delete_post(
    article_id: UUID,
    current_user: Users = Depends(get_current_user_db),
    db: AsyncSession = Depends(get_session)
) -> None:
    result = await db.execute(
        select(Articles).filter(Articles.id == article_id)
    )
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(
            status_code=404,
            detail="Статья не найдена"
        )

    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="У вас нет прав для удаления этой статьи"
        )
    
    await db.delete(article)
    await db.commit()