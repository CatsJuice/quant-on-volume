// 入口文件
import Vue from 'vue';
import VueRouter from 'vue-router';
import VueResource from 'vue-resource';
Vue.use(VueResource);


// 使用路由
Vue.use(VueRouter);
// 导入路由配置
import router from './router.js';

// 导入根组件
import app from './app.vue';

import 'bootstrap/dist/css/bootstrap.min.css';
import './css/public.scss';

const vm = new Vue({
    el: "#app",
    render: h => h(app),
    router
});