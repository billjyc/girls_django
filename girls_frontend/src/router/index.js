import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

const route = new Router({
    routes: [
        {
            path: '/',
            name: 'Home',
            component: HelloWorld,
        },
    ],
})

export default route
