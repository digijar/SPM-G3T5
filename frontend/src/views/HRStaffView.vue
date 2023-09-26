<template>
    <div>
        <TopNav></TopNav>
        <!-- <TheWelcome></TheWelcome> -->
        <RoleManage></RoleManage>
    </div>
    <div class="page-container">
        <div class="sidebar">
        <SkillsFilter :listings="listings" @filter="filterListings"></SkillsFilter>
        </div>
    <div class="listings-container">
      <ListingsDisplay :listings="filteredListings"></ListingsDisplay>
    </div>
  </div>
</template>
  
  <script>
import SkillsFilter from '../components/SkillsFilter.vue';
import ListingsDisplay from '../components/ListingsDisplay.vue';
// import TheWelcome from '../components/TheWelcome.vue'
import TopNav from '../components/TopNav.vue';
import RoleManage from '../components/RoleManage.vue';
  
  export default {
    components: {
    SkillsFilter,
    ListingsDisplay,
    RoleManage,
    TopNav
},
    data() {
      return {
        listings: [
          {
            id: 1,
            title: 'Job 1',
            skills: ['JavaScript', 'React', 'Node.js'],
          },
          {
            id: 2,
            title: 'Job 2',
            skills: ['Vue.js', 'HTML', 'CSS'],
          },
          {
            id: 3,
            title: 'Job 3',
            skills: ['Python', 'Django'],
          },
          // Add more listings with similar structure
        ],
        filteredListings: [], // Filtered listings based on selected skills
      };
    },
    created() {
      // Initialize filteredListings with all listings when the component is created
      this.filteredListings = [...this.listings];
    },
    methods: {
      filterListings(selectedSkills) {
        // Filter listings based on selected skills
        this.filteredListings = this.listings.filter(listing => {
          return selectedSkills.every(skill => listing.skills.includes(skill));
        });
      },
    },
  };
  </script>

<style scoped>
.page-container {
  display: flex;
}

.sidebar {
  width: 250px; /* Adjust the width of the sidebar as needed */
  background-color: #f0f0f0; /* Background color for the sidebar */
  padding: 20px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2); /* Add shadow to the sidebar */
}

.listings-container {
  flex-grow: 1; /* Allow the listings container to grow and take up remaining space */
  padding: 20px;
}

/* Style for the SkillsFilter component within the sidebar */
.skills-filter {
  /* Add your styling for the SkillsFilter component here */
}

/* Style for the ListingsDisplay component within the listings container */
.listings {
  /* Add your styling for the ListingsDisplay component here */
}

</style>



