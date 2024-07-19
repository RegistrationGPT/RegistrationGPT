<template>
  <div>
    <section>
      <img src="@/assets/bg.jpg" alt="" id="bg">
      <img src="@/assets/moon.png" alt="" id="moon">
      <img src="@/assets/mountain.png" alt="" id="mountain">
      <img src="@/assets/road.png" alt="" id="road">

      <h2 id="text">Smart Registration     Application</h2>
      <button @click="goToLoginPage" class="start-button">Start</button>
    </section>
  
    <div class="introduction">
      <h3>Introduction</h3>
      <div class="intro-section">
        <p>
          Welcome to our Smart Registration System! This innovative application leverages the power of machine learning and advanced image processing to assist users with their healthcare needs.
        </p>
      </div>
      <div class="intro-section">
        <p>
          By providing linguistic information and uploading medical images, users can receive a preliminary diagnosis of their condition. Our system analyzes the input to give users an insight into their health status before they visit a doctor.
        </p>
      </div>
      <div class="intro-section">
        <p>
          After the preliminary diagnosis, the system helps users to book an appointment with the appropriate specialist. This seamless process ensures that users can quickly and efficiently get the medical attention they need.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {};
  },
  methods: {
    goToLoginPage() {
      this.$router.push({ name: 'LoginPage' });
    }
  },
  mounted() {
    let bg = document.getElementById('bg');
    let moon = document.getElementById('moon');
    let mountain = document.getElementById('mountain');
    let road = document.getElementById('road');
    let text = document.getElementById('text');
    let button = document.querySelector('.start-button');
    window.addEventListener('scroll', function () {
      let value = window.scrollY;
      bg.style.top = value + 0.5 + 'px';
      moon.style.left = -value + 0.5 + 'px';
      mountain.style.top = -value * 0.15 + 'px';
      road.style.top = value * 0.15 + 'px';
      text.style.opacity = 1 - value / 500;
      button.style.opacity = 1 - value / 500;
    });
  }
};
</script>

<style scoped>
body, html {
  height: 100%;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Arial, sans-serif;
  background-color: #350124;
  padding: 0;
  min-height: 1500px;
}

section {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

section::before {
  content: '';
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100px;
  background: linear-gradient(to top, #350124, transparent);
  z-index: 10000;
}

section::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #350124;
  mix-blend-mode: color;
  z-index: 10000;
}

section img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}

#text {
  position: relative;
  z-index: 1;
  color: #fff;
  font-size: 8vw;
  top: -150px;
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  transition: opacity 0.5s;
}

.start-button {
  position: absolute;
  bottom: 150px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 2em;
  padding: 15px 30px;
  cursor: pointer;
  border: none;
  background-color: #fff;
  color: #8b0000;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s, box-shadow 0.3s, opacity 0.5s;
  z-index: 10001;
}

.start-button:hover {
  background-color: #e68900;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.introduction {
  padding: 20px;
  background-color: #350124;
  color: #fff;
  text-align: center;
  font-size: 2em;
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-top: -200px;
}

.intro-section {
  margin: 20px 0;
  background: rgba(255, 255, 255, 0.1); 
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.intro-section p {
  font-size: 1.2em;
  font-weight: normal;
  color: #d1d1d1; 
}
</style>
