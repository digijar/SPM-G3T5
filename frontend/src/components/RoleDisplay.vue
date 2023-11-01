<template>
  <div>
    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="Search by role name">
      <router-link to="/hrstaff/newjoblist" class="create-button">
        <button>Create a New Role Listing</button>
      </router-link>
    </div>

    <!-- Table container -->
    <div class="table-container">
      <table class="job-listing-table">
        <thead>
          <tr>
            <th>Role Name</th>
            <th>Role Description</th>
            <th>Department</th> <!-- Add Department column -->
            <th>Location</th>   <!-- Add Location column -->
            <th>Skills Required</th>
            <th>Deadline</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loop through job listings and display them -->
          <tr v-for="role in filteredroleData" :key="role.Role_Name">
            <td>{{ role.Role_Name }}</td>
            <td>{{ role.Role_Desc }}</td>
            <td>{{ role.Dept }}</td>    <!-- Display Department -->
            <td>{{ role.Location }}</td> <!-- Display Location -->
            <td>{{ getSkillName(role.Role_Name) }}</td>
            <td>{{ getDeadline(role.Role_Name) }}</td>
            <td>
              <button class="btn btn-success" @click="openModal_apply(role)">Update Listing</button>
              <br>
              <button class="btn btn-info" @click="openModal(role)">More Details</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

<RoleDetailModal
:showModal="modalData.showModal"
:roleName="modalData.roleName"
:roleDescription="modalData.roleDescription"
:skillName="modalData.skillName"
:skillDescription="modalData.skillDescription"
@close="modalData.showModal = false"
/>

<EditJobModal
  :showModal="modalData_apply.showModal"
  :roleName="modalData_apply.roleName"
  :refresh="modalData_apply.refresh"
  @close="modalData_apply.showModal = false"
  @form-submitted="handleFormSubmitted"
/>

<UpdateSuccessModal
  :showModal="modalData_updateSuccess.showModal"
  @close="modalData_updateSuccess.showModal = false"
/>

</template>

<script>
import axios from 'axios';
import RoleDetailModal from './RoleDetailModal.vue';
import EditJobModal from './EditJobModal.vue';
import UpdateSuccessModal from './UpdateSuccessModal.vue';

export default {
components: {
RoleDetailModal,
EditJobModal,
UpdateSuccessModal
},

data() {
return {
  roleData: [],
  skillData: [],
  roleSkillData: [],
  staffData: [],
  searchQuery: '',
  allDepts: [],
  modalData: {
    showModal: false,
    roleName: '',
    roleDescription: '',
    skillName: '',
    skillDescription: '',
    },
  modalData_apply: {
    showModal: false,
    roleName: '',
    },
  modalData_updateSuccess: {
    showModal: false,
    },
};
},

created() {
this.fetchStaffData();
this.fetchRoleData();
this.fetchSkillData();
this.fetchRoleSkillData();
},

methods: {
fetchRoleData() {
      axios.get('http://localhost:8000/get_role_data')
          .then(response => {
              // console.log(response.data);
              this.roleData = response.data;
          })
          .catch(error => {
              console.error(error);
          });
  },

  fetchSkillData() {
      axios.get('http://localhost:8000/get_skill_data')
          .then(response => {
              // console.log(response.data);
              this.skillData = response.data;
          })
          .catch(error => {
              console.error(error);
          });
  },

  fetchRoleSkillData() {
      axios.get('http://localhost:8000/get_roleskill_data')
          .then(response => {
              // console.log(response.data);
              this.roleSkillData = response.data;
          })
          .catch(error => {
              console.error(error);
          });
  },

  fetchStaffData() {
      axios.get('http://localhost:8000/get_staff_data')
          .then(response => {
              // console.log(response.data[0].Dept);
              this.staffData = response.data;
              // this.getUniqueDepts();
          })
          .catch(error => {
              console.error(error);
          });
  },

  getSkillName(roleName) {
      const role = this.roleData.find(role => role.Role_Name === roleName);
      if (role) {
        const roleSkill = this.roleSkillData.find(rs => rs.Role_Name === role.Role_Name);
        if (roleSkill) {
          const skill = this.skillData.find(skill => skill.Skill_Name === roleSkill.Skill_Name);
          if (skill) {
            return skill.Skill_Name;
          }
        }
      }
      return '';
    },

    getSkillDescription(roleName) {
      const role = this.roleData.find(role => role.Role_Name === roleName);
      if (role) {
        const roleSkill = this.roleSkillData.find(rs => rs.Role_Name === role.Role_Name);
        if (roleSkill) {
          const skill = this.skillData.find(skill => skill.Skill_Name === roleSkill.Skill_Name);
          if (skill) {
            return skill.Skill_Desc;
          }
        }
      }
      return '';
    },

    getDeadline(roleName) {
      const role = this.roleData.find(role => role.Role_Name === roleName);
  if (role) {
    if (role.Deadline) {
      // Parse the date string
      const deadlineDate = new Date(role.Deadline);

      // Extract day, month, and year
      const day = String(deadlineDate.getDate()).padStart(2, '0');
      const month = String(deadlineDate.getMonth() + 1).padStart(2, '0'); // Month is zero-based
      const year = deadlineDate.getFullYear();

      // Create the formatted date string
      const formattedDate = `${day}-${month}-${year}`;

      return formattedDate;
    }
  }
  return '';
},

    openModal(role) {
      this.modalData.showModal = true;
      this.modalData.roleName = role.Role_Name;
      this.modalData.roleDescription = role.Role_Desc;
      this.modalData.skillName = this.getSkillName(role.Role_Name);
      this.modalData.skillDescription = this.getSkillDescription(role.Role_Name);
    },

    openModal_apply(role) {
      this.modalData_apply.showModal = true;
      this.modalData_apply.roleName = role.Role_Name;
    },

    handleFormSubmitted() {
    this.fetchRoleData();
    this.fetchRoleSkillData();
    this.modalData_updateSuccess.showModal = true;
  },


},

computed: {
filteredroleData() {
  return this.roleData.filter((role) => {
    return role.Role_Name.toLowerCase().includes(this.searchQuery.toLowerCase());
  });
}
}
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
  max-width: 1000px; /* Adjust the maximum width as per your requirement */
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

.search-bar {
  padding: 10px;
}
</style>
