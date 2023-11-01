<template>
    <div class="modal" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update Success</h5>
            <button @click="closeModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <!-- <div class="modal-body">
            <p>The update was successful!</p>
          </div> -->
          <!-- <div class="modal-footer">
            <button @click="closeModal" type="button" class="btn btn-success" data-bs-dismiss="modal">Close</button>
          </div> -->
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      showModal: Boolean,
    },
    methods: {
      closeModal() {
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  .modal {
    display: block;
  }
  </style>
  