import os
import pytest
from app import app, db, Role, Staff, Skill, Role_Skill, Applications, StaffSkill
from flask_sqlalchemy import SQLAlchemy

# testing mode
app.config['TESTING'] = True

client = app.test_client()

def test_get_staff_data():
    response = client.get('/get_staff_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_get_role_data():
    response = client.get('/get_role_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# add more here

if __name__ == '__main__':
    pytest.main()