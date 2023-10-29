<template>
    <div class="modal" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Applying for: <b>{{ roleName }}</b></h5>
            <button @click="closeModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>Fill in the following details:</p>
            <form class="form-floating mb-3">
            <input type="text" class="form-control" id="InputValue_StaffID" placeholder="" v-model="staffId" @input="validateStaffId" :class="{ 'is-invalid': staffIdError }">
            <label for="InputValue_StaffID">Your Staff ID</label>
            <div class="invalid-feedback" v-if="staffIdError">{{ staffIdError }}</div>
            </form>
            <p>Current Department: <b>{{ currDept }}</b></p>
            <p>Percentage of Skills Matched: <b>{{ roleSkillPercent }}</b></p>
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
      // this.fetchStaffData();
    },

    data() {
      return {
        staffId: '',
        staffIdError: '', 
        currDept: '',
        allDepts: [],
        staffIdData: {},
        roleSkillPercent: '',
      };
    },

    methods: {
      closeModal() {
        this.$emit('close');
        this.staffId = '';
        this.currDept = '';
        this.roleSkillPercent = '';
      },

      confirmApply() {
        if (this.staffIdError) {
          alert("Please fix error in the required field(s)");
          return;
        }
        else {
            if (this.staffId == '') {
                alert("Please fill in the required field(s)");
                return;
            }
            else {
                alert("You have successfully applied for the role of " + this.roleName);
                this.submitApplication();
                this.$emit('close');
            }
        }
      },

    validateStaffId() {
        // console.log('Validating staff ID:', this.staffId);
        const regex = /^\d{6}$/;
        if (!regex.test(this.staffId)) {
            console.log('Invalid staff ID');
            this.staffIdError = 'Staff ID must be 6 digits';
        } else {
            this.fetchStaffIdData(this.staffId)
            }
        },
      
      fetchStaffIdData() {
        // console.log('Fetching staff data for staff ID:', this.staffId);
        axios.get('http://localhost:8000/get_staff_data_by_id/' + this.staffId)
            .then(response => {
                console.log(response.data);
                if (response.data.error) {
                    this.staffIdError = 'Staff ID does not exist';
                    this.staffIdData = {};
                    this.currDept = '';
                } else {
                    this.staffIdError = '';
                    this.staffIdData = response.data;
                    this.currDept = this.staffIdData.Dept;
                    this.getSkillMatchPercentage();
                }
            })
            .catch(error => {
              console.error(error);
            });
        },
      
      getSkillMatchPercentage() {
        console.log('Fetching Skill Match Percentage for role:', this.roleName, 'and staff ID:', this.staffId);
        axios.get(`http://localhost:8000/get_skill_match/${this.roleName}/${this.staffId}`)
            .then(response => {
                console.log(response.data);
                this.roleSkillPercent = parseFloat(response.data.Match_Percentage).toFixed(2);
            })
            .catch(error => {
              console.error(error);
            });
      },

    submitApplication() {
      // Prepare the data for submission
      const formData = {
        role_name: this.roleName,
        staff_id: this.staffId,
        current_dept: this.currDept,
        skill_match: this.roleSkillPercent,
      };

      // Send the data to the backend using the appropriate API endpoint
      axios.post('http://localhost:8000/create_new_application', formData)
        .then(response => {
          console.log('Data submitted successfully:', response.data);
          // Reset form fields after successful submission if needed
          this.roleName = '';
          this.staffId = '';
          this.currDept = '';
          this.skill_match = '';
        })
        .catch(error => {
          console.error('Error submitting data:', error);
        });
    },
      
      }
    
    // validateDepartment() {
    //     // console.log('Validating department:', this.currDept);
    //     if (!this.allDepts.includes(this.currDept)) {
    //         // console.log('Invalid department');
    //         this.deptError = 'Department does not exist!';
    //     } else {
    //         // console.log('Valid department');
    //         this.deptError = '';
    //         }
    //     },
    
    // fetchStaffData() {
    //     axios.get('http://localhost:8000/get_staff_data')
    //         .then(response => {
    //             // console.log(response.data[0].Dept);
    //             this.staffData = response.data;
    //             this.getUniqueDepts();
    //         })
    //         .catch(error => {
    //             console.error(error);
    //         });
    //     },

    //     getUniqueDepts() {
    //       this.staffData.forEach(staff => {
    //         if (!this.allDepts.includes(staff.Dept)) {
    //           this.allDepts.push(staff.Dept);
    //         }            
    //       });
    //       // console.log(this.allDepts)
    //     },    
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
  