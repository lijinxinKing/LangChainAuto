<template>
  <div class="hello">
    <p v-if="flag">Hello Vue 3!</p>
    <p v-else>Hello World!</p>
    <ul>
      <li v-for="item in newList" :key="item.id">{{item.name}}</li>
    </ul>
    <button @click="counter += 1"> 点击 + {{ counter }} </button>
    <button @click="clickHandler"> 点击 － {{ counter }} </button>
    <button @click="say('Hello Vue 3!')"> 点击 </button>
    <button @click="say('Hello Vue 2!')"> 点击 </button>
    <input v-model.lazy.trim="message" /> <!-- v-model.lazy 修饰符 change事件的时候才会更改 -->
    <span>{{ message }}</span>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data(){
    return {
      msg: 'Hello Vue 3!',
      rawHtml:"<span style='color:red'>This should be red.</span>",
      dynamicId:10001,
      num:10,
      flag:false,
      counter:1,
      newList:[
        {id:1,name:'Apple'},
        {id:2,name:'Banana'},
        {id:3,name:'Orange'},
        {id:4,name:'Mango'},
      ],
      message:'打印消息'
    }
  },
  methods:{
    clickHandler(){
      this.counter -= 1
    },
    say(data){
      console.log(data)
    }
  }
}
</script>
