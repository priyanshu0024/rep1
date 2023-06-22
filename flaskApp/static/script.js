import home from './component/home.js'
import login from './component/login.js'
import profile from './component/profile.js'

const routes = [{path : '/', component: home}, 
          {path : '/profile', component : profile},
          {path : '/login', component : login}
         ]


const router = new VueRouter({
    routes,
})

new Vue({
    el: "#app",
    template: `<div>
    <router-link to='/'>Home</router-link>
    <router-link to='/profile'>Profile</router-link>
    <router-link to='/login'>Login</router-link>
    <button @click="logout"> Logout </button>
    <router-view></router-view>
    </div>`,
    router,
    methods: {
        logout() {
            localStorage.removeItem('auth-token')
            window.location.href = '/logout'
        }
    }
})