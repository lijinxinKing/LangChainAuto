// 全局样式
import "./assets/main.css";
// 引入创建应用实例方法
import { createApp } from "vue";
// App 根组件
import App from "./App.vue";
// router
import router from "./router";
// ElementPlus 相关
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import zhCn from "element-plus/dist/locale/zh-cn.mjs";
import "dayjs/locale/zh-cn";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
// axios
import axios from "axios";
// md 预览
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

// highlightjs
import hljs from 'highlight.js';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

// md 复制代码插件
import createCopyCodePlugin from "@kangc/v-md-editor/lib/plugins/copy-code/index";
import "@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css";

// 配置api地址
import { baseURL } from "./config";
axios.defaults.baseURL = baseURL;

// 创建应用实例
const app = createApp(App);

// 安装路由插件
app.use(router);

// 导入ElementPlus所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 安装ElementPlus插件
app.use(ElementPlus, {
  locale: zhCn,
});

// md 预览
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});
VMdPreview.use(createCopyCodePlugin());
app.use(VMdPreview);

// 应用实例挂载
app.mount("#app");
