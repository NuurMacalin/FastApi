from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Review(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    play_name: str
    reviewer_name: str
    rating: int
    comment: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ReviewsGreate(SQLModel):
    play_name: str
    reviewer_name: str
    rating: int
    comment: str


class ReviewRead(SQLModel):
    play_name: str
    reviewer_name: str
    rating: int
    comment: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class ReviewUpdate(SQLModel):
    rating: int
    comment: str