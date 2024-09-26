<template>
    <div>
      <h2>Buy Airtime</h2>
      <form @submit.prevent="BuyAirtime">
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
  
        <button type="submit">Buy Airtime</button>
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
      async BuyAirtime() {
        try {
          // Clear previous messages
          this.successMessage = null;
          this.errorMessage = null;
  
          // Make POST request to the buy_airtime API
          const response = await api.post("/buy-airtime/", {
            amount: this.amount,
          });
  
          // Handle successful response
          this.successMessage = response.data.message;
          this.amount = ""; // Reset form fields
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while buying airtime.";
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
    background-color: #ffa500;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #e69500;
  }
  
  .success {
    color: green;
  }
  
  .error {
    color: red;
  }
  </style>
  