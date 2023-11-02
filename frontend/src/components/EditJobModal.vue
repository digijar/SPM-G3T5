<template>
  <div class="modal" v-if="showModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Details</h5>
          <button @click="closeModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="form-floating mb-3">
              <input type="text" class="form-control" id="InputValue_RoleName" v-model="newroleName">
              <label for="InputValue_RoleName">Role Name</label>
            </div>

            <div class="form-floating mb-3">
              <textarea class="form-control" id="InputValue_RoleDesc" v-model="roleDesc"></textarea>
              <label for="InputValue_RoleDesc">Role Description</label>
            </div>

            <div class="form-floating mb-3">
              <select class="form-select custom-select-height" id="InputValue_skillReq" v-model="skillReq" multiple>
                <option value="" disabled>Select</option>
                <option v-for="skill in skills" :key="skill.Skill_Name" :value="skill.Skill_Name">{{ skill.Skill_Name }}</option>
              </select>
              <label for="InputValue_skillReq">Skills Required</label>
            </div>

            <div class="form-check mb-3">
              <label>Location:</label>
              <div class="radio-container">
                <input type="radio" id="remote" class="form-check-input" value="Remote" v-model="location">
                <label for="remote" class="form-check-label">Remote</label>
              </div>
              <div class="radio-container">
                <input type="radio" id="onSite" class="form-check-input" value="On-Site" v-model="location">
                <label for="onSite" class="form-check-label">On-Site</label>
              </div>
            </div>

            <div class="form-floating mb-3">
              <select class="form-select" id="InputValue_Dept" v-model="department">
                <option value="" disabled>Select</option>
                <option v-for="dept in departments" :key="dept" :value="dept">{{ dept }}</option>
              </select>
              <label for="InputValue_Dept">Department</label>
            </div>

            <div class="form-floating mb-3">
              <input type="date" class="form-control" id="InputValue_Deadline" v-model="deadline">
              <label for="InputValue_Deadline">Deadline</label>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button @click="submitForm" type="button" class="btn btn-success" data-bs-dismiss="modal">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    showModal: Boolean,
    roleName: String,
  },

  data() {
    return {
      newroleName: '',
      roleDesc: '',
      skillReq: [], // Store selected skills as an array
      location: '',
      department: '',
      deadline: '',
      skills: [],
      departments: [],
    };
  },

  methods: {
    closeModal() {
      this.$emit('close');
    },

    async fetchRoleSkillData() {
      try {
        const response = await axios.get('http://localhost:8000/get_roleskill_data');
        const roleSkillData = response.data;

        const uniqueSkills = new Set();
        this.skills = roleSkillData.filter((roleSkill) => {
          if (!uniqueSkills.has(roleSkill.Skill_Name)) {
            uniqueSkills.add(roleSkill.Skill_Name);
            return true;
          }
          return false;
        });
      } catch (error) {
        console.error(error);
      }
    },

    fetchDepartments() {
      axios.get('http://localhost:8000/get_role_data')
        .then(response => {
          // Extract and populate department options from the response
          const departmentOptions = response.data.map(role => role.Dept);
          this.departments = [...new Set(departmentOptions)]; // Remove duplicates
        })
        .catch(error => {
          console.error('Error fetching department data:', error);
        });
    },

    async submitForm() {
  if (!this.roleName) {
    console.error('Role Name is required');
    return;
  }

  const data = {
    Role_Desc: this.roleDesc,
    Location: this.location,
    Dept: this.department,
    Deadline: this.deadline,
  };

  try {
    // Send PUT request to update the "Role" table
    await axios.put(`http://localhost:8000/update_role/${this.roleName}`, data);

    // Remove previous entries in the "Role_Skill" table for the current role
    await axios.delete(`http://localhost:8000/delete_roleskill/${this.roleName}`);

    // Update the "Role_Skill" table with the selected skills
    for (const selectedSkill of this.skillReq) {
      await axios.post('http://localhost:8000/new_role_skill', { // Use the existing endpoint
        roleName: this.roleName, // Keep using roleName
        skillName: selectedSkill, // Change to skillName to match your Flask app
      });
    }

    // Clear the form fields
    this.newroleName = '';
    this.roleDesc = '';
    this.skillReq = [];
    this.location = '';
    this.department = '';
    this.deadline = '';

    // Close the modal after a successful update
    this.$emit('form-submitted');
    this.$emit('close');
  } catch (error) {
    console.error(error);
  }
    },
  },

  created() {
    this.fetchRoleSkillData();
    this.fetchDepartments(); // Fetch department data
  },
};
</script>



<style scoped>
.modal {
  display: block;
}

.form-check {
  margin-top: 16px;
}

.form-check-label {
  margin-left: 8px;
}

.custom-select-height {
  height: 200px; /* Adjust the height as needed */
}
</style>
