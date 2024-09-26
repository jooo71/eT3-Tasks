<template>
  <nav>
    <router-link to="/deposit">deposit</router-link> |
    <router-link to="/withdraw">withdraw</router-link> |
    <router-link to="/payBill">payBill</router-link> |
    <router-link to="/buyAirtime">buyairtime</router-link> |
    <router-link to="/transfer">transfer</router-link> |
    <router-link to="/balance">balance</router-link> |
    <router-link to="/transaction-history">transactionHistory</router-link> |


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
