<template>
    <div>
      <h1>Listings</h1>
      <div class="listing-card" v-for="listing in listings" :key="listing.id">
        <div class="card-content">
          <h2>{{ listing.title }}</h2>
          <p>Skills: {{ listing.skills.join(', ') }}</p>
          <!-- Add other listing details here -->
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      listings: Array, // Array of listings with 'skills' attribute
    },
  };
  </script>
  
  <style scoped>
  .listing-card {
    background-color: #fff; /* Card background color */
    border: 1px solid #ddd; /* Card border */
    border-radius: 5px; /* Rounded corners */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Shadow effect */
  
    margin: 10px; /* Spacing between cards */
    padding: 10px; /* Padding within the card */
  }
  
  .card-content {
    /* Add your styling for the content inside the card */
  }
  
  /* Customize the card styles further as needed */
  </style>
  