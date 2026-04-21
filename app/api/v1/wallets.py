from fastapi import APIRouter, Depends
from app.service import wallets as wallets_service
from app.schemas import CreateWalletRequest
from sqlalchemy.orm import Session
from app.dependency import  get_db
from app.models import User
from app.api.v1.users import get_current_user

router = APIRouter()

@router.get("/balance")
def get_balance( wallet_name: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),):
    return wallets_service.get_wallet(db=db, current_user=current_user, wallet_name=wallet_name)
    


@router.post("/wallets")
def create_wallet(wallet: CreateWalletRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db) ):
    return wallets_service.create_wallet(db=db, wallet=wallet, current_user=current_user)
   

