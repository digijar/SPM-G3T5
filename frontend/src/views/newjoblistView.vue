
<script setup>
// import TheWelcome from '../components/TheWelcome.vue'
import TopNavHR from '../components/TopNavHR.vue'
import CreateNewJob from '../components/CreateNewJob.vue'
</script>


<template>
    <div>
        <TopNavHR></TopNavHR>
        <!-- <TheWelcome></TheWelcome> -->
      
      <!-- Display the job listing creation form -->
      <CreateNewJob></CreateNewJob>
      
      <!-- Display the job listings table (if needed) -->
      <!-- <div class="table-container">
        <table class="job-listing-table"> -->
          <!-- ... Table contents ... -->
        <!-- </table>
      </div> -->
    </div>
  </template>
  
  <script>
  export default {
    components: {
      TopNavHR,
      CreateNewJob,
    },
    
    // ... Other component code ...
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  