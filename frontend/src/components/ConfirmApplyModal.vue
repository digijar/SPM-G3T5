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
            <p>Name: <b>{{ staffName }}</b></p>
            <p>Current Department: <b>{{ currDept }}</b></p>
            <p>Percentage of Skills Matched: <b>{{ roleSkillPercent }}</b></p>
            <p style="color: red;">Missing Skills:</p>
            <ul>
              <li v-for="(skill, index) in staff_roleSkills.Missing_Skills" :key="index">
                {{ skill }}
              </li>
            </ul>

            <p style="color: green;">Skills that you have:</p>
            <ul>
              <li v-for="(skill, index) in staff_roleSkills.Common_Skills" :key="index">
                {{ skill }}
              </li>
            </ul>
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
      this.fetchApplicationData();
    },

    data() {
      return {
        staffId: '',
        staffName: '',
        staffIdError: '', 
        currDept: '',
        allDepts: [],
        staffIdData: {},
        roleSkillPercent: '',
        staff_roleSkills: [],
        existingApplications: [],
      };
    },

    methods: {
      closeModal() {
        this.$emit('close');
        this.staffId = '';
        this.staffName = '';
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
                for (let application of this.existingApplications) {
                    // console.log(application.Role_Name + application.Staff_ID)
                    if (application.Role_Name == this.roleName && application.Staff_ID == this.staffId) {
                        alert("Submission failed. You have already applied for this role.");
                        return;
                    }
                    else {
                        continue;
                    }
                }
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
            // console.log('Invalid staff ID');
            this.staffIdError = 'Staff ID must be 6 digits';
        } else {
            this.fetchStaffIdData(this.staffId)
            }
        },
      
      fetchStaffIdData() {
        // console.log('Fetching staff data for staff ID:', this.staffId);
        axios.get('http://localhost:8000/get_staff_data_by_id/' + this.staffId)
            .then(response => {
                // console.log(response.data);
                if (response.data.error) {
                    this.staffIdError = 'Staff ID does not exist';
                    this.staffIdData = {};
                    this.currDept = '';
                } else {
                    this.staffIdError = '';
                    this.staffIdData = response.data;
                    this.staffName = this.staffIdData.Staff_FName + " " + this.staffIdData.Staff_LName;
                    this.currDept = this.staffIdData.Dept;
                    this.getSkillMatchPercentage();
                    this.getMissingSkills();
                }
            })
            .catch(error => {
              console.error(error);
            });
        },
      
      getSkillMatchPercentage() {
        // console.log('Fetching Skill Match Percentage for role:', this.roleName, 'and staff ID:', this.staffId);
        axios.get(`http://localhost:8000/get_skill_match/${this.roleName}/${this.staffId}`)
            .then(response => {
                // console.log(response.data);
                // this.roleSkillPercent = parseFloat(response.data.Match_Percentage).toFixed(2);
                const matchPercentage = parseFloat(response.data.Match_Percentage);
                this.roleSkillPercent = isNaN(matchPercentage) ? 0 : matchPercentage.toFixed(2);
            })
            .catch(error => {
              console.error(error);
            });
      },

      getMissingSkills() {
        // console.log('Getting missing skills for:', this.roleName, 'and staff ID:', this.staffId);
        axios.get(`http://localhost:8000/get_missing_skills/${this.roleName}/${this.staffId}`)
            .then(response => {
                // console.log(response.data);
                this.staff_roleSkills = response.data;
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
          this.staffName = '';
        })
        .catch(error => {
          console.error('Error submitting data:', error);
        });
    },
      
    fetchApplicationData() {
        axios.get('http://localhost:8000/get_applications_data')
            .then(response => {
                // console.log(response.data);
                this.existingApplications = response.data;
                // for (let application of this.existingApplications) {
                //     console.log(application.Role_Name + application.Staff_ID);
                // }
            })
            .catch(error => {
                console.error(error);
            });
        },
      }

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
  