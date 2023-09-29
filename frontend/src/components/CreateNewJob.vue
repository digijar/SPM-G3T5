<template>
    <div>
      <h2>Create a New Job Listing</h2>
  
      <form @submit.prevent="submitJobListing">
        <!-- Add form fields for job listing details -->
        <div class="form-group">
          <label for="description">Job Description:</label>
          <input type="text" id="description" v-model="newJob.description" required>
        </div>
        
        <!-- Add more form fields for other job details (responsibilities, qualifications, etc.) -->
        
        <button type="submit">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        newJob: {
          description: '',
          // Add more properties for other job details
        },
      };
    },
    methods: {
      submitJobListing() {
        // Handle the submission logic here (e.g., send data to the backend)
        console.log('New job listing data:', this.newJob);
        // Reset form fields after submission if needed
        this.newJob = {
          description: '',
          // Reset other properties as well
        };
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  