<template>
  <nav>
    <router-link to="/deposit">deposit</router-link> |
    <router-link to="/withdraw">withdraw</router-link> |
    <router-link to="/payBill">payBill</router-link> |
    <router-link to="/buyAirtime">buyairtime</router-link> |
    <router-link to="/transfer">transfer</router-link> |
    <router-link to="/balance">balance</router-link> |
    <router-link to="/transaction-history">transactionHistory</router-link> |
    <a href="#" @click="logout">logout</a> 

  </nav>
  <router-view/>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script>
import axios from 'axios';

export default {
  methods: {
    async logout() {
      try {
        // Get the access token from localStorage
        const token = localStorage.getItem('access_token');

        // Call the server-side logout API with the token
        await axios.post('http://127.0.0.1:8000/api/logout/', {}, {
          headers: {
            'Authorization': `Bearer ${token}`, // Send the token in the Authorization header
          }
        });
        
        // Remove the access token from localStorage
        localStorage.removeItem('access_token');
        
        // Redirect to the login page
        this.$router.push('/login');
      } catch (error) {
        console.error("Error logging out:", error);
        // Always redirect to login even if there's an error
        this.$router.push('/login');
      }
    }
  }
};
</script>