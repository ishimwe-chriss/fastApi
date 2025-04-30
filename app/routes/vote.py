from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schema, oauth2, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votes: schema.Vote, db: Session = Depends(database.get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == votes.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Does Not Exist!!")

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == votes.post_id,
        models.Votes.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if votes.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {votes.post_id}")
        new_vote = models.Votes(post_id=votes.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Successfully deleted vote"}
