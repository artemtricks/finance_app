from decimal import Decimal
from app.models import User, Wallet

def test_add_expense_success(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    response = client.post("api/v1/operations/expense", json={
        'wallet_name': 'card',
        'amount': 50.0,
        'descriptions': 'Food',
    }, headers={
        "Authorization": f"Bearer {user.login}"
    })


    assert response.status_code == 200
    assert response.json()['message'] == "Expense added"
    assert response.json()['wallet'] == wallet.name
    assert Decimal(str(response.json()['amount'])) == Decimal(50)
    assert response.json()['descriptions'] == "Food"
    assert Decimal(str(response.json()['new_balance'])) == Decimal(150)
    


def test_add_expense_negative_amount(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    response = client.post("api/v1/operations/expense", json={
        'wallet_name': 'card',
        'amount': -50.0,
        'descriptions': 'Food',
    }, headers={
        "Authorization": f"Bearer {user.login}"
    })

    assert response.status_code == 422


def test_add_expense_empty_name(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    response = client.post("api/v1/operations/expense", json={
        'amount': 50.0,
        'descriptions': 'Food',
    }, headers={
        "Authorization": f"Bearer {user.login}"
    })

    assert response.status_code == 422


def test_add_expense_negative_amount(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    response = client.post("api/v1/operations/expense", json={
        'wallet_name': 'card',
        'amount': -50.0,
        'descriptions': 'Food',
    }, headers={
        "Authorization": f"Bearer {user.login}"
    })

    assert response.status_code == 422


def test_add_expense_wallet_not_exist(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.commit()
    
    response = client.post("api/v1/operations/expense", json={
        'wallet_name': 'cash',
        'amount': 50.0,
        'descriptions': 'Food',
    }, headers={
        "Authorization": f"Bearer {user.login}"
    })

    assert response.status_code == 404



def test_add_expense_unautorize(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.commit()
    
    response = client.post("api/v1/operations/expense", json={
        'wallet_name': 'cash',
        'amount': 50.0,
        'descriptions': 'Food',
    }, headers={
        "Authorization": f"Bearer notexist"
    })

    assert response.status_code == 401


def test_add_expense_not_enoght_money(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    response = client.post("api/v1/operations/expense", json={
        'wallet_name': 'card',
        'amount': 250.0,
        'descriptions': 'Food',
    }, headers={
        "Authorization": f"Bearer {user.login}"
    })

    assert response.status_code == 400
