
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import func

from database import connect_db
from models import Review, ReviewRead, ReviewsGreate, ReviewUpdate

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


# 1. CREATE REVIEW
@router.post(
    "/",
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED
)
def create_review(
    review: ReviewsGreate,
    session: Session = Depends(connect_db)
):
    db_review = Review.model_validate(review)

    session.add(db_review)
    session.commit()
    session.refresh(db_review)

    return db_review


# 2. GET ALL REVIEWS
@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    play_name: str | None = Query(
        default=None,
        description="Filter by play name"
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(connect_db)
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)

    query = (
        query
        .order_by(Review.id)
        .offset(skip)
        .limit(limit)
    )

    reviews = session.exec(query).all()

    return reviews


# 3. AVERAGE RATING BY PLAY NAME
@router.get("/average/{play_name}")
def get_average_rating(
    play_name: str,
    session: Session = Depends(connect_db)
):
    query = (
        select(
            func.avg(Review.rating),
            func.count(Review.id)
        )
        .where(Review.play_name == play_name)
    )

    result = session.exec(query).one()

    average_rating, total_reviews = result

    if total_reviews == 0:
        raise HTTPException(
            status_code=404,
            detail="No reviews found for this play"
        )

    return {
        "play_name": play_name,
        "average_rating": round(float(average_rating), 2),
        "total_reviews": total_reviews
    }


# 4. GET REVIEW BY ID
@router.get("/{review_id}", response_model=ReviewRead)
def get_review(
    review_id: int,
    session: Session = Depends(connect_db)
):
    review = session.get(Review, review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review


# 5. UPDATE REVIEW - PATCH
@router.patch("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    update: ReviewUpdate,
    session: Session = Depends(connect_db)
):
    review = session.get(Review, review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"{key} cannot be null"
            )
        setattr(review, key, value)

    session.commit()
    session.refresh(review)

    return review


# 6. REPLACE REVIEW - PUT
@router.put("/{review_id}", response_model=ReviewRead)
def replace_review(
    review_id: int,
    update: ReviewsGreate,
    session: Session = Depends(connect_db)
):
    review = session.get(Review, review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    update_data = update.model_dump()

    for key, value in update_data.items():
        setattr(review, key, value)

    session.commit()
    session.refresh(review)

    return review


# 7. DELETE REVIEW
@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    session: Session = Depends(connect_db)
):
    review = session.get(Review, review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    session.delete(review)
    session.commit()

    return {"message": "Review deleted successfully"}
