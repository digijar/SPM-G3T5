<template>
  <div>
    <div class="header">
      <h1 class="title">Role Listing Management</h1>
    </div>
  </div>
</template>

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