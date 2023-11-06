<template>
  <div>
    <!-- Header Section -->
    <div class="header">
      <h1 class="title">Create a New Job Listing</h1>
    </div>

    <!-- Form Section -->
    <div class="form-container">
      <form @submit.prevent="submitJobListing">
        <div class="form-group">
          <div class="input-container">
            <label for="roleName" class="label">Role Name:</label>
            <input type="text" id="roleName" v-model="newJob.roleName" class="form-control">
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="RoleDesc" class="label">Role Description:</label>
            <textarea class="form-control" id="RoleDesc" v-model="newJob.roleDesc"></textarea>
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="skillRequired" class="label">Skill Required:</label>
            <select class="form-select" id="skillRequired" v-model="newJob.skillsRequired" multiple>
              <option value="" disabled>Select</option>
              <option v-for="skill in skills" :key="skill.Skill_Name" :value="skill.Skill_Name">{{ skill.Skill_Name }}</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label class="label">Location:</label>
            <div class="radio-container">
              <div class="radio-option">
                <input type="radio" id="remote" value="Remote" v-model="newJob.location">
                <label for="remote">Remote</label>
              </div>
              <div class="radio-option">
                <input type="radio" id="onSite" value="On-Site" v-model="newJob.location">
                <label for="onSite">On-Site</label>
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="dept" class="label">Department:</label>
            <!-- Replace the select with an input -->
            <input type="text" id="dept" v-model="newJob.dept" class="form-control">
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="Deadline" class="label">Deadline:</label>
            <input type="date" class="form-control" id="Deadline" v-model="newJob.deadline">
          </div>
        </div>

        <button type="submit" class="btn btn-primary submit-button">Submit</button>
      </form>
    </div>

    <display-modal :display-message="displayMessage" :show-modal="showDisplayPopup" @close="closeDisplayPopup" />
  </div>
</template>

<script>
import axios from 'axios';
import DisplayModal from "./DisplayModal.vue";

export default {
  components: {
    DisplayModal,
  },
  data() {
    return {
      newJob: {
        roleName: '',
        roleDesc: '',
        skillsRequired: [],
        location: '',
        deadline: '',
      },
      skills: [],
      departments: [], 
      displayMessage: "",
      showDisplayPopup: false,
    };
  },
  created() {
    this.fetchSkills();
    this.fetchDepartments();
  },
  methods: {
    fetchSkills() {
      axios.get('http://localhost:8000/get_skill_data')
        .then(response => {
          this.skills = response.data;
        })
        .catch(error => {
          console.error('Error fetching skill data:', error);
        });
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
    submitJobListing() {
  if (
    !this.newJob.roleName ||
    !this.newJob.roleDesc ||
    this.newJob.skillsRequired.length === 0 || // Check for at least one skill selection
    !this.newJob.location ||
    !this.newJob.dept ||
    !this.newJob.deadline
  ) {
    this.displayMessage = 'Please fill in all form fields   ';
    this.showDisplayPopup = true;
    return;
  }

  axios.get('http://localhost:8000/check_role_exists', {
    params: { roleName: this.newJob.roleName }
  })
    .then(response => {
      if (response.data.exists) {
        this.displayMessage = 'Role Name already exists   ';
        this.showDisplayPopup = true;
      } else {
        // Create the job listing
        const formData = {
          roleName: this.newJob.roleName,
          roleDesc: this.newJob.roleDesc,
          dept: this.newJob.dept,
          location: this.newJob.location,
          deadline: this.newJob.deadline,
          skills: this.newJob.skillsRequired,
        };

        axios.post('http://localhost:8000/create_new_job_listing', formData)
          .then(response => {
            console.log('Data submitted successfully:', response.data);

            // Send POST request for each selected skill
            this.newJob.skillsRequired.forEach(skillName => {
              const roleSkillData = {
                roleName: formData.roleName,
                skillName,
              };
              axios.post('http://localhost:8000/new_role_skill', roleSkillData)
                .then(response => {
                  console.log('Role_Skill created successfully:', response.data);
                })
                .catch(error => {
                  console.error('Error updating Role_Skill:', error);
                });
            });

            this.displayMessage = "Form submitted successfully   ";
            this.showDisplayPopup = true;

            // Reset form fields after successful submission
            this.newJob = {
              roleName: '',
              roleDesc: '',
              skillsRequired: [], // Clear selected skills
              location: '',
              dept: '',
              deadline: '',
            };
          })
          .catch(error => {
            console.error('Error submitting data:', error);
          });
      }
    })
    .catch(error => {
      console.error('Error checking role existence:', error);
    });

    },
    
    closeDisplayPopup() {
      this.showDisplayPopup = false;
    },

  },
};
</script>


<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
}

.page-heading {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 16px;
}

.form-container {
  text-align: center;
  margin-top: 16px;
}

.form-group {
  margin-bottom: 16px;
  text-align: left;
}

.label {
  font-size: 18px;
  font-weight: bold;
}

.input-container {
  width: 50%;
  margin: 0 auto;
  padding: 10px;
}

.input {
  width: 100%;
  font-size: 18px;
  padding: 8px;
}

.submit-button {
  font-size: 18px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}
</style>
