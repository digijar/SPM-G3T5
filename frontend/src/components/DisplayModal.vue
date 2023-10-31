<template>
  <div v-if="showModal" class="display-modal">
    <div class="display-modal-content">
      <span>{{ displayMessage }}</span>
      <button @click="closeModal">OK</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    displayMessage: String,
    showModal: Boolean,
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.display-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.display-modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}

.display-modal button {
  margin-top: 10px;
}
</style>
