<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ChatRound } from "@element-plus/icons-vue";
import homeLogo from "../assets/home_logo.png";

const router = useRouter();
interface Nav {
  path: string;
  title: string;
  icon: any;
}
let home_logo = homeLogo;
// 导航列表
const navList = ref<Nav[]>([
  {
    path: "/AIAuto",
    title: "CSW AI Auto Agent",
    icon: ChatRound,
  },
]);

/**
 * 点击导航菜单的处理
 * @param navItem
 */
const navClickHandle = (navItem: Nav) => {
  router.push(navItem.path);
};

/**
 * 点击logo的处理
 */
const logoImgClickHandle = () => {
  window.location.href = "http://10.119.96.35:8088/#/dashboard";
};
</script>

<template>
  <div class="page-header">
    <div class="page-header-wrapper">
      <!-- logo  src="../assets/home_logo.png" JSON.stringify(chatList.value)  
        https://home.lenovo.com/static/img/home_logo.40e29e52.png -->
      <el-image
        class="logo-image"    
        fit="fit"   
        :src="home_logo"
        alt="logo"

        @click="logoImgClickHandle"
      />

      <!-- 导航 -->
      <nav>
        <span
          v-for="(navItem, index) of navList"
          :key="index"
          class="nav-item"
          :class="{ active: navItem.path === router.currentRoute.value.path }"
          @click="navClickHandle(navItem)"
        >
          <el-icon> <component :is="navItem.icon"> </component></el-icon>
          <span>{{ navItem.title }}</span>
        </span>
      </nav>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.page-header {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  .page-header-wrapper {
    flex: 1;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  // logo
  .logo-image {
    width: auto;
    height: 28px;
    cursor: pointer;
  }

  // 导航
  nav {
    display: flex;
    align-items: center;
    .nav-item {
      margin-left: 60px;
      display: flex;
      align-items: center;
      cursor: pointer;

      i {
        width: 24px;
        height: 24px;
        // margin-right: 6px;
      }

      &:hover {
        color: $primary-color;
      }

      &.active {
        color: $primary-color;

        i {
          color: $primary-color;
        }
      }
    }
  }
}
</style>
