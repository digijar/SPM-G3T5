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
            <th class="text-center" @click="sortTable('Application_ID')">Application ID{{ sortIcon('Application_ID') }}</th>
            <th class="text-center" @click="sortTable('Role_Name')">Role Name{{ sortIcon('Role_Name') }}</th>
            <th class="text-center" @click="sortTable('Staff_Name')">Staff Name{{ sortIcon('Staff_Name') }}</th>
            <th class="text-center" @click="sortTable('Current_Dept')">Department{{ sortIcon('Current_Dept') }}</th>
            <th class="text-center" @click="sortTable('Skills_Match_Percentage')">Skills Match Percentage{{ sortIcon('Skills_Match_Percentage') }}</th>
            <th class="text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loop through applications data and display it -->
          <tr
            v-for="(application, index) in sortedApplications"
            :key="application.Application_ID"
          >
            <td class="text-center">{{ application.Application_ID }}</td>
            <td class="text-center">{{ application.Role_Name }}</td>
            <!-- <td class="text-center">{{ application.Staff_ID}}</td> -->
            <td class="text-center">{{ application.Staff_Name }}</td>
            <td class="text-center">{{ application.Current_Dept }}</td>
            <td class="text-center">{{ application.Skills_Match_Percentage }}%</td>
            <td class="text-center">
                <button @click="fetchApplicantSkills(application)" class="btn btn-primary">View skills</button>
                <!-- <button @click="" class="btn btn-primary">View skills</button> -->
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Popup container -->
    <div class="popup-container" v-if="selectedApplication">
      <div class="popup card" style="max-height: 80vh; overflow-y: auto;">
        <div class="card-body">
          <h4 class="card-title"> Job Application for {{ selectedApplication.Role_Name }} </h4>
          <p class="card-text">Application ID: {{ selectedApplication.Application_ID }}</p>
          <p class="card-text">Staff ID: {{ selectedApplication.Staff_ID }}</p>
          <p class="card-text">Name: {{ selectedApplication.Staff_Name }}</p>
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

          <!-- Display missing skills as a list of bullet points -->
        <!-- <div v-if="selectedMissingSkills.length > 0">
          <h5>Missing Skills:</h5>
          <ul class="skills-list">
            <li v-for="skill in selectedMissingSkills" :key="skill.Skill_Name">
              {{ skill.Skill_Name }}
            </li>
          </ul>
        </div> -->
        <div>
            <h5>Missing Skills:</h5>
            <div v-if="selectedMissingSkills.length > 0">
              <ul class="skills-list">
                <li v-for="skill in selectedMissingSkills" :key="skill.Skill_Name">
                  {{ skill.Skill_Name }}
                </li>
              </ul>
            </div>
            <div v-else>
              <p>- no missing skills -</p>
            </div>
          </div>

          <button class="btn btn-primary" @click="hidePopup">Close</button>
        </div>
      </div>
    </div>
  </div>

    </div>

    
</template>

<script>
import 'jquery';
import axios from 'axios';

export default {
  data() {
    return {
      applications: [],
      selectedApplication: null,
      selectedRoleNames: [],   // Store selected Role_Names
      selectedDepts: [], // Store selected Depts
      searchQuery: '', // Define searchQuery
      staffSkills: [], // Initialize the staffSkills array
      staffNameMap: {}, // New object to store staff names
      selectedApplicantSkills: [], // Store skills
      selectedMissingSkills: [], // Store missing skills
      sortColumn: '',
      sortDirection: 'asc',
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

    sortedApplications() {
      const column = this.sortColumn;
      const direction = this.sortDirection === 'asc' ? 1 : -1;
      return this.filteredApplications.sort((a, b) => {
        if (column === 'Skills_Match_Percentage') {
          // Convert the Skills_Match_Percentage values to numbers before sorting
          const aPercentage = parseFloat(a[column]);
          const bPercentage = parseFloat(b[column]);
          if (aPercentage < bPercentage) return -1 * direction;
          if (aPercentage > bPercentage) return 1 * direction;
          return 0;
        } else {
          if (a[column] < b[column]) return -1 * direction;
          if (a[column] > b[column]) return 1 * direction;
          return 0;
        }
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
            // Fetch and update the skill match percentage for each application
            this.fetchSkillMatch(application); // Update the skill match percentage
            
            const staffId = application.Staff_ID;
            if (this.staffNameMap[staffId]) {
              application.Staff_Name = this.staffNameMap[staffId];
            } else {
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
          this.fetchMissingSkills(applicant); // Show the popup after fetching skills
        })
        .catch((error) => {
          console.error(error);
        });
    },
    fetchMissingSkills(application) {
      axios
        .get(`http://localhost:8000/get_roleskill_data_by_name/${application.Role_Name}`)
        .then((response) => {
          const roleSkills = response.data;
          axios
            .get(`http://localhost:8000/get_staff_skill_by_id/${application.Staff_ID}`)
            .then((response) => {
              const applicantSkills = response.data;
              const applicantSkillNames = applicantSkills.map(skill => skill.Skill_Name);
              const missingSkills = roleSkills.filter(skill => !applicantSkillNames.includes(skill.Skill_Name));
              this.selectedApplicantSkills = applicantSkills;
              this.selectedMissingSkills = missingSkills;
              this.showPopup(application); // Show the popup after fetching skills
            })
            .catch((error) => {
              console.error(error);
            });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    fetchSkillMatch(application) {
      axios
        .get(`http://localhost:8000/get_skill_match/${application.Role_Name}/${application.Staff_ID}`)
        .then((response) => {
          // Update the Skills_Match_Percentage property for the selected application
          application.Skills_Match_Percentage = parseFloat(response.data.Match_Percentage).toFixed(2);
          console.log('Skills Match Percentage updated:', application.Skills_Match_Percentage); // Add this line for debugging
          // this.showPopup(application);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    sortTable(column) {
      if (column === this.sortColumn) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
    },

    sortIcon(column) {
      if (column !== this.sortColumn) {
        return '';
      } else if (this.sortDirection === 'asc') {
        return '▲';
      } else {
        return '▼';
      }
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