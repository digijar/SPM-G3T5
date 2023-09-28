<template>
    <div>
      <div class="header">
        <h1 class="title">Open Role Listing</h1>
      </div>
      
      <button @click="fetchRoleData" class="btn btn-info">Fetch Role Data</button>
      <button @click="fetchSkillData" class="btn btn-info">Fetch Skill Data</button>
      <button @click="fetchRoleSkillData" class="btn btn-info">Fetch roleSkill Data</button>
      
      <input type="text" v-model="searchQuery" placeholder="Search by role name">

      <!-- Table container -->
      <div class="table-container">
        <table class="job-listing-table">
          <thead>
            <tr>
              <th>Role Name</th>
              <th>Role Description</th>
              <th>Skills Required</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <!-- Loop through job listings and display them -->
            <tr v-for="role in filteredroleData" :key="role.Role_Name">
              <td>{{ role.Role_Name }}</td>
              <td>{{ role.Role_Desc }}</td>
              <td>{{ getSkillName(role.Role_Name) }}</td>
              <td>
                <button class="btn btn-success">Apply</button>
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

  </template>
  
  <script>
  import axios from 'axios';
  import RoleDetailModal from './RoleDetailModal.vue';

  export default {
    components: {
      RoleDetailModal
    },

    data() {
      return {
        roleData: [],
        skillData: [],
        roleSkillData: [],
        searchQuery: '',
        modalData: {
          showModal: false,
          roleName: '',
          roleDescription: '',
          skillName: '',
          skillDescription: '',
          },
      };
    },

    created() {
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
                    console.log(response.data);
                    this.roleSkillData = response.data;
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

          openModal(role) {
            this.modalData.showModal = true;
            this.modalData.roleName = role.Role_Name;
            this.modalData.roleDescription = role.Role_Desc;
            this.modalData.skillName = this.getSkillName(role.Role_Name);
            this.modalData.skillDescription = this.getSkillDescription(role.Role_Name);
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
  