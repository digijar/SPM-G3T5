import os
import pytest
from app import app, db, Role, Staff, Skill, Role_Skill, Applications, StaffSkill
from flask_sqlalchemy import SQLAlchemy
from flask import json

# testing mode
app.config['TESTING'] = True

client = app.test_client()

# test 1 /get_staff_data
def test_get_staff_data():
    response = client.get('/get_staff_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 2 /get_staff_data_by_id/<int:staff_id>
def test_get_staff_data_by_id():
    response = client.get('/get_staff_data_by_id/210044')  # valid staff_id here
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)

# test 3 /edit_staff_data
def test_edit_staff_data():
    staff_data = {
        "Staff_ID": 130001,  # Provide a valid Staff_ID for the test
        "Staff_FName": "Jaron",
        "Staff_LName": "Chan",
        "Dept": "HR",
        "Country": "Singapore",
        "Email": "jaronchan123@gmail.com",
        "Role": 1
    }
    response = client.put('/edit_staff_data', data=json.dumps(staff_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Staff data updated successfully"

# test 4 /check_role_exists
def test_check_role_exists():
    response = client.get('/check_role_exists?roleName=Developer')  # Provide a valid role name
    assert response.status_code == 200
    data = response.get_json()
    assert "exists" in data

# test 5 /get_role_data
def test_get_role_data():
    response = client.get('/get_role_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 6 /create_new_job_listing
def test_create_new_job_listing():
    role_data = {
        "roleName": "testrolename12345",
        "roleDesc": "test create new job",
        "dept": "HR",
        "location": "On-Site",  # Provide a valid location
        "deadline": "2023-12-31"  # Provide a valid date
    }
    response = client.post('/create_new_job_listing', data=json.dumps(role_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Job listing created successfully"

# test 7 /update_role/<role_name>
def test_update_role():
    role_name = "Account Manager"  # Provide a valid role name
    role_data = {
        "Role_Desc": "test update account manager",
        "Location": "Remote",
        "Dept": "Sales",
        "Deadline": "2024-01-15"
    }
    response = client.put(f'/update_role/{role_name}', data=json.dumps(role_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Role updated successfully"

# test 8 /get_skill_data
def test_get_skill_data():
    response = client.get('/get_skill_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 9 /get_roleskill_data
def test_get_roleSkill_data():
    response = client.get('/get_roleskill_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 10 /get_roleskill_data_by_name/<role_name>
def test_get_roleSkill_data_by_name():
    response = client.get('/get_roleSkill_data_by_name/Developer')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 11 /new_role_skill
def test_new_role_skill():
    role_name = "Account Manager"  # Provide a valid role name
    skill_name = "Account Management"  # Provide a valid skill name
    role_data = {"roleName": role_name, "skillName": skill_name}
    response = client.post('/new_role_skill', data=json.dumps(role_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Role_Skill updated successfully"

# test 12 /update_roleskill/<role_name>
def test_update_roleskill():
    role_name = "Account Manager"  # Provide a valid role name
    role_skill_data = {"Skill_Name": "Applications Development"}  # Provide a valid skill name
    response = client.put(f'/update_roleskill/{role_name}', data=json.dumps(role_skill_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Role_Skill updated successfully"

# test 13 /delete_roleskill/<string:role_name>
def test_delete_role_skill():
    role_name = "Account Manager"  # Provide a valid role name
    response = client.delete(f'/delete_roleskill/{role_name}')
    assert response.status_code == 200
    data = response.get_json()
    assert f'Successfully deleted Role_Skill entries for {role_name}' in data["message"]

# test 14 /get_applications_data
def test_get_applications_data():
    response = client.get('/get_applications_data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 15 /create_new_application
def test_create_new_application():
    application_data = {
        "role_name": "Account Manager",  # Provide a valid role name
        "staff_id": 210044,  # Provide a valid staff_id
        "current_dept": "IT",  # Provide a valid department name
        "skill_match": 85.0  # Provide a valid skill match percentage
    }
    response = client.post('/create_new_application', data=json.dumps(application_data), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Application created successfully"

# test 16 /get_staff_skill
def test_get_staff_skill():
    response = client.get('/get_staff_skill')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 17 /get_staff_skill_by_id/<int:staff_id>
def test_get_staff_skill_by_id():
    staff_id = 210044  # Provide a valid staff_id
    response = client.get(f'/get_staff_skill_by_id/{staff_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 18 /get_skill_match/<role_name>/<int:staff_id>
def test_get_skill_match():
    role_name = "Account Manager"  # Provide a valid role name
    staff_id = 210044  # Provide a valid staff_id
    response = client.get(f'/get_skill_match/{role_name}/{staff_id}')
    assert response.status_code == 200
    data = response.get_json()

# test 19 /get_missing_skills/<role_name>/<int:staff_id>
def test_get_missing_skills():
    role_name = "Account Manager"  # Provide a valid role name
    staff_id = 210044  # Provide a valid staff_id
    response = client.get(f'/get_missing_skills/{role_name}/{staff_id}')
    assert response.status_code == 200
    data = response.get_json()

if __name__ == '__main__':
    pytest.main()