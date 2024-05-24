<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <h1>  {{ message }} </h1>
  <MyComponent @onEvent="getDataHandler"/>
  <MyComponent :title="title"/>
  <MyLifeCycle />
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import MyComponent from './components/MyComponent.vue'
import MyLifeCycle from './components/MyLifeCycle.vue'
export default {
  name: 'App',
  components: {
    HelloWorld,
    MyComponent,
    MyLifeCycle
  },
  data(){
    return{
      title:{
        type:String,
        default:'Hello Vue 3!'
      },
      message: 'Hello My Component!'
    }
  },
  methods:{
    getDataHandler(data){
      console.log(data)
      this.message = data
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
