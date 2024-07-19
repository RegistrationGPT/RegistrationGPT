<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  created() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
      if (!isLoggedIn && this.$route.meta.requiresAuth) {
        this.$router.push({ name: 'LoginPage' });
      }
    }
  },
  watch: {
    $route() {
      this.checkLoginStatus();
    }
  }
};
</script>
