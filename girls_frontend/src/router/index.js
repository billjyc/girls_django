import Vue from 'vue'
import Router from 'vue-router'
import Teamlist from '@/components/TeamList'

Vue.use(Router)

const route = new Router({
    routes: [
        {
            path: '/',
            name: 'TeamList',
            component: Teamlist,
        },
        {
            path: '/team-list/',
            name: 'TeamList',
            component: Teamlist,
        },
    ],
})

export default route
