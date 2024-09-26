<template>
    <div>
      <h2>Deposit Funds</h2>
      <form @submit.prevent="Deposit">
        <div class="form-group">
          <label for="amount">Amount:</label>
          <input
            v-model="amount"
            type="number"
            id="amount"
            placeholder="Enter amount"
            required
          />
        </div>
  
        <button type="submit">Deposit</button>
      </form>
  
      <!-- Success or error messages -->
      <div v-if="successMessage" class="success">
        {{ successMessage }}
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
        amount: "",
        successMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async Deposit() {
        try {
          // Clear previous messages
          this.successMessage = null;
          this.errorMessage = null;
  
          // Make POST request to the deposit API
          const response = await api.post("/deposit/", {
            amount: this.amount,
          });
  
          // Handle successful response
          this.successMessage = response.data.message;
          this.amount = ""; // Reset the form field
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while making the deposit.";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Simple styles for form and messages */
  form {
    margin: 20px 0;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .success {
    color: green;
  }
  
  .error {
    color: red;
  }
  </style>
  