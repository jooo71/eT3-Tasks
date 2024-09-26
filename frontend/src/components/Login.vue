<template>
  <div>
    <form @submit.prevent="login">
      <input v-model="phone_number" type="text" placeholder="Phone Number" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
    <div v-if="error">{{ error }}</div>
  </div>
</template>

<script>
import api from '@/api.js';

export default {
  data() {
    return {
      phone_number: '',
      password: '',
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await api.post('/login/', {
          phone_number: this.phone_number,
          password: this.password,
        });

        // Save the access token
        localStorage.setItem('access_token', response.data.access);
        this.$router.push('/dashboard'); // Redirect to a protected route
      } catch (err) {
        this.error = 'Invalid credentials';
      }
    }
  }
};
</script>