# all imports
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from os import environ
import requests
from flask_sqlalchemy import SQLAlchemy
import logging

# for API Keys
from dotenv import load_dotenv
load_dotenv('spm.env')
user = os.getenv('user')
password = os.getenv('password')

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@spm-database.cfr5k6rgnsdu.ap-southeast-2.rds.amazonaws.com:3306/SPM_fiesta'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://admin:98CsBUaGxbkqn6elAgdD@spm-database.cfr5k6rgnsdu.ap-southeast-2.rds.amazonaws.com:3306/SPM_fiesta'
db = SQLAlchemy(app)
CORS(app)

# Staff
class Staff(db.Model):
    __tablename__ = 'Staff'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(255))
    Staff_LName = db.Column(db.String(255))
    Dept = db.Column(db.String(255))
    Country = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Role = db.Column(db.String(255))

@app.route("/get_staff_data", methods=["GET"])
def get_staff_data():
    try:
        staff_data = Staff.query.all()
        staff_list = []
        for staff in staff_data:
            staff_list.append({
                "Staff_ID": staff.Staff_ID,
                "Staff_FName": staff.Staff_FName,
                "Staff_LName": staff.Staff_LName,
                "Dept": staff.Dept,
                "Country": staff.Country,
                "Email": staff.Email,
                "Role": staff.Role,
            })
        app.logger.info(staff_list)
        return jsonify(staff_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/get_staff_data_by_id/<int:staff_id>", methods=["GET"])
def get_staff_data_by_id(staff_id):
    try:
        staff = Staff.query.get(staff_id)
        if staff:
            return jsonify({
                "Staff_ID": staff.Staff_ID,
                "Staff_FName": staff.Staff_FName,
                "Staff_LName": staff.Staff_LName,
                "Dept": staff.Dept,
                "Country": staff.Country,
                "Email": staff.Email,
                "Role": staff.Role,
            })
        else:
            return jsonify({"error": "Staff not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/edit_staff_data", methods=["PUT"])
def edit_staff_data():
    try:
        staff_data = request.json  # Assuming the updated staff data is sent in the request body as JSON
        staff_id = staff_data.get("Staff_ID")

        # Find the staff record to update by Staff_ID
        staff = Staff.query.get(staff_id)
        if staff:
            # Update staff record with the new data
            staff.Staff_FName = staff_data.get("Staff_FName")
            staff.Staff_LName = staff_data.get("Staff_LName")
            staff.Dept = staff_data.get("Dept")
            staff.Country = staff_data.get("Country")
            staff.Email = staff_data.get("Email")
            staff.Role = staff_data.get("Role")

            db.session.commit()
            return jsonify({"message": "Staff data updated successfully"})
        else:
            return jsonify({"error": "Staff not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Role
class Role(db.Model):
    __tablename__ = 'Role'
    Role_Name = db.Column(db.String(255), primary_key=True)
    Role_Desc = db.Column(db.String(255))
    Dept      = db.Column(db.String(255))
    Location  = db.Column(db.Enum('Remote', 'On-Site'))
    Deadline  = db.Column(db.Date)

def check_role_exists(role_name):
    role = Role.query.filter_by(Role_Name=role_name).first()
    return role is not None

@app.route('/check_role_exists', methods=['GET'])
def check_role_exists_route():
    role_name = request.args.get('roleName')
    
    exists = check_role_exists(role_name)
    
    return jsonify({'exists': exists})

@app.route("/get_role_data", methods=["GET"])
def get_role_data():
    try:
        role_data = Role.query.all()
        role_list = []
        for role in role_data:
            role_list.append({
                "Role_Name":    role.Role_Name,
                "Role_Desc":    role.Role_Desc,
                "Dept":         role.Dept,
                "Location":     role.Location,
                "Deadline":     role.Deadline,
            })
        app.logger.info(role_list)
        return jsonify(role_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/create_new_job_listing', methods=['POST'])
def create_new_job_listing():
    try:
        data = request.json

        # Extract data from the request
        role_name = data['roleName']
        role_desc = data['roleDesc']
        department = data['dept']
        location = data['location']
        deadline = data['deadline']
        skills = data['skills']

        existing_role = Role.query.filter_by(Role_Name=role_name).first()
        if existing_role:
            return jsonify({"error": "Role name already exists"}), 500
        
        if not (role_name and role_desc and department and location and deadline and skills):
            return jsonify({"error": "One or more fields are blank"}), 500

        # Create a new Role object and add it to the database
        new_role = Role(
            Role_Name=role_name,
            Role_Desc=role_desc,
            Dept=department,
            Location=location,
            Deadline=deadline
        )
        db.session.add(new_role)
        db.session.commit()

        return jsonify({"message": "Job listing created successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/update_role/<role_name>', methods=['PUT'])
def update_role(role_name):
    data = request.json
    role = Role.query.get(role_name)
    if not role:
        return jsonify({'message': 'Role not found'}), 404
    
    # Check if any data field is blank
    if 'Role_Desc' in data and data['Role_Desc']:
        role.Role_Desc = data['Role_Desc']
    else:
        return jsonify({'message': 'Role description cannot be blank'}), 500

    if 'Location' in data and data['Location']:
        role.Location = data['Location']
    else:
        return jsonify({'message': 'Location cannot be blank'}), 500

    if 'Dept' in data and data['Dept']:
        role.Dept = data['Dept']
    else:
        return jsonify({'message': 'Department cannot be blank'}), 500

    if 'Deadline' in data and data['Deadline']:
        role.Deadline = data['Deadline']
    else:
        return jsonify({'message': 'Deadline cannot be blank'}), 500
    
    if 'Skills' in data and (isinstance(data['Skills'], list) or (isinstance(data['Skills'], str) and data['Skills'])):
        role.Skills = data['Skills']
    else:
        return jsonify({'message': 'Skills cannot be blank or empty list'}), 500
    
    db.session.commit()
    return jsonify({'message': 'Role updated successfully'}), 200

# Skill
class Skill(db.Model):
    __tablename__ = 'Skill'
    Skill_Name = db.Column(db.String(255), primary_key=True)
    Skill_Desc = db.Column(db.String(255))

@app.route("/get_skill_data", methods=["GET"])
def get_skill_data():
    try:
        skill_data = Skill.query.all()
        skill_list = []
        for skill in skill_data:
            skill_list.append({
                "Skill_Name": skill.Skill_Name,
                "Skill_Desc": skill.Skill_Desc,
            })
        app.logger.info(skill_list)
        return jsonify(skill_list)
    except Exception as e:
        return jsonify({"error": str(e)})

# Role_Skill
class Role_Skill(db.Model):
    __tablename__ = 'Role_Skill'
    # Role_Skill_ID = db.Column(db.String(255), primary_key=True)
    Role_Name = db.Column(db.String(255), db.ForeignKey('Role.Role_Name'), primary_key=True)
    Skill_Name = db.Column(db.String(255), db.ForeignKey('Skill.Skill_Name'), primary_key=True)

@app.route("/get_roleskill_data", methods=["GET"])
def get_roleSkill_data():
    try:
        # roleSkill_data = Role_Skill.query.all()
        roleSkill_data = Role_Skill.query.with_entities(
            Role_Skill.Role_Name,
            Role_Skill.Skill_Name
            ).all()
        roleSkill_list = []
        for roleSkill in roleSkill_data:
            roleSkill_list.append({
                # "Role_Skill_ID": roleSkill.Role_Skill_ID,
                "Role_Name": roleSkill.Role_Name,
                "Skill_Name": roleSkill.Skill_Name,
            })
        app.logger.info(roleSkill_list)
        return jsonify(roleSkill_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/get_roleskill_data_by_name/<role_name>", methods=["GET"])
def get_roleSkill_data_by_name(role_name):
    try:
        app.logger.info(f"Fetching skills for role: {role_name}")

        roleSkill_data = Role_Skill.query.with_entities(
            Role_Skill.Role_Name,
            Role_Skill.Skill_Name
        ).filter_by(Role_Name=role_name).all()

        if not roleSkill_data:
            app.logger.warning(f"No skills found for role: {role_name}")

        roleSkill_list = []

        for roleSkill in roleSkill_data:
            roleSkill_list.append({
                "Role_Name": roleSkill.Role_Name,
                "Skill_Name": roleSkill.Skill_Name,
            })

        app.logger.info(f"Skills for role {role_name}: {roleSkill_list}")
        return jsonify(roleSkill_list), 200
    except Exception as e:
        app.logger.error(f"Error fetching skills for role {role_name}: {str(e)}")
        return jsonify({"error": str(e)}), 404

@app.route('/new_role_skill', methods=['POST'])
def new_role_skill():
    try:
        data = request.json

        role_name = data['roleName']
        skill_name = data['skillName']

        role = Role.query.filter_by(Role_Name=role_name).first()
        if role is None:
            return jsonify({"error": "Role not found"}), 404

        skill = Skill.query.filter_by(Skill_Name=skill_name).first()
        if skill is None:
            return jsonify({"error": "Skill not found"}), 404

        new_role_skill = Role_Skill(
            Role_Name=role.Role_Name,
            Skill_Name=skill.Skill_Name
        )
        db.session.add(new_role_skill)
        db.session.commit()

        return jsonify({"message": "Role_Skill updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_roleskill/<role_name>', methods=['PUT'])
def update_roleskill(role_name):
    data = request.json
    role_skill = Role_Skill.query.filter_by(Role_Name=role_name).first()
    if not role_skill:
        return jsonify({'message': 'Role_Skill not found'}), 404
    
    # Update the skill associated with the role
    role_skill.Skill_Name = data['Skill_Name']
    
    db.session.commit()
    return jsonify({'message': 'Role_Skill updated successfully'}), 200

@app.route('/delete_roleskill/<string:role_name>', methods=['DELETE'])
def delete_role_skill(role_name):
    try:
        # Find the Role_Skill entries related to the given role_name
        role_skill_entries = Role_Skill.query.filter_by(Role_Name=role_name).all()

        # Delete each related Role_Skill entry
        for entry in role_skill_entries:
            db.session.delete(entry)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': f'Successfully deleted Role_Skill entries for {role_name}'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Applications
class Applications(db.Model):
    __tablename__ = 'Applications'
    Application_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role_Name = db.Column(db.String(255))
    Staff_ID = db.Column(db.Integer)
    Current_Dept = db.Column(db.String(255))
    Skills_Match_Percentage = db.Column(db.Numeric(5, 2))
    
# Get Applications
@app.route("/get_applications_data", methods=["GET"])
def get_applications_data():
    try:
        applications_data = Applications.query.all()
        applications_list = []
        for application in applications_data:
            applications_list.append({
                "Application_ID": application.Application_ID,
                "Role_Name": application.Role_Name,
                "Staff_ID": application.Staff_ID,
                "Current_Dept": application.Current_Dept,
                "Skills_Match_Percentage": application.Skills_Match_Percentage,
            })
        app.logger.info(applications_list)
        return jsonify(applications_list)
    except Exception as e:
        return jsonify({"error": str(e)})

def staff_exists(staff_id):
    return Staff.query.get(staff_id) is not None

@app.route("/create_new_application", methods=["POST"])
def create_new_application():
    try:
        # Get the data from the POST request
        data = request.json
        role_name = data.get("role_name")
        staff_id = data.get("staff_id")
        current_dept = data.get('current_dept')
        skill_match = data.get('skill_match')
        
        # Check if staff_id exists
        if not staff_exists(staff_id):
            return jsonify({"error": "Invalid staff_id. No such staff exists."}), 400

        # Check if an application with the given role_name and staff_id already exists
        existing_application = Applications.query.filter_by(Role_Name=role_name, Staff_ID=staff_id).first()
        if existing_application:
            return jsonify({"error": "An application with the same role_name and staff_id already exists"}), 400

        # Create a new entry in the Application table
        new_application = Applications(Role_Name=role_name, Staff_ID=staff_id, Current_Dept=current_dept, Skills_Match_Percentage=skill_match)
        db.session.add(new_application)
        db.session.commit()

        return jsonify({"message": "Application created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/delete_application", methods=["DELETE"])
def delete_application():
    try:
        # Get the role_name and staff_id from the request parameters
        role_name = request.args.get("role_name")
        staff_id = request.args.get("staff_id")

        # Query the Applications table to find an application with the given role_name and staff_id
        application = Applications.query.filter_by(Role_Name=role_name, Staff_ID=staff_id).first()

        # If an application is found, delete it from the database
        if application:
            db.session.delete(application)
            db.session.commit()
            # print(f"Deleted application with role_name {role_name} and staff_id {staff_id}")
            return jsonify({"message": "Application deleted successfully"})
        # If no application is found, return a JSON response indicating that no application exists
        else:
            # print(f"No application found with role_name {role_name} and staff_id {staff_id}")
            return jsonify({"error": "No application found with the given role_name and staff_id"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/check_application", methods=["GET"])
def check_application():
    try:
        # Get the role_name and staff_id from the request parameters
        role_name = request.args.get("role_name")
        staff_id = request.args.get("staff_id")

        # Query the Applications table to find an application with the given role_name and staff_id
        application = Applications.query.filter_by(Role_Name=role_name, Staff_ID=staff_id).first()

        # If an application is found, return a JSON response indicating that an application exists
        if application:
            return jsonify({"application_exists": True})
        # If no application is found, return a JSON response indicating that no application exists
        else:
            return jsonify({"application_exists": False})

    except Exception as e:
        return jsonify({"error": str(e)})

# Staff Skills
class StaffSkill(db.Model):
    __tablename__ = 'Staff_Skill'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Skill_Name = db.Column(db.String(20), primary_key=True)

# Get Staff Skills
@app.route('/get_staff_skill', methods=['GET'])
def get_staff_skill():
    try:
        staff_skills = StaffSkill.query.all()
        result = []
        for skill in staff_skills:
            result.append({
                'Staff_ID': skill.Staff_ID, 
                'Skill_Name': skill.Skill_Name
            })
        app.logger.info(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Get particular staff's skills 
@app.route("/get_staff_skill_by_id/<int:staff_id>", methods=['GET'])
def get_staff_skill_by_id(staff_id):
    try:
        staff_skills = StaffSkill.query.filter_by(Staff_ID=staff_id).all()
        result = []
        for skill in staff_skills:
            result.append({
                'Staff_ID': skill.Staff_ID, 
                'Skill_Name': skill.Skill_Name
            })
        app.logger.info(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route("/get_skill_match/<role_name>/<int:staff_id>", methods=['GET'])
def get_skill_match(role_name, staff_id):
    try:
        # Get the skills of the role
        role_skills = Role_Skill.query.with_entities(
            Role_Skill.Skill_Name
        ).filter_by(Role_Name=role_name).all()

        role_skill_set = set([skill.Skill_Name for skill in role_skills])

        # Get the skills of the applicant
        staff_skills = StaffSkill.query.filter_by(Staff_ID=staff_id).all()
        staff_skill_set = set([skill.Skill_Name for skill in staff_skills])

        # Calculate the percentage match
        app.logger.info(role_skill_set)
        app.logger.info(staff_skill_set)

        if len(role_skill_set) == 0:
            match_percentage = 0  # Set the match percentage to 0% if there are no skills for the role.
        else:
            common_skills = role_skill_set.intersection(staff_skill_set)
            match_percentage = (len(common_skills) / len(role_skill_set)) * 100
        
        # common_skills = role_skill_set.intersection(staff_skill_set)
        # match_percentage = (len(common_skills) / len(role_skill_set)) * 100

        result = {
            'Role_Name': role_name,
            'Staff_ID': staff_id,
            'Match_Percentage': match_percentage
        }

        app.logger.info(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_missing_skills/<role_name>/<int:staff_id>", methods=['GET'])
def get_missing_skills(role_name, staff_id):
    try:
        # Get the skills of the role
        role_skills = Role_Skill.query.with_entities(
            Role_Skill.Skill_Name
        ).filter_by(Role_Name=role_name).all()

        role_skill_set = set([skill.Skill_Name for skill in role_skills])

        # Get the skills of the applicant
        staff_skills = StaffSkill.query.filter_by(Staff_ID=staff_id).all()
        staff_skill_set = set([skill.Skill_Name for skill in staff_skills])

        # Calculate the percentage match
        app.logger.info(role_skill_set)
        app.logger.info(staff_skill_set)

        # Calculate the missing skills
        missing_skills = role_skill_set - staff_skill_set
        common_skills = role_skill_set.intersection(staff_skill_set)

        result = {
            'Missing_Skills': list(missing_skills),
            'Common_Skills': list(common_skills),
        }

        app.logger.info(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

    
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for the SPM monolith...")
    app.run(host="127.0.0.1", port=8000, debug=True)