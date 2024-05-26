<template>
    <p>{{ message }}</p>
</template>
<script>
import axios from 'axios'
//import api from '../api/index'
export default{
    name:'MyAxios',
    data(){
        return{
            message:'I am axios'
        }
    },
    mounted(){
      axios.get('https://iwenwiki.com/api/blueberrypai/getChengpinDetails.php').then(res=>{
        console.log(res.data)
      })
      //解决网络跨域问题
      axios.get('https://iwenwiki.com/api/FingerUnion/list.php').then(res=>{
        console.log(res.data)
      })
      // api.getChengpin().then(res =>{
      //   console.log('#########')
      //   console.log(res.data)
      // })
    }
}
</script>
<style scoped>

</style>