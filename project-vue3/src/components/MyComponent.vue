<template>
  <div>
    <h1>MyComponent</h1>
    <button @click="sendMessage">Send Message</button>
  </div>
</template>
<script>
export default{
  name: 'MyComponent',
  props: {
    title: String
  },
  data(){
    return{
      data: 'Hello from MyComponent',
      messsage:'我是MyComponent组件'
    }
  },
  methods:{
    sendMessage(){
      this.$emit('onEvent', this.messsage)
    }
  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only 只在当前组件中生效，其他组件不会变 -->
<style scoped>
h1{
  color: red;
}
</style>