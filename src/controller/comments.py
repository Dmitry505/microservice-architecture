from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from sqlalchemy import select

from controller.users import get_current_user_db
from models.articles import Articles
from models.comments import Comments
from models.users import Users
from service.db import get_session
from schemas.comments import CreateComment, ResponseComment, ResponseComments


async def get_comments(
    article_id: UUID,
    db: AsyncSession = Depends(get_session)
) -> ResponseComments:
    result = await db.execute(
        select(Comments).filter(Comments.articles_id == article_id).order_by(Comments.dt_created.desc())
    )
    comments = result.scalars().all()
    return ResponseComments(comments=comments)

async def create_comment(
    article_id: UUID,
    comment: CreateComment,
    current_user: Users = Depends(get_current_user_db),
    db: AsyncSession = Depends(get_session)
) -> ResponseComment:
    article_result = await db.execute(select(Articles).filter(Articles.id == article_id))
    article = article_result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    
    db_comment = Comments(
        articles_id=article_id,
        user_id=current_user.id,
        body=comment.body
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(
    article_id: UUID,
    comment_id: UUID,
    current_user: Users = Depends(get_current_user_db),
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Comments)
        .filter(Comments.id == comment_id, Comments.articles_id == article_id)
    )
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление")
    
    await db.delete(comment)
    await db.commit()