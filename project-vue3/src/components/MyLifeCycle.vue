<template>
    <p>我是生命周期组建</p>
</template>
<script>
export default{
    name:'MyLifeCycle',
    beforeCreate(){
        console.log('beforeCreate：组建创建之前')
    },
    created(){
        console.log('created：组建创建之后')
    },
    beforeMount(){
        console.log('beforeMount:组建渲染之前')
    },
    mounted(){
        console.log('mounted：组建渲染之后')
    },
    beforeUpdate(){
        console.log('beforeUpdate：组建更新之前')
    },
    updated(){
        console.log('updated：组建更新之后')
    },
    beforeUnmount(){
        console.log('beforeUnmount：组建卸载之前')
    },
    unmounted(){
        console.log('unmounted：组建卸载之后')
    }

}
</script>
<style scoped>

</style>
