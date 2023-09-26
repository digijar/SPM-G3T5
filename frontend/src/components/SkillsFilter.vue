<template>
    <div class="skills-filter">
      <h2>Skills Filter</h2>
      <div v-for="skill in uniqueSkills" :key="skill">
        <label>
          <input type="checkbox" v-model="selectedSkills" :value="skill" @change="filterListings">
          {{ skill }}
        </label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      listings: Array, // Array of listings with 'skills' attribute
    },
    data() {
      return {
        selectedSkills: [], // Selected skills
      };
    },
    computed: {
      uniqueSkills() {
        // Get a unique list of skills from listings
        const skillsSet = new Set();
        this.listings.forEach(listing => {
          if (listing.skills) {
            listing.skills.forEach(skill => skillsSet.add(skill));
          }
        });
        return Array.from(skillsSet);
      },
    },
    methods: {
      filterListings() {
        // Emit an event to notify the parent component of selected skills
        this.$emit('filter', this.selectedSkills);
      },
    },
  };
  </script>
  
  <style scoped>
  /* .skills-filter {
  } */
  </style>
  