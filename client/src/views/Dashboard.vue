<template>
  <div class="container">
    <div class="dashboard-container">
      <h1>Dashboard</h1>
      <div class="selection-wrapper">
        <div class="selection-item" @click="goToPersonalInfo">Personal Information</div>
        <div class="selection-item" @click="goToRegistration">Registration</div>
      </div>
      <div class="logout-button" @click="logout">Logout</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  methods: {
    goToPersonalInfo() {
      this.$router.push({ name: 'PersonalInfoPage' });
    },
    goToRegistration() {
      this.$router.push({ name: 'Registration' });
    },
    logout() {
      localStorage.removeItem('isLoggedIn');
      this.$router.push({ name: 'LoginPage' });
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.dashboard-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: scale(1.2);
  font-family: Arial, sans-serif;
}
h1 {
  font-size: 36px;
  margin-bottom: 40px;
}
.selection-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.selection-item {
  padding: 20px 40px;
  border: 1px solid #2eb67d;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  font-size: 18px;
  transition: background-color 0.3s ease;
}
.selection-item:hover {
  background-color: #2eb67d;
  color: #fff;
}
.logout-button {
  margin-top: 40px;
  padding: 10px 20px;
  border: 1px solid #e74c3c;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  font-size: 18px;
  transition: background-color 0.3s ease;
}
.logout-button:hover {
  background-color: #e74c3c;
  color: #fff;
}
</style>
