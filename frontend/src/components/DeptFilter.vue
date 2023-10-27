<template>
    <div>
      <select :value="selectedDept" @input="$emit('update:selectedDept', $event.target.value)">
        <option value="">All Departments</option>
        <option v-for="dept in uniqueDepts" :key="dept" :value="dept">{{ dept }}</option>
      </select>
      <select :value="selectedLocation" @input="$emit('update:selectedLocation', $event.target.value)">
      <option value="">All Locations</option>
      <option value="Remote">Remote</option>
      <option value="On-Site">On-Site</option>
    </select>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DeptFilter',
    props: {
      allDepts: {
        type: Array,
        required: true,
      },
      selectedDept: {
        type: String,
        required: true,
      },
      selectedLocation: {
        type: String,
        required: true,
      },
    },
    computed: {
      uniqueDepts() {
        return [...new Set(this.allDepts)];
      },
    },
  };
  </script>