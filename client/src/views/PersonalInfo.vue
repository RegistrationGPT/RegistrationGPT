<template>
  <div class="container">
    <div class="personal-info-container">
      <h1>Personal Information</h1>
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="personalInfo.name" class="form-control" readonly>
      </div>
      <div class="form-group">
        <label for="age">Age</label>
        <input type="number" id="age" v-model="personalInfo.age" class="form-control" readonly>
      </div>
      <div class="form-group">
        <label for="gender">Gender</label>
        <select id="gender" v-model="personalInfo.gender" class="form-control" disabled>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>
      <div class="form-group">
        <label for="phone">Phone</label>
        <input type="tel" id="phone" v-model="personalInfo.phone" class="form-control" readonly>
      </div>
      <div class="form-group">
        <label for="idNumber">ID Number</label>
        <input type="text" id="idNumber" v-model="personalInfo.idNumber" class="form-control" readonly>
      </div>
      <div class="form-group">
        <label for="medicalHistory">Medical History</label>
        <textarea id="medicalHistory" v-model="personalInfo.medicalHistory" class="form-control" readonly></textarea>
      </div>
      <div class="back-button" @click="goBack">Back to Dashboard</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PersonalInfo',
  data() {
    return {
      personalInfo: {
        name: '',
        age: '',
        gender: '',
        phone: '',
        idNumber: '',
        medicalHistory: ''
      }
    };
  },
  methods: {
    async fetchPersonalInfo() {
      try {
        const phone = localStorage.getItem('userPhone');
        const response = await axios.get(`api/user/${phone}`);
        if (response.data.success) {
          this.personalInfo = response.data.data;
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        console.error('Error fetching personal info:', error);
      }
    },
    goBack() {
      this.$router.push({ name: 'DashboardPage' });
    }
  },
  mounted() {
    this.fetchPersonalInfo(); 
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.personal-info-container {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
}
h1 {
  font-size: 36px;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 15px;
}
.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f8f8f8; 
}
.back-button {
  margin-top: 20px;
  padding: 10px;
  background-color: #dc3545;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  cursor: pointer;
}
.back-button:hover {
  background-color: #c82333;
}
</style>
