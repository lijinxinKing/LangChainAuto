<template>
  
  <h1>Vue3</h1>
  <button @click="test()">测试按钮</button>
  <button @click="send()">发送数据</button>
 
</template>
 
<script setup>
import axios from 'axios';
function test(){
  axios.get('http://127.0.0.1:5000/api/axios').
  then(res=>{
    console.log(res)
  })
}
 
function send(){
  axios.post('http://127.0.0.1:5000/api/msg',{name:'lily',age:23,school:'麻省理工'}).
  then(res=>{
    console.log(res)
  })
}
</script>
 
 