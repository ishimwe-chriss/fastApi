from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, oauth2
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# -----------------CREATE POST---------------#
@router.post("/new-posts", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    #
    # new_post = cursor.fetchone()
    # conn.commit()


# ----------------ALL POSTS----------------------------
@router.get("/", response_model=List[schema.PostVote])
def get_all_posts(db: Session = Depends(get_db),
                  current_user: models.User = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = ((db.query(models.Post, func.count(models.Votes.post_id).label("votes")).
                join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)).
               group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())

    return results

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)


# ......Get One Post........#
@router.get("/{post_id}", response_model=schema.PostVote)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = ((db.query(models.Post, func.count(models.Votes.post_id).label("votes")).
             join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)).
            group_by(models.Post.id).filter(models.Post.id == post_id).first())

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")

    return post

    # cursor.execute("""SELECT * FROM posts WHERE id = %s  """, (str(post_id)))
    # post = cursor.fetchone()


# ......DELETE........#

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform this action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id)))
    # post = cursor.fetchone()
    # conn.commit()


# ......UPDATE........#
@router.put("/{post_id}", response_model=schema.PostResponse)
def update_post(post_id: int, post: schema.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    posts = post_query.first()

    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")

    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform this action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(post_id)))
    #
    # posts = cursor.fetchone()
    # conn.commit()
