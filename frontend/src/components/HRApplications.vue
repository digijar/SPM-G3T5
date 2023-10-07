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
          <!-- Loop through applications data and display it -->
          <tr v-for="(application, index) in applications" :key="application.Application_ID">
            <td>{{ application.Application_ID }}</td>
            <td>{{ application.Role_Name }}</td>
            <td>{{ application.Staff_Name }}</td>
            <td>{{ application.Current_Dept }}</td>
            <td>{{ application.Skills_Match_Percentage }}</td>
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
        .get('http://localhost:8000/get_applications_data')
        .then((response) => {
          this.applications = response.data;
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