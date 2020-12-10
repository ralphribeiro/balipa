from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.crud import (
    get_item,
    get_items,
    create_item,
    delete_item,
    edit_item
)
from app.db.schemas import ItemCreate, Item

items_router = r = APIRouter()


@r.get("/items", response_model=list[Item], response_model_exclude_none=True)
async def items_list(db: Session = Depends(get_db)):
    """
    Get all items
    """
    return get_items(db=db)


@r.get("/items/{item_id}", response_model=Item,
       response_model_exclude_none=True)
async def item_details(item_id: int, db: Session = Depends(get_db)):
    """
    Get any item details
    """
    item = get_item(db=db, item_id=item_id)
    return item


@r.post("/items", response_model=Item, response_model_exclude_none=True)
async def item_create(item_in: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item
    """
    return create_item(db=db, item=item_in)


@r.put("/items/{item_id}", response_model=Item,
       response_model_exclude_none=True)
async def item_edit(item_id: int, item_in: ItemCreate,
                    db: Session = Depends(get_db)):
    """
    Update existing item
    """
    return edit_item(db=db, item_id=item_id, item=item_in)


@r.delete("/items/{item_id}", response_model=Item,
          response_model_exclude_none=True)
async def item_delete(item_id: int, db: Session = Depends(get_db)):
    """
    Delete existing item
    """
    return delete_item(db=db, item_id=item_id)
