<template>
    <div>
      <h2>Withdraw Funds</h2>
      <form @submit.prevent="Withdraw">
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
  
        <button type="submit">Withdraw</button>
      </form>
  
      <!-- Success or error messages -->
      <div v-if="successMessage" class="success">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="error">
        {{ errorMessage }}
      </div>
    </div>
    <BackButton/>
  </template>
  
  <script>
  import api from "@/api"; // Ensure you've set up the axios instance in api.js
  import BackButton from '@/components/BackButton.vue'; // Import the BackButton component

  export default {
    components: {
    BackButton, // Register the BackButton component
  },
    data() {
      return {
        amount: "",
        successMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async Withdraw() {
        try {
          // Clear previous messages
          this.successMessage = null;
          this.errorMessage = null;
  
          // Make POST request to the withdraw API
          const response = await api.post("/withdraw/", {
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
              : "An error occurred while making the withdrawal.";
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
    background-color: #ff5733;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #e04e2e;
  }
  
  .success {
    color: green;
  }
  
  .error {
    color: red;
  }
  </style>
  