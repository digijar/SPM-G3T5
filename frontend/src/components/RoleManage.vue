<template>
  <div>
    <div class="header">
      <h1 class="title">Job Listing Management</h1>

      <!-- Create Job Listing button -->
      <router-link to="/hrstaff/newjoblist" class="create-button">
      <button>Create a New Role Listing</button>
    </router-link>
    </div>
    
  </div>
</template>

<!-- <script>
export default {
  data() {
    return {
      jobListings: [], // Initialise empty array to store job listings
      showCreateForm: false, // Flag to control the visibility of the create job form
      newJob: { // Object to store data for a new job listing
        description: '',
        responsibilities: '',
        qualifications: '',
        salary: '',
        vacancies: '',
        deadline: '',
      },
    };
  },
  methods: {
    showCreateJobForm() {
      this.showCreateForm = true;
    },
    createJobListing() {
      // Add the new job listing to the jobListings array
      this.jobListings.push(this.newJob);
      
      // Reset the new job object and hide the create form
      this.newJob = {
        description: '',
        responsibilities: '',
        qualifications: '',
        salary: '',
        vacancies: '',
        deadline: '',
      };
      this.showCreateForm = false;
    },
  },
};
</script> -->

<style scoped>
/* component-specific styles here */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px; /* padding around header */
}

.title {
  margin: 0;
}

.create-button {
  /* padding around button */
  padding: 5px 10px;
}

.table-container {
  max-width: 800px;
  margin: 0 auto;
}

.job-listing-table {
  border-collapse: collapse;
  width: 100%;
}

.job-listing-table th, .job-listing-table td {
  border: 1px solid #ccc;
  padding: 8px;
}

.job-listing-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}
</style>