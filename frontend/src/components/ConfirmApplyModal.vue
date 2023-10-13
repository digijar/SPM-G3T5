<template>
    <div class="modal" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Application Form</h5>
            <button @click="closeModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>Fill in the following details:</p>
            <form class="form-floating mb-3">
            <input type="text" class="form-control" id="InputValue_StaffID" placeholder="" v-model="staffId" @input="validateStaffId" :class="{ 'is-invalid': staffIdError }">
            <label for="InputValue_StaffID">Your Staff ID</label>
            <div class="invalid-feedback" v-if="staffIdError">{{ staffIdError }}</div>
            </form>
            <form class="form-floating">
            <input type="text" class="form-control" id="InputValue_Dept" placeholder="" v-model="currDept" @input="validateDepartment" :class="{ 'is-invalid': deptError }">
            <label for="InputValue_Dept">Your Current Department</label>
            <div class="invalid-feedback" v-if="deptError">{{ deptError }}</div>
            </form>
          </div>
          <div class="modal-footer">
            <button @click="closeModal" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button @click="confirmApply" type="button" class="btn btn-success" data-bs-dismiss="modal">Apply</button>
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
    
    created() {
      this.fetchStaffData();
    },

    data() {
      return {
        staffId: '',
        staffIdError: '', 
        currDept: '',
        deptError: '',
        testDepts: ['1', '2', '3', '4'],
        allDepts: [],
      };
    },

    methods: {
      closeModal() {
        this.$emit('close');
      },

      confirmApply() {
        this.$emit('close');
        alert("You have successfully applied for the role of " + this.roleName);
      },

    validateStaffId() {
        // console.log('Validating staff ID:', this.staffId);
        const regex = /^\d{6}$/;
        if (!regex.test(this.staffId)) {
            // console.log('Invalid staff ID');
            this.staffIdError = 'Staff ID must be 6 digits';
        } else {
            // console.log('Valid staff ID');
            this.staffIdError = '';
            }
        },
    
    validateDepartment() {
        // console.log('Validating department:', this.currDept);
        if (!this.allDepts.includes(this.currDept)) {
            // console.log('Invalid department');
            this.deptError = 'Department does not exist';
        } else {
            // console.log('Valid department');
            this.deptError = '';
            }
        },
    
    fetchStaffData() {
        axios.get('http://localhost:8000/get_staff_data')
            .then(response => {
                // console.log(response.data[0].Dept);
                this.staffData = response.data;
                this.getUniqueDepts();
            })
            .catch(error => {
                console.error(error);
            });
        },

        getUniqueDepts() {
          this.staffData.forEach(staff => {
            if (!this.allDepts.includes(staff.Dept)) {
              this.allDepts.push(staff.Dept);
            }            
          });
          console.log(this.allDepts)
        },

    selectDept(dept) {
        this.selectedDept = dept;
        console.log('Selected dept:', dept);
        }
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
  