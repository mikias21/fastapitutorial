from fastapi import status, HTTPException, Depends, APIRouter 
from app.database import engine, get_db 
from sqlalchemy.orm import Session
from app import models
from .. import schemas, models, oauth2

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user[0].id)
    vote_found = vote_query.first()

    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Post already liked by this user')

        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user[0].id) 
        db.add(new_vote)
        db.commit()   
        return {"message": "post liked"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "post unliked"}
