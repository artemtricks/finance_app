

from app.database import SessionLocal
from app.models import Wallet


def is_wallet_exist(wallet_name: str) -> bool:
    db = SessionLocal()
    try: 
        return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None
    finally: 
        db.close()
      


def add_income(wallet_name:str, amount: float) -> Wallet:
    db = SessionLocal()
    try: 
        wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
        wallet.balance += amount 
        db.commit()
        return wallet
    finally: 
        db.close()
   
   
   

def add_expense(wallet_name:str, amount: float) -> Wallet:
    db = SessionLocal()
    try: 
        wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
        wallet.balance -= amount 
        db.commit()
        return wallet
    finally: 
        db.close()


def get_wallet_balance_by_name(wallet_name: str) -> Wallet:
    db = SessionLocal()
    try: 
        return db.query(Wallet).filter(Wallet.name == wallet_name).first() 
    finally: 
        db.close()


def get_all_wallets() -> list[Wallet]:
    db = SessionLocal()
    try: 
        return db.query(Wallet).all() 
    finally: 
        db.close()

def create_wallet(wallet_name:str , initial_balance: float) -> Wallet:
    db = SessionLocal()
    try: 
     wallet = Wallet(name= wallet_name, balance=initial_balance)
     db.add(wallet)
     db.commit()
     db.refresh(wallet)
    finally: 
        db.close()