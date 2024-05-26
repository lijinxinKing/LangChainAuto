import { createRouter,  createWebHashHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView'

const routes = [
    {
        path:'/',
        component:HomeView
    },
    {
        path:'/about',
        component:AboutView
    },
    {
        // 这是异步加载节省资源
        path:'/news',
        component:()=>import('@/views/NewsView.vue')
    }
]

const router = createRouter({
    // 此种方式不需要后台配合重定向
    // a 标签的锚点连接
    history:createWebHashHistory(),
    routes
})
export default router