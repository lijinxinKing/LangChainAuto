import { createStore } from 'vuex'

// VueX的核心作用就是帮我们管理组件之间的状态
const store = createStore({
    // 所有的数据都在这里
    state:{
        counter:0
    }
})

export default store