<template>
    <h3>prop传递数据</h3>
    <p>{{ title }} </p>
</template>
<script>
export default{
    name:"MyProps",
    props:{
        title:{
            type:String,
            default:""
        }
    }
}
</script>
<style scoped>

</style>
