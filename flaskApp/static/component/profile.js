import Loading from'./loading.js'
import Error from'./error.js'


export default {
    template: `<div> 
        <div v-if='name'>
            this is Profile page {{ name }} 
        </div>
        <Error v-else-if='hasError' />
        <Loading v-else='hasError' />
        </div>`, 
    data() {
        return {
            name : null,
            hasError : false,
        }
    },
    mounted() {
        fetch("http://127.0.0.1:5000/profile", {
            headers: {
                'Authentication-Token' : localStorage.getItem('auth-token')
            }
        }).then((res) => {
            console.log(res.statusText)
            return res.json()
        }).then((data) => {
            console.log(data)
            this.name = data.name
        })
    },
    components : {
        Loading,
        Error,
    }
}