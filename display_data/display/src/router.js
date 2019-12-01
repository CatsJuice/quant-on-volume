import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    // mode: 'hash',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '',
            redirect: '/hly/list',
        },
        {
            path: '/hly/list',
            name: 'hlylist',
            component: () => import( /* webpackChunkName: "code-list" */ '@/pages/HlyList')
        },
        {
            path: '/hly/:code',
            name: 'hlyDetail',
            component: () => import( /* webpackChunkName: "hly-detail" */ '@/pages/HlyDetail')
        },
    ]
})
