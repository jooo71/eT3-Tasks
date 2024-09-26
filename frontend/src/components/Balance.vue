<template>
    <div>
      <h2>Check Balance</h2>
      <button @click="getBalance">Check Balance</button>
  
      <!-- Success or error messages -->
      <div v-if="balanceMessage" class="balance-message">
        {{ balanceMessage }}
      </div>
      <div v-if="errorMessage" class="error">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import api from "@/api"; // Ensure you've set up the axios instance in api.js
  
  export default {
    data() {
      return {
        balanceMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async getBalance() {
        try {
          // Clear previous messages
          this.balanceMessage = null;
          this.errorMessage = null;
  
          // Make GET request to the balance API
          const response = await api.get("/balance/");
  
          // Handle successful response
          this.balanceMessage = response.data.message;
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while fetching the balance.";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Simple styles for form and messages */
  button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    margin-bottom: 20px;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .balance-message {
    font-weight: bold;
    color: blue;
  }
  
  .error {
    color: red;
  }
  </style>
  