import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import store from './store'
Vue.prototype.$axios = axios;

// element
import { 
  Button, 
  Select, 
  Tooltip,
  Option,
  Switch
} from 'element-ui';
Vue.use(Button)
Vue.use(Select)
Vue.use(Tooltip)
Vue.use(Option)
Vue.use(Switch)

// ant-design
import { message } from 'ant-design-vue';
Vue.prototype.$message = message;


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
