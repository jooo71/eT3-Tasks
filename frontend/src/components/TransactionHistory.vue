<template>
    <div>
      <h2>Transaction History</h2>
      <button @click="TransactionHistory">Transaction History</button>
  
      <!-- Display Transactions -->
      <div v-if="transactions.length" class="transactions">
        <ul>
          <li v-for="(transaction, index) in transactions" :key="index">
            <strong>{{ transaction.transaction_type }}</strong> - 
            Amount: {{ transaction.amount }} - 
            Date: {{ formatDate(transaction.date) }} 
            <span v-if="transaction.sender"> (Sent by: {{ transaction.sender.name }})</span>
            <span v-if="transaction.recipient"> (Received by: {{ transaction.recipient.name }})</span>
          </li>
        </ul>
      </div>
  
      <!-- Error Message -->
      <div v-if="errorMessage" class="error">
        {{ errorMessage }}
      </div>
    </div>
    <BackButton/>
  </template>
  
  <script>
  import api from "@/api"; // Axios instance
  import BackButton from '@/components/BackButton.vue'; // Import the BackButton component

  export default {
    components: {
    BackButton, // Register the BackButton component
  },
    data() {
      return {
        transactions: [],
        errorMessage: null,
      };
    },
    methods: {
      async TransactionHistory() {
        try {
          // Clear previous messages
          this.errorMessage = null;
  
          // Make GET request to the transaction history API
          const response = await api.get("/transaction-history/");
  
          // Handle successful response
          this.transactions = response.data;
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while fetching the transaction history.";
        }
      },
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString(); // Format the date in a readable way
      },
    },
  };
  </script>
  
  <style scoped>
  /* Basic styles for the transaction list */
  button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    margin-bottom: 20px;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .transactions ul {
    list-style-type: none;
    padding: 0;
  }
  
  .transactions li {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    margin: 5px 0;
    padding: 10px;
  }
  
  .error {
    color: red;
    margin-top: 20px;
  }
  </style>
  