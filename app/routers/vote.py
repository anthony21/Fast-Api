from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from charset_normalizer import models
from sqlalchemy.orm import Session
from os import sync
from .. import schemas, database, oauth, models

router = APIRouter(
    prefix = "/vote", 
    tags =['Vote']
)

@router.post('/', status_code=status.HTTP_200_OK)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: { vote.post_id} doest not exist")

    vote_query = db.query(models.Vote).filter(
                          models.Vote.post_id == vote.post_id,
                          models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                                detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "successfully added vote"}
    else:
        if not found_vote: 
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vote doesnt exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "successfully deleted vote"}
    