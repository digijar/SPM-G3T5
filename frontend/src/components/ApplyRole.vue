<template>
    <div>
      <div class="header">
        <h1 class="title">Open Role Listing</h1>
      </div>
      
      <!-- <button @click="fetchRoleData" class="btn btn-info">Fetch Role Data</button>
      <button @click="fetchSkillData" class="btn btn-info">Fetch Skill Data</button>
      <button @click="fetchRoleSkillData" class="btn btn-info">Fetch roleSkill Data</button> -->
      <div class="container mb-3">
        <input type="text" v-model="searchQuery" placeholder="Search by role name">
        <DeptFilter :allDepts="uniqueDepts" :selectedDept="selectedDept" :selectedLocation="selectedLocation" @update:selectedDept="selectedDept = $event" @update:selectedLocation="selectedLocation = $event" />
      </div>

      <!-- Table container -->
      <div class="table-container">
        <table class="job-listing-table">
          <thead>
            <tr>
              <th>Role Name</th>
              <th>Role Description</th>
              <th>Skills Required</th>
              <th>Department</th>
              <th>Location</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <!-- Loop through job listings and display them -->
            <tr v-for="role in filteredroleData" :key="role.Role_Name">
              <td>{{ role.Role_Name }}</td>
              <td>{{ role.Role_Desc.slice(0, 150) + "..." }}</td>
              <td>
                <ul>
                  <li v-for="skill in getRoleSkills(role.Role_Name)" :key="skill">{{ skill }}</li>
                </ul>
              </td>
              <td>{{ role.Dept }}</td>
              <td>{{ role.Location }}</td>
              <td>
                <button class="btn btn-success" @click="openModal_apply(role)">Apply</button>
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

    <ConfirmApplyModal
      :showModal="modalData_apply.showModal"
      :roleName="modalData_apply.roleName"
      @close="modalData_apply.showModal = false"
    />

  </template>
  
  <script>
  import axios from 'axios';
  import RoleDetailModal from './RoleDetailModal.vue';
  import ConfirmApplyModal from './ConfirmApplyModal.vue';
  import DeptFilter from './DeptFilter.vue';

  export default {
    name: 'ApplyRole',
    
    components: {
      RoleDetailModal,
      ConfirmApplyModal,
      DeptFilter,
    },

    data() {
      return {
        roleData: [],
        skillData: [],
        roleSkillData: [],
        roleSkills: [],
        formattedSkills: '',
        staffData: [],

        searchQuery: '',
        allDepts: [],
        selectedDept: '',
        selectedLocation: '',

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
                    // console.log(response.data);
                    this.staffData = response.data;
                    // this.getUniqueDepts();
                })
                .catch(error => {
                    console.error(error);
                });
        },

        getUniqueDepts() {
            const allDepts = this.staffData.map(staff => staff.Dept);
            return [...new Set(allDepts)];
          },
          selectDept(dept) {
            this.selectedDept = dept;
          },

          getRoleSkills(roleName) {
            const role = this.roleData.find(role => role.Role_Name === roleName);
            if (role) {
              const roleSkills = this.roleSkillData
                .filter(rs => rs.Role_Name === role.Role_Name)
                .map(rs => rs.Skill_Name);
              if (roleSkills.length > 0) {
                return roleSkills;
              }
            }
            return [];
          },


        // const role = this.roleData.find(role => role.Role_Name === roleName);
        // if (role) {
        //   const roleSkill = this.roleSkillData.find(rs => rs.Role_Name === role.Role_Name);
        //   if (roleSkill) {
        //     const skill = this.skillData.find(skill => skill.Skill_Name === roleSkill.Skill_Name);
        //     if (skill) {
        //       return skill.Skill_Name;
        //     }
        //   }
        // }

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

        openModal_apply(role) {
          this.modalData_apply.showModal = true;
          this.modalData_apply.roleName = role.Role_Name;
        },

        updateSelectedDept(value) {
          this.selectedDept = value;
        },

    },

    computed: {
        filteredroleData() {
          let filteredData = this.roleData;
          if (this.selectedDept) {
            filteredData = filteredData.filter(role => role.Dept === this.selectedDept);
          }
          if (this.selectedLocation) {
            filteredData = filteredData.filter(role => role.Location === this.selectedLocation);
          }
          if (this.searchQuery) {
            filteredData = filteredData.filter(role => role.Role_Name.toLowerCase().includes(this.searchQuery.toLowerCase()));
          }
          return filteredData;
        },

      uniqueDepts() {
          // const allDepts = this.staffData.map(staff => staff.Dept);
          return [...new Set(this.roleData.map(role => role.Dept))];
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
  
  .job-listing-table th, .job-listing-table td {
    border: 1px solid #ccc;
    padding: 8px;
  }
  
  .job-listing-table th {
    background-color: #f2f2f2;
    font-weight: bold;
  }
  </style>
  