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
            <th>Department</th>
            <th>Skills Match Percentage</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loop through applications data and display it -->
                <tr v-for="(application, index) in applications" :key="application.Application_ID" @click="showPopup(application)">
                  <td class="text-center">{{ application.Application_ID }}</td>
                  <td class="text-center">{{ application.Role_Name }}</td>
                  <td class="text-center">{{ application.Staff_Name }}</td>
                  <td class="text-center">{{ application.Current_Dept }}</td>
                  <td class="text-center">{{ application.Skills_Match_Percentage }}%</td>
                </tr>
              </tbody>
            </table>
          </div>

    <!-- Popup container -->
    <div class="popup-container" v-if="selectedApplication">
      <div class="popup card">
        <div class="card-body">
          <h4 class="card-title"> Job Application for {{ selectedApplication.Role_Name }} </h4>
          <p class="card-text">Application ID: {{ selectedApplication.Application_ID }}</p>
          <p class="card-text">Staff Name: {{ selectedApplication.Staff_Name }}</p>
          <p class="card-text">Department: {{ selectedApplication.Current_Dept }}</p>
          <p class="card-text">Skills Match Percentage: {{ selectedApplication.Skills_Match_Percentage }}%</p>
          
          <button class="btn btn-primary" @click="hidePopup">Close</button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      applications: [],
      selectedApplication: null,
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

    showPopup(application) {
      this.selectedApplication = application;
      $('#exampleModalCenter').modal('show');
    },

    hidePopup() {
      this.selectedApplication = null;
      $('#exampleModalCenter').modal('hide');
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

.popup-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  text-align: center;
}

.popup h2 {
  margin-top: 0;
}

.popup p {
  margin-bottom: 10px;
}

.popup button {
  padding: 5px 10px;
}
</style>