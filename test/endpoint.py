import pytest
from front.database import db
from front import create_app
from front.models import User

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Using SQLite for simplicity

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()  # Set up test database
        yield test_client
        with app.app_context():
            db.drop_all()  # Tear down test database

def test_add_user(test_client):
    response = test_client.post('/user', json={"email": "test@example.com", "password": "testpass", "first_name": "Test"})
    assert response.status_code == 200
    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None

def test_delete_user(test_client):
    user = User(email="delete@example.com", password="testpass", first_name="Delete")
    db.session.add(user)
    db.session.commit()
    response = test_client.delete(f'/user/{user.id}')
    assert response.status_code == 200
    deleted_user = User.query.get(user.id)
    assert deleted_user is None

def test_add_lol_username(test_client):
    user = User(email="loluser@example.com", password="testpass", first_name="LOLUser")
    db.session.add(user)
    db.session.commit()
    response = test_client.post(f'/user/{user.id}/lol-username', json={"lol_username": "Summoner123"})
    assert response.status_code == 200
    updated_user = User.query.get(user.id)
    assert updated_user.lol_username == "Summoner123"

def test_update_lol_username(test_client):
    user = User(email="updateuser@example.com", password="testpass", first_name="UpdateUser", lol_username="OldSummoner")
    db.session.add(user)
    db.session.commit()
    response = test_client.put(f'/user/{user.id}/lol-username', json={"lol_username": "NewSummoner"})
    assert response.status_code == 200
    updated_user = User.query.get(user.id)
    assert updated_user.lol_username == "NewSummoner"
