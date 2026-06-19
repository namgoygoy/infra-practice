from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import cache, crud, schemas
from app.database import get_db

router = APIRouter(prefix="/memos", tags=["memos"])


def _serialize_memo(memo) -> dict:
    return schemas.MemoResponse.model_validate(memo).model_dump(mode="json")


def _serialize_memos(memos) -> list[dict]:
    return [_serialize_memo(memo) for memo in memos]


@router.get("", response_model=list[schemas.MemoResponse])
def list_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip == 0:
        cached = cache.get_recent_memos(limit)
        if cached is not None:
            return cached

    memos = crud.get_memos(db, skip=skip, limit=limit)
    if skip == 0:
        cache.set_recent_memos(limit, _serialize_memos(memos))
    return memos


@router.get("/{memo_id}", response_model=schemas.MemoResponse)
def read_memo(memo_id: int, db: Session = Depends(get_db)):
    cached = cache.get_memo(memo_id)
    if cached is not None:
        return cached

    memo = crud.get_memo(db, memo_id)
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found"
        )

    serialized = _serialize_memo(memo)
    cache.set_memo(serialized)
    return memo


@router.post("", response_model=schemas.MemoResponse, status_code=status.HTTP_201_CREATED)
def create_memo(memo: schemas.MemoCreate, db: Session = Depends(get_db)):
    created = crud.create_memo(db, memo)
    cache.invalidate_recent_lists()
    cache.set_memo(_serialize_memo(created))
    return created


@router.put("/{memo_id}", response_model=schemas.MemoResponse)
def update_memo(
    memo_id: int, memo: schemas.MemoUpdate, db: Session = Depends(get_db)
):
    updated = crud.update_memo(db, memo_id, memo)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found"
        )

    cache.invalidate_memo(memo_id)
    cache.set_memo(_serialize_memo(updated))
    return updated


@router.delete("/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_memo(db, memo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found"
        )

    cache.invalidate_memo(memo_id)
