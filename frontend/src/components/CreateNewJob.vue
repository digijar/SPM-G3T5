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
            <input type="text" id="roleName" v-model="newJob.roleName" class="form-control" required>
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="RoleDesc" class="label">Role Description:</label>
            <textarea class="form-control" id="RoleDesc" v-model="roleDesc"></textarea>
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="skillRequired" class="label">Skill Required:</label>
            <select class="form-select" id="skillRequired" v-model="newJob.skillRequired">
              <option value="" disabled>Select</option>
              <option v-for="skill in skills" :key="skill.Skill_Name" :value="skill.Skill_Name">{{ skill.Skill_Name }}</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="Deadline" class="label">Deadline:</label>
            <input type="date" class="form-control" id="Deadline" v-model="deadline">
          </div>
        </div>

        <button type="submit" class="submit-button">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newJob: {
        roleName: '',
        skillRequired: '',
      },
      skills: [], // Add a new data property for skills
    };
  },
  created() {
    // Fetch skill data when the component is created
    this.fetchSkills();
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
    submitJobListing() {
      // Prepare the data for submission
      const formData = {
        roleName: this.newJob.roleName,
        skillRequired: this.newJob.skillRequired,
      };

      // Send the data to the backend using the appropriate API endpoint
      axios.post('http://localhost:8000/create_new_job_listing', formData)
        .then(response => {
          console.log('Data submitted successfully:', response.data);
          // Reset form fields after successful submission if needed
          this.newJob = {
            roleName: '',
            skillRequired: '',
          };
        })
        .catch(error => {
          console.error('Error submitting data:', error);
        });
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
