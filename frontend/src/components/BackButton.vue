<template>
    <button @click="goBack" class="back-button">Back</button>
  </template>
  
  <script>
  export default {
    methods: {
      // Method to navigate back to the previous page
      goBack() {
        this.$router.go(-1);
      }
    }
  };
  </script>
  
  <style scoped>
  .back-button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 16px;
    color: white;
    background-color: #42b983;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .back-button:hover {
    background-color: #7a3535;
  }
  </style>
  