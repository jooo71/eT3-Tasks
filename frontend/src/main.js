import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// import { useAuthStore } from './store/auth'

createApp(App).use(store).use(router).mount('#app')


