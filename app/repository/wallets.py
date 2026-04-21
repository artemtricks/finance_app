from decimal import Decimal

from app.models import Wallet
from sqlalchemy.orm import Session


def is_wallet_exist(db: Session,  wallet_name: str, user_id: int,) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet_name,Wallet.user_id == user_id).first() is not None
   


def add_income(db: Session, wallet_name:str, user_id: int, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balance += amount 
    
    return wallet
   
   

def add_expense(db: Session, user_id: int,wallet_name:str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name,  Wallet.user_id == user_id).first()
    wallet.balance -= amount 
    
    return wallet
   


def get_wallet_balance_by_name(db: Session, wallet_name: str, user_id: int ) -> Wallet:
    return db.query(Wallet).filter(Wallet.name == wallet_name,  Wallet.user_id == user_id).first() 
   


def get_all_wallets(db: Session, user_id:int) -> list[Wallet]:
    return db.query(Wallet).filter(Wallet.user_id == user_id).all() 
    

def create_wallet(db: Session, user_id: int, wallet_name:str , initial_balance: Decimal) -> Wallet:
    print(user_id, wallet_name, initial_balance)
    wallet = Wallet(name=wallet_name, balance=initial_balance, user_id=user_id)
    db.add(wallet)
    db.flush()
    return wallet
    