<template>
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <h2>{{ roleName }}</h2>
        <p>{{ roleDescription }}</p>
        <h3>{{ skillName }}</h3>
        <p>{{ skillDescription }}</p>
        <button @click="closeModal">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      showModal: Boolean,
      roleName: String,
      roleDescription: String,
      skillName: String,
      skillDescription: String,
    },
    methods: {
      closeModal() {
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Modal styling goes here */
  .modal {
    /* Style to make it a modal dialog, like position, background, and opacity */
    display: block;
  }
  
  .modal-content {
    /* Style for the content of the modal, like padding, background color, etc. */
    display: flex;
  }
  </style>
  