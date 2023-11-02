<style>
    .centered-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .btn {
        margin: 5px; /* Add margin between buttons */
    }
</style>

<template>
  <div class="container centered-container">
    <router-link to="/hrstaff">
      <button class="btn btn-primary">HR Staff</button>
    </router-link>

    <router-link to="/regstaff">
      <button class="btn btn-success">Regular Staff</button>
    </router-link>

    <!-- <router-link to="/testDB">
      <button class="btn btn-info">Test DB CRUD</button>
    </router-link> -->
      
  </div>
</template>
