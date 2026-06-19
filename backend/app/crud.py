from sqlalchemy.orm import Session

from app import models, schemas


def get_memos(db: Session, skip: int = 0, limit: int = 100) -> list[models.Memo]:
    return (
        db.query(models.Memo)
        .order_by(models.Memo.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_memo(db: Session, memo_id: int) -> models.Memo | None:
    return db.query(models.Memo).filter(models.Memo.id == memo_id).first()


def create_memo(db: Session, memo: schemas.MemoCreate) -> models.Memo:
    db_memo = models.Memo(title=memo.title, content=memo.content)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo


def update_memo(
    db: Session, memo_id: int, memo: schemas.MemoUpdate
) -> models.Memo | None:
    db_memo = get_memo(db, memo_id)
    if not db_memo:
        return None

    update_data = memo.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_memo, field, value)

    db.commit()
    db.refresh(db_memo)
    return db_memo


def delete_memo(db: Session, memo_id: int) -> bool:
    db_memo = get_memo(db, memo_id)
    if not db_memo:
        return False

    db.delete(db_memo)
    db.commit()
    return True
