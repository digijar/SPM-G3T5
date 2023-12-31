import os
import pytest
from app import app, db, Role, Staff, Skill, Role_Skill, Applications, StaffSkill
from flask_sqlalchemy import SQLAlchemy
from flask import json
from datetime import datetime

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
# def test_create_new_job_listing():
#     role_data = {
#         "roleName": "testjaronrole12345",
#         "roleDesc": "test create new job",
#         "dept": "HR",
#         "location": "On-Site",  # Provide a valid location
#         "deadline": datetime.strptime("2023-12-31", "%Y-%m-%d")  # Convert the string to a date
#     }
#     response = client.post('/create_new_job_listing', data=json.dumps(role_data), content_type='application/json')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data["message"] == "Job listing created successfully"

# test 6 /create_new_job_listing
def test_create_new_job_listing_():
    role_name = "testbrandnewrolename"

    role_data = {
        "roleName": role_name,
        "roleDesc": "sample",
        "dept": "HR",
        "location": "Remote",
        "deadline": "2023-11-16",
        "skills": "Account Management"
    }

    # Make a POST request to create the job listing
    response = client.post('/create_new_job_listing', json=role_data)

    # Check that the response is successful
    assert response.status_code == 200

    with app.app_context():
        new_role = Role.query.filter_by(Role_Name=role_data["roleName"]).first()
        if new_role:
            db.session.delete(new_role)
            db.session.commit()


# test 7 /update_role/<role_name>
# def test_update_role():
#     role_name = "Account Manager"  # Provide a valid role name
#     role_data = {
#         "Role_Desc": "test update account manager",
#         "Location": "Remote",
#         "Dept": "Sales",
#         "Deadline": "2024-01-15"
#     }
#     response = client.put(f'/update_role/{role_name}', data=json.dumps(role_data), content_type='application/json')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data["message"] == "Role updated successfully"

# test 7 /update_role/<role_name>
def test_update_role():
    role_name = "Finance Director"

    # Define the updated data
    updated_data = {
        "Role_Desc": "Sample updated description",
        "Location": "On-site",
        "Dept": "Finance",
        "Deadline": "2024-01-01",
        "Skills": ["Financial Planning", "Financial Reporting"]
    }

    with app.app_context():
        # Retrieve the current data for the role name
        role = Role.query.get(role_name)
        skill = Role_Skill.query.filter_by(Role_Name=role_name).first()

        # Save the original data
        original_data = {
            "Role_Desc": role.Role_Desc,
            "Location": role.Location,
            "Dept": role.Dept,
            "Deadline": str(role.Deadline),
            "Skills": skill.Skill_Name
        }

        # Make a PUT request to update the role with the new data
        response = client.put(f'/update_role/{role_name}', json=updated_data)
        
        # Check that the response is successful
        assert response.status_code == 200

        # Make another PUT request to revert to the original data
        response_revert = client.put(f'/update_role/{role_name}', json=original_data)

        # Check that the reversion response is also successful
        assert response_revert.status_code == 200

        db.session.commit()

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
    response = client.get('/get_roleskill_data_by_name/Developer')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# test 11 /new_role_skill
# def test_new_role_skill():
#     role_name = "Account Manager"  # Provide a valid role name
#     skill_name = "Account Management"  # Provide a valid skill name
#     role_data = {"roleName": role_name, "skillName": skill_name}
#     response = client.post('/new_role_skill', data=json.dumps(role_data), content_type='application/json')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data["message"] == "Role_Skill updated successfully"

# test 11 /new_role_skill
def test_new_role_skill():
    role_name = "testjaronrole12345"
    skill_name = "Account Management"

    role_skill_data = {
        "roleName": role_name,
        "skillName": skill_name
    }

    # Make a POST request to create the Role-Skill relationship
    response = client.post('/new_role_skill', json=role_skill_data)

    # Check that the response is successful
    assert response.status_code == 200

    # Delete the Role-Skill relationship immediately after creation
    with app.app_context():
        role_skill = Role_Skill.query.filter_by(Role_Name=role_name, Skill_Name=skill_name).first()
        if role_skill is not None:
            db.session.delete(role_skill)
            db.session.commit()

# test 12 /update_roleskill/<role_name>
# def test_update_roleskill():
#     role_name = "Account Manager"  # Provide a valid role name
#     role_skill_data = {"Skill_Name": "Applications Development"}  # Provide a valid skill name
#     response = client.put(f'/update_roleskill/{role_name}', data=json.dumps(role_skill_data), content_type='application/json')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data["message"] == "Role_Skill updated successfully"

# test 13 /delete_roleskill/<string:role_name>
# def test_delete_role_skill():
#     role_name = "Account Manager"  # Provide a valid role name
#     response = client.delete(f'/delete_roleskill/{role_name}')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert f'Successfully deleted Role_Skill entries for {role_name}' in data["message"]

# test 13 /delete_roleskill/<string:role_name>
def test_delete_roleskill():
    role_name = "testjaronrole12345"

    # Check if the Role-Skill relationship exists
    with app.app_context():
        role_skill = Role_Skill.query.filter_by(Role_Name=role_name).first()

    response_delete = client.delete(f'/delete_roleskill/{role_name}')

    
    assert response_delete.status_code == 200

    role_skill_data = {
        "roleName": role_name,
        "skillName": role_skill.Skill_Name
    }

    response_post = client.post('/new_role_skill', json=role_skill_data)

    # Check that the response for re-creation is successful
    assert response_post.status_code == 200

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

    # Delete any existing application with the same role_name and staff_id
    response_delete = client.delete(f"/delete_application?role_name={application_data['role_name']}&staff_id={application_data['staff_id']}")
    assert response_delete.status_code in [200, 404]  # It's okay if the application didn't exist

    # Ccreate a new application
    response = client.post('/create_new_application', data=json.dumps(application_data), content_type='application/json')
    # print(response.get_json())  # Print the server response
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
    role_name = "Sales Manager"
    staff_id = 140004

    response = client.get(f"/get_skill_match/{role_name}/{staff_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert "Match_Percentage" in data
    assert data["Role_Name"] == role_name
    assert data["Staff_ID"] == staff_id

    # Assert the match percentage value within a certain tolerance due to floating-point precision
    expected_match_percentage = 9.090909090909092
    assert abs(data["Match_Percentage"] - expected_match_percentage) < 0.00001

# test 19 /get_missing_skills/<role_name>/<int:staff_id>
def test_get_missing_skills():
    role_name = "Account Manager"  # Provide a valid role name
    staff_id = 210044  # Provide a valid staff_id
    response = client.get(f'/get_missing_skills/{role_name}/{staff_id}')
    assert response.status_code == 200
    data = response.get_json()

# test 20: Applications for the same role with the same staff ID will not be accepted
def test_same_role_same_staff():
    role_name = "testrolename0"
    staff_id = 21044

    # Check if an application has already been submitted
    response1 = client.get(f"/check_application?role_name={role_name}&staff_id={staff_id}")
    assert response1.status_code == 200
    data1 = response1.get_json()

    # If an application has been submitted, the system should not accept a second application
    if data1["application_exists"]:
        response2 = client.post(f"/create_new_application/{role_name}/{staff_id}")
        assert response2.status_code == 400  # Assuming 400 is the status code for a bad request
        assert "Applications for the same role with the same staff ID will not be accepted" in response2.get_json()["message"]

# test 21: Check if the given staff_id is not exactly 6 digits that the application is rejected
def test_invalid_staff_id():
    role_name = "testrolename0"
    invalid_staff_ids = [0, 12345, 1234567, 'ABCDEF', 'ABC', 'ABCDEFG']  # This list contains staff_id values that does not exist

    for staff_id in invalid_staff_ids:
        # Try to submit an application with an invalid staff_id
        response = client.post("/create_new_application", json={"role_name": role_name, "staff_id": staff_id})
        assert response.status_code == 400  # Assuming 400 is the status code for a bad request

# test 22: Create new role with invalid/missing data 
def test_create_new_job_listing_missing():
    role_data = {
        "dept": "HR",
        "location": "On-Site",
        "deadline": "2023-12-31"
    }
    response = client.post('/create_new_job_listing', data=json.dumps(role_data), content_type='application/json')
    assert response.status_code == 500 

# test 23: Create new job listing with an existing role name
def test_same_role_name():
    role_name = "Finance Director"

    response = client.post("/create_new_job_listing", json={
            "roleName": role_name,
        })
    assert response.status_code == 500

# test 24: Update role with invalid/missing data
def test_update_role_missing():
    role_name = "Finance Director"
    role_data = {
        "Dept": "Finance",
        "Location": "Remote",
        "Deadline": "2023-12-31"
    }

    response = client.put(f'/update_role/{role_name}', data=json.dumps(role_data), content_type='application/json')
    assert response.status_code == 500

if __name__ == '__main__':
    pytest.main()