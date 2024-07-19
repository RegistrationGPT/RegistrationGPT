<template>
  <div class="container">
    <div class="login-wrapper">
      <div class="welcome-back">Welcome Back</div>
      <div class="header">Login</div>
      <div class="form-wrapper">
        <div class="form-group" :class="{ 'focused': isPhoneFocused || phone }">
          <label for="phone" class="form-label">Phone</label>
          <input type="tel" id="phone" name="phone" class="input-item" v-model="phone" @focus="clearError('phone')" @blur="handleBlur('phone')" @input="clearError('phone')" autocomplete="off">
          <div v-if="phoneError" class="tooltip">Invalid phone format</div>
        </div>
        <div class="form-group" :class="{ 'focused': isPasswordFocused || password }">
          <label for="password" class="form-label">Password</label>
          <input type="password" id="password" name="new-password" class="input-item" v-model="password" @focus="clearError('password')" @blur="handleBlur('password')" @input="clearError('password')" autocomplete="new-password">
          <div v-if="passwordError && passwordTouched" class="tooltip">Invalid password</div>
        </div>
        <div class="btn" @click="login">Login</div>
        <div class="btn" @click="goToSignin">Sign Up</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Login",
  data() {
    return {
      phone: '',
      password: '',
      isPhoneFocused: false,
      isPasswordFocused: false,
      phoneError: false,
      passwordError: false,
      passwordTouched: false
    };
  },
  methods: {
    handleBlur(field) {
      if (field === 'phone') {
        this.isPhoneFocused = false;
        this.phoneError = !this.validatePhone(this.phone);
      } else if (field === 'password') {
        this.isPasswordFocused = false;
      }
    },
    validatePhone(phone) {
      const re = /^[0-9]{10,11}$/; 
      return re.test(phone);
    },
    validatePassword(password) {
      return password.length >= 6; 
    },
    clearError(field) {
      if (field === 'phone') {
        this.isPhoneFocused = true;
        this.phoneError = false;
      } else if (field === 'password') {
        this.isPasswordFocused = true;
        this.passwordError = false;
      }
    },
    async login() {
      this.phoneError = !this.validatePhone(this.phone);
      this.passwordError = !this.validatePassword(this.password);
      this.passwordTouched = true;
      if (this.phoneError || this.passwordError) {
        return;
      }
      const userExists = await this.checkUserInDatabase(this.phone, this.password);
      if (userExists) {
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('userPhone', this.phone); 
        this.$router.push({ name: 'DashboardPage' });
      } else {
        alert("User does not exist or incorrect password");
      }
    },
    async checkUserInDatabase(phone, password) {
      try {
        const response = await axios.post('/api/login', { phone, password });
        console.log('111');
        console.log(response);
        return response.data.success;
      } catch (error) {
        console.error('Error checking user in database:', error);
        return false;
      }
    },
    goToSignin() {
      this.$router.push({ name: 'Signin' });
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body {
  height: 100%;
  margin: 0;
  font-family: Arial, sans-serif;
}
.container {
  display: flex;
  align-items: flex-start; 
  justify-content: center;
  height: 100%;
  background: #fff;
  padding-top: 100px; 
  transform: scale(1.2); 
}
.login-wrapper {
  background-color: #fff;
  width: 100%;
  max-width: 600px; 
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
}
.welcome-back {
  font-family: 'Poppins', sans-serif;
  font-size: 24px;
  font-weight: 300;
  text-align: center;
  margin-bottom: 10px;
  color: #666;
}
.header {
  font-family: 'Poppins', sans-serif;
  font-size: 38px;
  font-weight: 700;
  text-align: center;
  margin-top: 10px;
  color: #333;
}
.form-wrapper {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}
.form-group {
  position: relative;
  margin-bottom: 30px; 
}
.form-label {
  position: absolute;
  top: 20px;
  left: 10px;
  color: rgb(128, 125, 125);
  transition: all 0.2s ease;
  background: white;
  padding: 0 5px;
  font-size: 25px; 
}
.input-item {
  display: block;
  width: 100%;
  border: 1px solid rgb(128, 125, 125); 
  padding: 20px; 
  border-radius: 8px; 
  font-size: 20px; 
  outline: none;
  transition: border-color 0.2s ease; 
}
.form-group.focused .form-label,
.form-group .input-item:not(:placeholder-shown) + .form-label {
  top: -15px;
  font-size: 16px;
  color: #2eb67d;
}
.input-item:focus {
  border-color: #2eb67d; 
}
.tooltip {
  position: absolute;
  top: 50%;
  left: calc(100% + 10px); 
  transform: translateY(-50%);
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  padding: 10px;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
  white-space: nowrap;
  z-index: 1000; 
}
.btn {
  text-align: center;
  padding: 20px; 
  margin: 0 auto;
  width: 100%;
  margin-top: 20px;
  background-color: #2eb67d; 
  color: #fff;
  border: none;
  border-radius: 8px; 
  cursor: pointer;
  font-size: 20px; 
  transition: background-color 0.3s ease, box-shadow 0.3s ease; 
  font-family: 'Poppins', sans-serif; 
}
.btn:hover {
  background-color: #249e61; 
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15); 
}
</style>
