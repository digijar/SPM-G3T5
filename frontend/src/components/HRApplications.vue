<template>
    <div>
      <div class="header">
        <h1 class="title">Applications</h1>
      </div>

      <!-- Table container -->
      <div class="table-container">
        <input type="text" v-model="searchQuery" placeholder="Search Application">
      
        <table class="job-listing-table">
          <thead>
            <tr>
              <th>Application ID</th>
              <th>Role Name</th>
              <th>Staff Name</th>
              <th>Current Role</th>
              <th>Skills Match Percentage</th>
            </tr>
          </thead>
          <tbody>
            <!-- Loop through job listings and display them -->
            <tr v-for="(application, index) in applications" :key="application.id">
              <td>{{ index + 1 }}</td>
              <td>{{ application.roleName }}</td>
              <td>{{ application.staffName }}</td>
              <td>{{ application.currentRole }}</td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        applications: [],
      };
    },
  
    created() {
      this.fetchApplications();
    },
  
    methods: {
      fetchApplications() {
        axios
          .get('http://localhost:8000/get_applications')
          .then((response) => {
            this.applications = response.data.map((application) => ({
              id: application.id,
              roleName: application.roleName,
              staffName: `${application.staff_FName} ${application.staff_LName}`,
              currentRole: application.Dept,
            }));
          })
          .catch((error) => {
            console.error(error);
          });
      },
    },
  };
  </script>
  
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
  
  .job-listing-table th,
  .job-listing-table td {
    border: 1px solid #ccc;
    padding: 8px;
  }
  
  .job-listing-table th {
    background-color: #f2f2f2;
    font-weight: bold;
  }
  </style>