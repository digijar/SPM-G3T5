<template>
    <div class="modal" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Details</h5>
            <button @click="closeModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <h3>Role Details: {{ roleName }}</h3>
            <p>{{ roleDescription }}</p>
            <h3>Skill Details: {{ skillName }}</h3>
            <p>{{ skillDescription }}</p>
          </div>
          <div class="modal-footer">
            <button @click="closeModal" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
      </div>
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
  