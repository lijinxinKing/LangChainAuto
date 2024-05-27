import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    /** 路由懒加载的方式 **/
    {
      path: "/aiChat",
      name: "aiChat",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AiChatView.vue"),
    },
    // 主页（暂时未用，若匹配到则跳转）
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        title: "主页",
      },
    },
  ],
});

// 监听路由切换之后
router.afterEach((to, from, next) => {
  if (to.path === "/") {
    // 如果路由为"/"，则启动切换页面
    router.push("/aiChat");
  }
});

export default router;
