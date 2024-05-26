<template>
    <P>{{ message }}</P>
    <router-link to="/">首页</router-link> |
    <router-link to="/about">关于</router-link>|
    <router-link to="/news">新闻</router-link>
    <router-view></router-view>
</template>
<script>
export default{
    name:'MyRouter',
    data(){
        return{
            message:'My Router'
        }
    }
}
</script>

<style scoped>

</style>