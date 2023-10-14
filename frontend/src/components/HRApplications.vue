<template>
  <div>
    <div class="header">
      <h1 class="title">Applications</h1>
    </div>

    <div class="row">
      <div class="filter-container col-2">
      <h2>Filters 
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-filter" viewBox="0 0 16 16">
          <path d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5z"/>
        </svg>
      </h2>
      <div class="filter-section">
        <h3>Role Names</h3>
        <div v-for="roleName in uniqueRoleNames" :key="roleName">
          <input
            type="checkbox"
            :value="roleName"
            v-model="selectedRoleNames"
          />
          {{ roleName }}
        </div>
      </div>
      <div class="filter-section">
        <h3>Departments</h3>
        <div v-for="dept in uniqueDepts" :key="dept">
          <input
            type="checkbox"
            :value="dept"
            v-model="selectedDepts"
          />
          {{ dept }}
        </div>
      </div>
    </div>

    <!-- Table container -->
    <div class="table-container col-10">
      <input type="text" v-model="searchQuery" placeholder="Search Application" />

      <table class="job-listing-table">
        <thead>
          <tr>
            <th class="text-center">Application ID</th>
            <th class="text-center">Role Name</th>
            <th class="text-center">Staff Name</th>
            <th class="text-center">Department</th>
            <th class="text-center">Skills Match Percentage</th>
            <th class="text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loop through applications data and display it -->
          <tr
            v-for="(application, index) in filteredApplications"
            :key="application.Application_ID"
            @click="showPopup(application)"
          >
            <td class="text-center">{{ application.Application_ID }}</td>
            <td class="text-center">{{ application.Role_Name }}</td>
            <!-- <td class="text-center">{{ application.Staff_ID}}</td> -->
            <td class="text-center">{{ application.Staff_Name }}</td>
            <td class="text-center">{{ application.Current_Dept }}</td>
            <td class="text-center">{{ application.Skills_Match_Percentage }}%</td>
            <td class="text-center">
                <!-- TODO: update this to show the skills of the applicant -->
                <button @click="fetchApplicantSkills(application)" class="btn btn-primary">View skills</button>
                <!-- <button @click="" class="btn btn-primary">View skills</button> -->
            </td>
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
          <p class="card-text">Staff ID: {{ selectedApplication.Staff_ID }}</p>
          <p class="card-text">Department: {{ selectedApplication.Current_Dept }}</p>
          <p class="card-text">Skills Match Percentage: {{ selectedApplication.Skills_Match_Percentage }}%</p>

          <!-- Display skills as a list of bullet points -->
          <div v-if="selectedApplicantSkills.length > 0">
            <h5>Skills:</h5>
            <ul class="skills-list">
              <li v-for="skill in selectedApplicantSkills" :key="skill.Skill_Name">
                {{ skill.Skill_Name }}
              </li>
            </ul>
          </div>

          <button class="btn btn-primary" @click="hidePopup">Close</button>
        </div>
      </div>
    </div>


    <!-- Add this section to display staff skills -->
    <div class="staff-skills">
      <h2>Staff Skills</h2>
      <ul>
        <li v-for="(staffSkill, index) in staffSkills" :key="index">
          Staff ID: {{ staffSkill.Staff_ID }}, Skill Name: {{ staffSkill.Skill_Name }}
        </li>
      </ul>
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
      selectedRoleNames: [],   // Array to store selected Role_Names
      selectedDepts: [],
      searchQuery: '', // Add this line to define searchQuery
      staffSkills: [], // Add this line to initialize the staffSkills array
      staffNameMap: {}, // New object to store staff names
      selectedApplicantSkills: [], // Add this line to store skills

    };
  },

  computed: {
    filteredApplications() {
      return this.applications.filter(app => {
        const roleNameMatch = this.selectedRoleNames.length === 0 || this.selectedRoleNames.includes(app.Role_Name);
        const deptMatch = this.selectedDepts.length === 0 || this.selectedDepts.includes(app.Current_Dept);
        const searchMatch = !this.searchQuery ||
          app.Application_ID.toString().includes(this.searchQuery) ||
          app.Role_Name.includes(this.searchQuery) ||
          app.Staff_Name.includes(this.searchQuery) ||
          app.Current_Dept.includes(this.searchQuery);
        return roleNameMatch && deptMatch && searchMatch;
      });
    },

    uniqueRoleNames() {
      return [...new Set(this.applications.map(app => app.Role_Name))];
    },
    uniqueDepts() {
      return [...new Set(this.applications.map(app => app.Current_Dept))];
    },
  },

  created() {
    this.fetchApplications();
    this.fetchStaffSkills(); // Call the new method to fetch staff skills
  },

  methods: {
    fetchApplications() {
      axios
        .get('http://localhost:8000/get_applications_data')
        .then((response) => {
          this.applications = response.data.map((application) => {
            // Fetch the staff name based on the staff ID
            const staffId = application.Staff_ID;
            if (this.staffNameMap[staffId]) {
              application.Staff_Name = this.staffNameMap[staffId];
            } else {
              // If staff name is not in the map, make an API request to get it
              this.fetchStaffNameById(staffId);
            }
            return application;
          });
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

    fetchStaffSkills() {
      axios
        .get('http://localhost:8000/get_staff_skill')
        .then((response) => {
          this.staffSkills = response.data; // Update the staffSkills data
        })
        .catch((error) => {
          console.error(error);
        });
    },

    fetchStaffNameById(staffId) {
      axios
        .get(`http://localhost:8000/get_staff_data_by_id/${staffId}`)
        .then((response) => {
          const staffData = response.data;
          const staffName = `${staffData.Staff_FName} ${staffData.Staff_LName}`;
          this.staffNameMap[staffId] = staffName;
          // Update the staff name in the applications array
          this.applications.forEach((application) => {
            if (application.Staff_ID === staffId) {
              application.Staff_Name = staffName;
            }
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },

    fetchApplicantSkills(applicant) {
      axios
        .get(`http://localhost:8000/get_staff_skill_by_id/${applicant.Staff_ID}`)
        .then((response) => {
          this.selectedApplicantSkills = response.data;
          this.showPopup(applicant); // Show the popup after fetching skills
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
  max-width: 1000px;
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

.filter-container{
  padding-left: 30px;
}

.skills-list {
  padding-left: 0;
  list-style-position: inside;
}
</style>