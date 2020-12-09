from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models
from app.db.crud import (
    get_local,
    get_locals,
    create_local,
    edit_local,
    delete_local
)
from app.db.schemas import LocalCreate, LocalBase, Local

locals_router = r = APIRouter()


@r.get("/locals", response_model=list[Local], response_model_exclude_none=True)
async def locals_list(db: Session = Depends(get_db)):
    """
    Get all locals
    """
    return get_locals(db=db)


@r.get("/locals/{local_id}", response_model=Local,
       response_model_exclude_none=True)
async def local_details(local_id: int, db: Session = Depends(get_db)):
    """
    Get any local details
    """
    local = get_local(db=db, local_id=local_id)
    return local


@r.post("/locals", response_model=Local, response_model_exclude_none=True)
async def local_create(local_in: LocalCreate, db: Session = Depends(get_db)):
    """
    Create a new local
    """
    return create_local(db=db, local=local_in)


@r.put("/locals/{local_id}", response_model=Local,
       response_model_exclude_none=True)
async def local_edit(local_id: int, local_in: LocalCreate,
                     db: Session = Depends(get_db)):
    """
    Update existing local
    """
    return edit_local(db=db, local_id=local_id, local=local_in)


@r.delete("/locals/{local_id}", response_model=Local,
          response_model_exclude_none=True)
async def local_delete(local_id: int, db: Session = Depends(get_db)):
    """
    Delete existing local
    """
    return delete_local(db=db, local_id=local_id)
