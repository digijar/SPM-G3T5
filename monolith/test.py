import os
import pytest
from app import app, db, Role, Staff, Skill, Role_Skill, Applications, StaffSkill
from flask_sqlalchemy import SQLAlchemy
from flask import json

# testing mode
app.config['TESTING'] = True

client = app.test_client()

# test /get_staff_data
def test_get_staff_data():
    response = client.get('/get_staff_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test the "/get_staff_data_by_id/<int:staff_id>" route
def test_get_staff_data_by_id():
    response = client.get('/get_staff_data_by_id/')  # valid staff_id here
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    # Add more assertions based on the expected response JSON structure

# Test the "/edit_staff_data" route
def test_edit_staff_data():
    staff_data = {
        "Staff_ID": 1,  # Provide a valid Staff_ID for the test
        "Staff_FName": "UpdatedFirstName",
        "Staff_LName": "UpdatedLastName",
        "Dept": "UpdatedDept",
        "Country": "UpdatedCountry",
        "Email": "UpdatedEmail",
        "Role": "UpdatedRole"
    }
    response = client.put('/edit_staff_data', data=json.dumps(staff_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Staff data updated successfully"

# Test the "/check_role_exists" route
def test_check_role_exists():
    response = client.get('/check_role_exists?roleName=YourRoleName')  # Provide a valid role name
    assert response.status_code == 200
    data = response.get_json()
    assert "exists" in data

# test /get_role_data
def test_get_role_data():
    response = client.get('/get_role_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test the "/create_new_job_listing" route
def test_create_new_job_listing():
    role_data = {
        "roleName": "NewRoleName",
        "roleDesc": "NewRoleDesc",
        "dept": "NewDept",
        "location": "On-Site",  # Provide a valid location
        "deadline": "2023-12-31"  # Provide a valid date
    }
    response = client.post('/create_new_job_listing', data=json.dumps(role_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Job listing created successfully"

# Test the "/update_role/<role_name>" route
def test_update_role():
    role_name = "YourRoleName"  # Provide a valid role name
    role_data = {
        "Role_Desc": "UpdatedRoleDescription",
        "Location": "Remote",  # Provide a valid location
        "Dept": "UpdatedDept",
        "Deadline": "2024-01-15"  # Provide a valid date
    }
    response = client.put(f'/update_role/{role_name}', data=json.dumps(role_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Role updated successfully"

# add more here

if __name__ == '__main__':
    pytest.main()