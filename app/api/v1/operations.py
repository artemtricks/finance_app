from datetime import datetime

from fastapi import APIRouter, Depends, Query
from app.service import operations as operations_service
from app.schemas import OperationRequest, OperationResponse
from sqlalchemy.orm import Session
from app.dependency import get_db
from app.models import User
from app.api.v1.users import get_current_user

router = APIRouter()

@router.post("/operations/income", response_model=OperationResponse)
def add_income(operation: OperationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return operations_service.add_income(db=db,current_user=current_user, operation=operation )


@router.post("/operations/expense", response_model=OperationResponse)
def add_expense(operation: OperationRequest, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return operations_service.add_expense(db=db,current_user=current_user, operation=operation )


@router.get("/operations", response_model=list[OperationResponse])
def get_operations_list(
                         db: Session = Depends(get_db),
                         user: User = Depends(get_current_user), 
                         wallet_id: int | None = Query(None), 
                         date_from: datetime | None = Query(None), 
                         date_to: datetime | None = Query(None)
                         ):
    
    return operations_service.get_operations_list(db=db, user=user, wallet_id=wallet_id, date_from=date_from, date_to=date_to)
    