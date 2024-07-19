<template>
  <div class="container">
    <div class="signin-wrapper">
      <div class="welcome-back">Create Account</div>
      <div class="header">Sign Up</div>
      <div class="form-wrapper">
        <!-- 表单项 -->
        <div class="form-group" :class="{ 'focused': isNameFocused || name, 'error': nameError }">
          <label for="name" class="form-label">Name <span v-if="nameError" class="error-message">- Name is required</span></label>
          <input type="text" id="name" name="name" class="input-item" v-model="name" @focus="handleFocus('name')" @blur="handleBlur('name')" @input="validateName" autocomplete="off">
        </div>
        <div class="form-group" :class="{ 'focused': isPhoneFocused || phone, 'error': phoneError || phoneExists }">
          <label for="phone" class="form-label">Phone <span v-if="phoneError" class="error-message">- Must be 11 digits</span><span v-if="phoneExists" class="error-message">- Phone number already exists</span></label>
          <input type="tel" id="phone" name="phone" class="input-item" v-model="phone" @focus="handleFocus('phone')" @blur="handleBlur('phone')" @input="validatePhone" autocomplete="off">
        </div>
        <div class="form-group" :class="{ 'focused': isPasswordFocused || password, 'error': passwordError }">
          <label for="password" class="form-label">Password <span v-if="passwordError" class="error-message">- Must be 8-14 characters</span></label>
          <input type="password" id="password" name="new-password" class="input-item" v-model="password" @focus="handleFocus('password')" @blur="handleBlur('password')" @input="validatePassword" autocomplete="new-password">
        </div>
        <div class="form-group" :class="{ 'focused': isConfirmPasswordFocused || confirmPassword, 'error': confirmPasswordError }">
          <label for="confirm-password" class="form-label">Confirm Password <span v-if="confirmPasswordError" class="error-message">- Passwords do not match</span></label>
          <input type="password" id="confirm-password" name="confirm-password" class="input-item" v-model="confirmPassword" @focus="handleFocus('confirm-password')" @blur="handleBlur('confirm-password')" @input="validateConfirmPassword" autocomplete="new-password">
        </div>
        <div class="form-group" :class="{ 'focused': isIdNumberFocused || idNumber, 'error': idNumberError || idNumberExists }">
          <label for="id-number" class="form-label">ID Number <span v-if="idNumberError" class="error-message">- Must be 18 digits</span><span v-if="idNumberExists" class="error-message">- ID number already exists</span></label>
          <input type="text" id="id-number" name="id-number" class="input-item" v-model="idNumber" @focus="handleFocus('id-number')" @blur="handleBlur('id-number')" @input="validateIdNumber" autocomplete="off">
        </div>
        <div class="form-group" :class="{ 'focused': isGenderFocused || gender, 'error': genderError }">
          <label for="gender" class="form-label">Gender <span v-if="genderError" class="error-message">- Please select a gender</span></label>
          <select id="gender" name="gender" class="input-item" v-model="gender" @focus="handleFocus('gender')" @blur="handleBlur('gender')" @change="validateGender">
            <option value="" disabled></option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div class="form-group" :class="{ 'focused': isAgeFocused || age, 'error': ageError }">
          <label for="age" class="form-label">Age <span v-if="ageError" class="error-message">- Must be a valid number</span></label>
          <input type="number" id="age" name="age" class="input-item" v-model="age" @focus="handleFocus('age')" @blur="handleBlur('age')" @input="validateAge" autocomplete="off">
        </div>
        <div class="btn" @click="signin">Sign Up</div>
        <div class="btn btn-secondary" @click="goToLogin">Back to Login</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Signin",
  data() {
    return {
      name: '',
      phone: '',
      password: '',
      confirmPassword: '',
      idNumber: '',
      gender: '',
      age: '',
      isNameFocused: false,
      isPhoneFocused: false,
      isPasswordFocused: false,
      isConfirmPasswordFocused: false,
      isIdNumberFocused: false,
      isGenderFocused: false,
      isAgeFocused: false,
      nameError: false,
      phoneError: false,
      passwordError: false,
      confirmPasswordError: false,
      idNumberError: false,
      genderError: false,
      ageError: false,
      idNumberExists: false,
      phoneExists: false,
      nameTouched: false,
      phoneTouched: false,
      passwordTouched: false,
      confirmPasswordTouched: false,
      idNumberTouched: false,
      genderTouched: false,
      ageTouched: false,
    };
  },
  methods: {
    handleFocus(field) {
      if (field === 'name') {
        this.isNameFocused = true;
        this.nameError = false;
        this.nameTouched = true;
      } else if (field === 'phone') {
        this.isPhoneFocused = true;
        this.phoneError = false;
        this.phoneExists = false;
        this.phoneTouched = true;
      } else if (field === 'password') {
        this.isPasswordFocused = true;
        this.passwordError = false;
        this.passwordTouched = true;
      } else if (field === 'confirm-password') {
        this.isConfirmPasswordFocused = true;
        this.confirmPasswordError = false;
        this.confirmPasswordTouched = true;
      } else if (field === 'id-number') {
        this.isIdNumberFocused = true;
        this.idNumberError = false;
        this.idNumberExists = false;
        this.idNumberTouched = true;
      } else if (field === 'gender') {
        this.isGenderFocused = true;
        this.genderError = false;
        this.genderTouched = true;
      } else if (field === 'age') {
        this.isAgeFocused = true;
        this.ageError = false;
        this.ageTouched = true;
      }
    },
    handleBlur(field) {
      if (field === 'name') {
        this.isNameFocused = false;
        this.validateName();
      } else if (field === 'phone') {
        this.isPhoneFocused = false;
        this.validatePhone();
      } else if (field === 'password') {
        this.isPasswordFocused = false;
        this.validatePassword();
      } else if (field === 'confirm-password') {
        this.isConfirmPasswordFocused = false;
        this.validateConfirmPassword();
      } else if (field === 'id-number') {
        this.isIdNumberFocused = false;
        this.validateIdNumber();
      } else if (field === 'gender') {
        this.isGenderFocused = false;
        this.validateGender();
      } else if (field === 'age') {
        this.isAgeFocused = false;
        this.validateAge();
      }
    },
    validateName() {
      this.nameError = !this.name;
    },
    validatePhone() {
      const re = /^[0-9]{11}$/; 
      this.phoneError = !re.test(this.phone);
    },
    validatePassword() {
      this.passwordError = this.password.length < 8 || this.password.length > 14 || /\s/.test(this.password);
    },
    validateConfirmPassword() {
      this.confirmPasswordError = this.password !== this.confirmPassword;
    },
    validateIdNumber() {
      const re = /^[0-9]{18}$/; 
      this.idNumberError = !re.test(this.idNumber);
    },
    validateGender() {
      this.genderError = !this.gender;
    },
    validateAge() {
      this.ageError = isNaN(this.age) || this.age <= 0;
    },
    async signin() {
      this.validateName();
      this.validatePhone();
      this.validatePassword();
      this.validateConfirmPassword();
      this.validateIdNumber();
      this.validateGender();
      this.validateAge();
      if (this.nameError || this.phoneError || this.passwordError || this.confirmPasswordError || this.idNumberError || this.genderError || this.ageError) {
        return;
      }
      const phoneExists = await this.checkPhoneInDatabase(this.phone);
      if (phoneExists) {
        this.phoneExists = true;
        return;
      }
      const idExists = await this.checkIdNumberInDatabase(this.idNumber);
      if (idExists) {
        this.idNumberExists = true;
        return;
      }
      console.log('Sending registration request:', { name: this.name, phone: this.phone, password: this.password, idNumber: this.idNumber, gender: this.gender, age: this.age }); // 添加日志记录
      const success = await this.saveUserToDatabase(this.name, this.phone, this.password, this.idNumber, this.gender, this.age);
      if (success) {
        alert(`Account created successfully: Name: ${this.name}, Phone: ${this.phone}, Password: ${this.password}`);
        this.$router.push({ name: 'LoginPage' }); 
      } else {
        alert("Failed to create account. Please try again.");
      }
    },
    async checkPhoneInDatabase(phone) {
      try {
        const response = await axios.post('/api/check-phone', { phone });
        return response.data.exists;
      } catch (error) {
        console.error('Failed to check phone number:', error);
        return false;
      }
    },
    async checkIdNumberInDatabase(idNumber) {
      try {
        const response = await axios.post('/api/check-id', { idNumber });
        return response.data.exists;
      } catch (error) {
        console.error('Failed to check ID number:', error);
        return false;
      }
    },
    async saveUserToDatabase(name, phone, password, idNumber, gender, age) {
      try {
        console.log('Sending registration request:', { name, phone, password, idNumber, gender, age });
        const response = await axios.post('/api/register', { name, phone, password, idNumber, gender, age });
        console.log('Received response from server:', response.data); 
        return response.data.success;
      } catch (error) {
        console.error('Failed to save user:', error);
        return false;
      }
    },
    goToLogin() {
      this.$router.push({ name: 'LoginPage' }); // 跳转到登录页面
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
.signin-wrapper {
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
.form-group.error .form-label,
.form-group.error .input-item {
  color: #e74c3c;
  border-color: #e74c3c;
}
.error-message {
  color: #e74c3c;
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
.btn-secondary {
  background-color: #ccc;
  margin-top: 10px;
}
.btn:hover {
  background-color: #249e61;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}
</style>
