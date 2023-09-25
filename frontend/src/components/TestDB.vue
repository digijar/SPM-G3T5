<template>
    <div>
    <button @click="fetchData">Fetch Data</button>
    <table>
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
        </tr>
        </tbody>
    </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
    return {
        staffData: [],
    };
    },
    methods: {
    fetchData() {
        axios.get('http://localhost:8000/get_staff_data') // Adjust the URL to your Flask route
        .then(response => {
            this.staffData = response.data;
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