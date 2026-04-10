from fastapi import HTTPException
from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository


def get_wallet(wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets()
        return {"total_balance": sum([w.amount for w in wallets])}
    
    if not wallets_repository.is_wallet_exist(wallet_name):
        raise HTTPException(status_cade=404, detail=f"Wallet '{wallet_name} not found")

    wallet = wallets_repository.get_wallet_balance_by_name(wallet_name)
    return {"wallet": wallet_name, "balance": wallet.balance}



def create_wallet(wallet: CreateWalletRequest):
    if wallets_repository.is_wallet_exist(wallet.name):
      raise HTTPException(
          status_code=400,
          detail=f"wallet {wallet.name} already exist"
      )

    wallet = wallets_repository.create_wallet(wallet.name, wallet.initial_balance)

    return {
        "message": f"Wallet {wallet.name} crated",
        "wallet": wallet.name,
        "new_balance":wallet.balance,
    }