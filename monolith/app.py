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

@app.route("/get_role_data", methods=["GET"])
def get_role_data():
    try:
        role_data = Role.query.all()
        role_list = []
        for role in role_data:
            role_list.append({
                "Role_Name": role.Role_Name,
                "Role_Desc": role.Role_Desc,
            })
        app.logger.info(role_list)
        return jsonify(role_list)
    except Exception as e:
        return jsonify({"error": str(e)})

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
    Role_Skill_ID = db.Column(db.String(255), primary_key=True)
    Role_Name = db.Column(db.String(255), db.ForeignKey('Role.Role_Name'))
    Skill_Name = db.Column(db.String(255), db.ForeignKey('Skill.Skill_Name'))

@app.route("/get_roleskill_data", methods=["GET"])
def get_roleSkill_data():
    try:
        roleSkill_data = Role_Skill.query.all()
        roleSkill_list = []
        for roleSkill in roleSkill_data:
            roleSkill_list.append({
                "Role_Skill_ID": roleSkill.Role_Skill_ID,
                "Role_Name": roleSkill.Role_Name,
                "Skill_Name": roleSkill.Skill_Name,
            })
        app.logger.info(roleSkill_list)
        return jsonify(roleSkill_list)
    except Exception as e:
        return jsonify({"error": str(e)})

# Applications
class Applications(db.Model):
    __tablename__ = 'Applications'
    Application_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(255))
    Staff_Name = db.Column(db.String(255))
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
                "Staff_Name": application.Staff_Name,
                "Current_Dept": application.Current_Dept,
                "Skills_Match_Percentage": application.Skills_Match_Percentage,
            })
        app.logger.info(applications_list)
        return jsonify(applications_list)
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
    
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for the SPM monolith...")
    app.run(host="127.0.0.1", port=8000, debug=True)