<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <MyComponent></MyComponent>
  <MyProps :title="title"></MyProps>
  <MyEmit @onEvent="getDataHandle"></MyEmit>
  <p>{{ message }}</p>
  <MyLifeCycleVue ></MyLifeCycleVue>
  <MySWiperVue></MySWiperVue>
  <MyAxios></MyAxios>
  <MyRouter></MyRouter>
  <MyVuex></MyVuex>
  <p>counter:{{ $store.state.counter }}</p>
</template>

<script>
import MyComponent from './components/MyComponent.vue'
import MyProps from './components/MyProps.vue'
import MyEmit from './components/MyEmit.vue'
import MyLifeCycleVue from './components/MyLifeCycle.vue'
import MySWiperVue from './components/MySWiper.vue'
import MyAxios from './components/MyAxios.vue'
import MyRouter from './components/MyRouter.vue'
import MyVuex from './components/MyVuex.vue'
export default {
  name: 'App',
  components: {
    MyComponent,
    MyProps,
    MyEmit,
    MyLifeCycleVue,
    MySWiperVue,
    MyAxios,
    MyRouter,
    MyVuex
  },
  data(){
    return{
      title:"传递数据",
      message: ''
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
