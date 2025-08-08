import { createApp } from 'vue'
import App from './App.vue'
import BootstrapVue3 from 'bootstrap-vue-3';
import {
  BIconCardChecklist,
} from "bootstrap-icons-vue";

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

const app = createApp(App);
app.component("BIconCardChecklist", BIconCardChecklist);
app.use(BootstrapVue3);
app.mount('#app');
