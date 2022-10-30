from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import List
from .. import models, schemas, oauth
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth.get_current_user),
              limit: int = 10, skip: int =0,
              search: Optional[str] = ""):


    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall(
    # print(posts)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
     
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id  == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return results

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s; """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with {id} not found")

    return  post

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute("""INSERT INTO posts ( title, content, published) VALUES(%s,%s,%s) Returning *;""",
    #               (post.title, post.content,post.published))
    # new_post = cursor.fetchone()
    
    #conn.commit()
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *;""",(str(id)) )
    # delete_post = cursor.fetchone()

    # conn.commit()
    
    post_query  = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} doesnt exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post_query: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title= %s, content =%s, published=%s WHERE id = %s RETURNING * ; """, 
    #               (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()

    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post = updated_post.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} doesnt exist")
    
    if post.owner_id != current_user.id:
        HTTPException(status = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")

    updated_post.update(post_query.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()
