from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models 
from app.database import engine, get_db 
from sqlalchemy.orm import Session
from app import models, oauth2
from app.schemas import CreatePost, PostResponse, PostOut
from typing import List, Optional
from .. import oauth2 
from sqlalchemy import func 

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# @router.get('/', response_model=List[PostOut])
@router.get('/')
def get_posts(db: Session = Depends(get_db), current_user: tuple = Depends(oauth2.get_current_user), 
                limit: int=10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("num_of_likes")).join(models.Vote, 
            models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(
                limit).offset(skip).all()
    return posts

# @router.get('/{id}', response_model=PostResponse)
@router.get('/{id}')
def get_post(id: int, db: Session=Depends(get_db), current_user: tuple = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).where(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("num_of_likes")).join(models.Vote, 
            models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"content with an id {id} not found")
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: CreatePost, db: Session=Depends(get_db), current_user: tuple = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s ) RETURNING * """, 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user[-1].id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: tuple = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with an id {id} not found")
    if post.owner_id != current_user[-1].id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='You can only delete your post')

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session=Depends(get_db), current_user: tuple = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with an id {id} not found")
    
    if post.owner_id != current_user[-1].id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='You can only update your post')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()