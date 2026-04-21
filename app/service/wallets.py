from fastapi import HTTPException
from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository
from sqlalchemy.orm import Session
from app.models import User

def get_wallet(db: Session, current_user: User, wallet_name: str | None = None  ):
    print(current_user, wallet_name)
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        return {"total_balance": sum([w.balance for w in wallets])}

    if not wallets_repository.is_wallet_exist(db,wallet_name, current_user.id):
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name} not found")

    wallet = wallets_repository.get_wallet_balance_by_name(db,wallet_name, current_user.id)
    return {"wallet": wallet_name, "balance": wallet.balance}
  



def create_wallet(db:Session, wallet: CreateWalletRequest, current_user:User):
   
    if wallets_repository.is_wallet_exist(db, wallet.name, current_user.id):
      raise HTTPException(
          status_code=400,
          detail=f"wallet {wallet.name} already exist"
      )

    wallet = wallets_repository.create_wallet(db,current_user.id,  wallet.name, wallet.initial_balance, )
    db.commit()
    return {
        "message": f"Wallet {wallet.name} crated",
        "wallet": wallet.name,
        "new_balance":wallet.balance,
    }

  