from fastapi import HTTPException
from app.repository import wallets as wallets_repository
from app.schemas import OperationRequest




def add_income(operation: OperationRequest):
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
       raise HTTPException(
           status_code=404,
           detail=f"Wallet {operation.wallet_name} not found"
       )
   
    wallet = wallets_repository.add_income(operation.wallet_name, operation.amount)

    return {
       'message': 'Income added',
       'wallet': operation.wallet_name,
       'amount': operation.amount,
       'description': operation.descriptions,
       'new_balance': wallet.balance
   }




def add_expense(operation: OperationRequest):
 
   if not wallets_repository.is_wallet_exist(operation.wallet_name):
       raise HTTPException(
           status_code=404,
           detail=f"Wallet {operation.wallet_name} not found"
       )
   if operation.amount <= 0:
       raise HTTPException(
           status_code=400,
           detail=f"Amount must be positive"
       )
   
   wallet = wallets_repository.get_wallet_balance_by_name(operation.wallet_name)

   if wallet.balance < operation.amount:
       raise HTTPException(
           status_code=400,
           detail=f"Insufficient founds. Available: {wallet.balance}"
       )
   
   wallet = wallets_repository.add_expense(operation.wallet_name, operation.amount)

   return {
       {
       'message': 'Expense added',
       'wallet': operation.wallet_name,
       'amount': operation.amount,
       'description': operation.descriptions,
       'new_balance': wallet.balance
   }
   }