from datetime import datetime

from fastapi import HTTPException
from app.repository import wallets as wallets_repository
from app.repository import operations as operations_repository
from app.schemas import OperationRequest, OperationResponse
from sqlalchemy.orm import Session
from app.models import User



def add_income(*, db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:
   
    if not wallets_repository.is_wallet_exist(db, operation.wallet_name, current_user.id):
       raise HTTPException(
           status_code=404,
           detail=f"Wallet {operation.wallet_name} not found"
       )
   
    wallet = wallets_repository.add_income(db, operation.wallet_name, current_user.id, operation.amount)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type='income',
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.descriptions,
        subcategory=operation.descriptions
    )
    db.commit()
    return OperationResponse.model_validate(operation)
  



def add_expense(*, db: Session, current_user: User,operation: OperationRequest) -> OperationResponse:
 
    if not wallets_repository.is_wallet_exist(db, operation.wallet_name, current_user.id):
       raise HTTPException(
           status_code=404,
           detail=f"Wallet {operation.wallet_name} not found"
       )
    if operation.amount <= 0:
       raise HTTPException(
           status_code=400,
           detail=f"Amount must be positive"
       )
   
    wallet = wallets_repository.get_wallet_balance_by_name(db, operation.wallet_name, current_user.id)

    if wallet.balance < operation.amount:
            raise HTTPException(
            status_code=400,
            detail=f"Insufficient founds. Available: {wallet.balance}"
        )
   
    wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type='expense',
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.descriptions,
        subcategory=operation.descriptions
    )
    db.commit()
    return OperationResponse.model_validate(operation)
   


def get_operations_list(*, db: Session, current_user: User, wallet_id: int | None = None, date_from: datetime | None = None, date_to: datetime | None = None) -> list[OperationResponse]:
    if wallet_id:
        wallet = wallets_repository.get_wallet_by_id(db=db, wallet_id=wallet_id, user_id=current_user.id)
        if not wallet:
          raise HTTPException(
           status_code=404,
           detail=f"Wallet {wallet_id} not found"
       )  
        
        wallets_ids = [wallet.id]
    else:
        wallets = wallets_repository.get_all_wallets(db=db, user_id=current_user.id)
        wallets_ids = [w.id for w in wallets]

    operations = operations_repository.get_operations_list(db=db, wallet_ids=wallets_ids, date_from=date_from, date_to=date_to)
    result = []
    for operation in operations:
        result.append(OperationResponse.model_validate(operation))
    return result
    

