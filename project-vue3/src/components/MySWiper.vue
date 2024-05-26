<template>
 <p>我的 轮播图</p>
 <Swiper 
    :slides-per-view="3"
    :space-between="50"
    @swiper="onSwiper"
    @slideChange="onSlideChange">
    <SwiperSlide>
        <img src="../assets/AI.png">
    </SwiperSlide>
    <SwiperSlide>
        <img src="../assets/AI.png">
    </SwiperSlide>
    <SwiperSlide>
        <img src="../assets/AI.png">
    </SwiperSlide>
 </Swiper>
</template>
<script>
//import {Swiper,SwiperSlider} from 'swiper'
import {Pagination} from 'swiper'
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css'
//import 'swiper/css/Pagination'
export default{
    name:'MySWiper',
    components:{
        Swiper,
        SwiperSlide,
        
    },
    data(){
        return{
            message:'Test',
            modules:[Pagination]
        }
    },
    methods:{
        onSwiper(swiper){
        console.log(swiper)
      },
      onSlideChange (){
        console.log('slide change')
      }

    }
}
</script>
<style scoped>

</style>