<template>
    <div class="table-container">
      <SkillsFilter :listings="listings" @filter="filterListings"></SkillsFilter>
  
      <table class="listings-table">
        <!-- ... -->
        <thead>
          <tr>
            <th class="text-center">Role Name</th>
            <th class="text-center">Skill Required</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="listing in filteredListings" :key="listing.Role_Skill_ID">
            <!-- <td>{{ listing.Role_Skill_ID }}</td> -->
            <td>{{ listing.Role_Name }}</td>
            <td>{{ listing.Skill_Name }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import SkillsFilter from './SkillsFilter.vue';
  import axios from 'axios';
  
  export default {
    components: {
      SkillsFilter,
    },
    data() {
      return {
        listings: [],
        selectedSkills: [],
      };
    },
    computed: {
      filteredListings() {
        // Filter listings based on selected skills
        if (this.selectedSkills.length === 0) {
          return this.listings; // Return all listings if no skills are selected
        }
        return this.listings.filter(listing => this.selectedSkills.includes(listing.Skill_Name));
      },
    },
    methods: {
      fetchData() {
        axios.get('http://localhost:8000/get_roleskill_data')
          .then(response => {
            this.listings = response.data;
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
      },
      filterListings(selectedSkills) {
        this.selectedSkills = selectedSkills;
      },
    },
    mounted() {
      this.fetchData();
    },
  };
  </script>
  
  <style>
.table-container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .listings-table {
    border-collapse: collapse;
    width: 100%;
  }
  
  .listings-table th, .listings-table td {
    border: 1px solid #ccc;
    padding: 8px;
  }
  
  .listings-table th {
    background-color: #f2f2f2;
    font-weight: bold;
  }
  
  </style>

  