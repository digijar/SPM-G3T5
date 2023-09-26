<template>
    <div>
        <div class="container">
            <h1>Staff Data</h1>
            <hr>

            <!-- Add a modal for editing staff data -->
            <div class="modal fade" id="editStaffModal" tabindex="-1" aria-labelledby="editStaffModalLabel" aria-hidden="true" v-if="isEditing">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="editStaffModalLabel">Edit Staff Data</h5>
                            <button type="button" class="btn-close" @click="cancelEdit" data-bs-dismiss="modal"  aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <!-- Create a form for editing staff data -->
                            <form @submit.prevent="saveEditedStaff">
                                <div class="form-group">
                                    <label for="editFName">First Name</label>
                                    <input type="text" v-model="editedStaff.Staff_FName" class="form-control" id="editFName">
                                </div>

                                <div class="form-group">
                                    <label for="editLName">Last Name</label>
                                    <input type="text" v-model="editedStaff.Staff_LName" class="form-control" id="editLName">
                                </div>

                                <div class="form-group">
                                    <label for="editDept">Dept</label>
                                    <input type="text" v-model="editedStaff.Dept" class="form-control" id="editDept">
                                </div>

                                <div class="form-group">
                                    <label for="editCountry">Country</label>
                                    <input type="text" v-model="editedStaff.Country" class="form-control" id="editCountry">
                                </div>

                                <div class="form-group">
                                    <label for="editEmail">Email</label>
                                    <input type="text" v-model="editedStaff.Email" class="form-control" id="editEmail">
                                </div>

                                <div class="form-group">
                                    <label for="editRole">Role</label>
                                    <input type="number" v-model="editedStaff.Role" class="form-control" id="editRole">
                                </div>

                                <button type="submit" class="btn btn-primary">Save</button>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>

            <button @click="fetchStaffData" class="btn btn-info">Fetch Staff Data</button>
            <table class="table">
                <thead>
                    <tr>
                        <th>Staff ID</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Dept</th>
                        <th>Country</th>
                        <th>Email</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="staff in staffData" :key="staff.Staff_ID">
                        <td>{{ staff.Staff_ID }}</td>
                        <td>{{ staff.Staff_FName }}</td>
                        <td>{{ staff.Staff_LName }}</td>
                        <td>{{ staff.Dept }}</td>
                        <td>{{ staff.Country }}</td>
                        <td>{{ staff.Email }}</td>
                        <td>{{ staff.Role }}</td>
                        <td>
                            <button @click="editStaffData(staff)" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editStaffModal">Edit</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <hr>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            staffData: [],
            editedStaff: null,
            isEditing: false, // Add a property to control the modal visibility
        };
    },
    methods: {
        fetchStaffData() {
            axios.get('http://localhost:8000/get_staff_data')
                .then(response => {
                    this.staffData = response.data;
                })
                .catch(error => {
                    console.error(error);
                });
        },

        editStaffData(staff) {
            console.log("opening modal");
            console.log(staff);
            this.editedStaff = staff; // Clone the staff object to avoid modifying the original data
            this.isEditing = true; // Show the modal when editing
        },

        // Add a method to cancel the edit and close the modal or form
        cancelEdit() {
            this.editedStaff = null;
            this.isEditing = false; // Close the modal
        },

        saveEditedStaff() {
            // Send the editedStaff object to the backend to update the data
            axios.put('http://localhost:8000/edit_staff_data', this.editedStaff)
                .then(response => {
                    // Handle success and update the staffData with the edited data
                    this.fetchStaffData();
                    // Close the modal or form
                    this.editedStaff = null;
                    this.isEditing = false;
                })
                .catch(error => {
                    console.error(error);
                });
        },
    },
};
</script>

<style scoped>
/* Add your CSS styles here */
</style>
