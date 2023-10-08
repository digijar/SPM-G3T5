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
            <input type="text" id="roleName" v-model="newJob.roleName" class="input" required>
          </div>
        </div>

        <div class="form-group">
          <div class="input-container">
            <label for="skillRequired" class="label">Skill Required:</label>
            <input type="text" id="skillRequired" v-model="newJob.skillRequired" class="input" required>
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
    };
  },
  methods: {
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
