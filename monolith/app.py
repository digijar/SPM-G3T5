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
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@spm-database.cfr5k6rgnsdu.ap-southeast-2.rds.amazonaws.com:3306/SPM_fiesta'
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

        return jsonify({"message": "Job listing created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/update_role/<role_name>', methods=['PUT'])
def update_role(role_name):
    data = request.json
    role = Role.query.get(role_name)
    if not role:
        return jsonify({'message': 'Role not found'}), 404
    
    # Update the role details based on the data received
    # role.Role_Name = data['Role_Name'] 
    role.Role_Desc = data['Role_Desc']
    role.Skill_Name = data['Skill_Name']
    role.Location = data['Location']
    role.Dept = data['Dept']
    role.Deadline = data['Deadline']
    
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
        roleSkill_data = Role_Skill.query.with_entities(
            Role_Skill.Role_Name,
            Role_Skill.Skill_Name
        ).filter_by(Role_Name=role_name).all()

        roleSkill_list = []

        for roleSkill in roleSkill_data:
            roleSkill_list.append({
                "Role_Name": roleSkill.Role_Name,
                "Skill_Name": roleSkill.Skill_Name,
            })

        app.logger.info(roleSkill_list)
        return jsonify(roleSkill_list)
    except Exception as e:
        return jsonify({"error": str(e)})

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

        return jsonify({"message": "Role_Skill updated successfully"})
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

@app.route("/create_new_application", methods=["POST"])
def create_new_application():
    try:
        # Get the data from the POST request
        data = request.json
        role_name = data.get("role_name")
        staff_id = data.get("staff_id")
        current_dept = data.get('current_dept')
        skill_match = data.get('skill_match')
        

        # Create a new entry in the Application table
        new_application = Applications(Role_Name=role_name, Staff_ID=staff_id, Current_Dept=current_dept, Skills_Match_Percentage=skill_match)
        db.session.add(new_application)
        db.session.commit()

        return jsonify({"message": "Application created successfully"})
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
        common_skills = role_skill_set.intersection(staff_skill_set)
        match_percentage = (len(common_skills) / len(role_skill_set)) * 100

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