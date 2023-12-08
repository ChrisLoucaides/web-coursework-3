import { createApp } from 'vue'
// @ts-ignore
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';
// @ts-ignore
import { useAuthStore } from '../auth.ts';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const pinia = createPinia();
pinia.use(useAuthStore);

const app = createApp(App).use(pinia)

app.use(router)

app.mount('#app')
