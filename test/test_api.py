import pytest
from app import create_app
from back.database import db
from back.models import User

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
        yield test_client
        with app.app_context():
            db.drop_all()

# Parametrized test for adding and updating lol_username
@pytest.mark.parametrize(
    "email,first_name,lol_username,new_lol_username",
    [
        ("test1@example.com", "Test1", "Summoner123", "NewSummoner1"),
        ("test2@example.com", "Test2", "Summoner456", "NewSummoner2"),
    ]
)
def test_lol_username_operations(test_client, email, first_name, lol_username, new_lol_username):
    # Add user
    response = test_client.post('/api/user', json={"email": email, "password": "testpass", "first_name": first_name})
    assert response.status_code == 201
    user = User.query.filter_by(email=email).first()
    assert user is not None
    
    # Add lol_username
    response = test_client.post(f'/api/user/{user.id}/lol-username', json={"lol_username": lol_username})
    assert response.status_code == 200
    updated_user = db.session.get(User, user.id)
    assert updated_user.lol_username == lol_username

    # Update lol_username
    response = test_client.put(f'/api/user/{user.id}/lol-username', json={"lol_username": new_lol_username})
    assert response.status_code == 200
    updated_user = db.session.get(User, user.id)
    assert updated_user.lol_username == new_lol_username
