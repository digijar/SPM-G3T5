<template>
  <div class="modal" v-if="showModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Details</h5>
          <button @click="closeModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="form-floating mb-3">
              <input type="text" class="form-control" id="InputValue_RoleName" v-model="roleName">
              <label for="InputValue_RoleName">Role Name</label>
            </div>

            <div class="form-floating mb-3">
              <textarea class="form-control" id="InputValue_RoleDesc" v-model="roleDesc"></textarea>
              <label for="InputValue_RoleDesc">Role Description</label>
            </div>

            <div class="form-floating mb-3">
              <select class="form-select" id="InputValue_skillReq" v-model="skillReq">
                <option value="" disabled>Select</option>
                <option v-for="skill in skills" :key="skill.Skill_Name" :value="skill.Skill_Name">{{ skill.Skill_Name }}</option>
              </select>
              <label for="InputValue_skillReq">Skill Required</label>
            </div>

            <div class="form-floating mb-3">
              <input type="date" class="form-control" id="InputValue_Deadline" v-model="deadline">
              <label for="InputValue_Deadline">Deadline</label>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button @click="submitForm" type="button" class="btn btn-success" data-bs-dismiss="modal">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    showModal: Boolean,
    roleName: String,
  },

  data() {
    return {
      roleName: '',
      roleDesc: '',
      skillReq: '',
      deadline: '',
      skills: [],
    };
  },

  methods: {
    closeModal() {
      this.$emit('close');
    },

    async fetchRoleSkillData() {
      try {
        const response = await axios.get('http://localhost:8080/get_roleskill_data');
        const roleSkillData = response.data;

        const uniqueSkills = new Set();
        this.skills = roleSkillData.filter((roleSkill) => {
          if (!uniqueSkills.has(roleSkill.Skill_Name)) {
            uniqueSkills.add(roleSkill.Skill_Name);
            return true;
          }
          return false;
        });
      } catch (error) {
        console.error(error);
      }
    },

    submitForm() {
      const data = {
        roleName: this.roleName,
        roleDesc: this.roleDesc,
        skillReq: this.skillReq,
        deadline: this.deadline,
      };

      // Send PUT request to API endpoint
      axios.put('api_endpoint_here', data)
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });

      this.$emit('close');
    },
  },

  created() {
    this.fetchRoleSkillData();
  },
};
</script>

<style scoped>
.modal {
  display: block;
}

.modal-content {
  display: flex;
}
</style>
