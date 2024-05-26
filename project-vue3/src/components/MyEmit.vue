<template>
    <h3>自定义事件传递数据</h3>
    <button @click="sendClickHandle">点击传递</button>
</template>
<script>
export default{
    name:"MyEmit",
    data(){
        return{
            message:"我是自定义数据传递"
        }
    },
    methods:{
        sendClickHandle(){
            this.$emit("onEvent",this.message)
        }
    }
}
</script>
<style scoped>

</style>
