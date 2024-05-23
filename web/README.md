# vue-demo

## 1. 项目简介

当前，人工智能机器人相关的产品正以惊人的速度涌现，仿佛雨后春笋般不断冒出。在这个背景下，本项目旨在整合讯飞星火认知大模型，打造一个独一无二的“智能 AI 聊天”助手！我们的目标是帮助大家轻松掌握如何借助人工智能技术提升项目开发效能的技能。

为了实现这一目标，我们将结合主流的前端框架 Vue3 和 vite4，利用 webSocket 技术与 AI 进行对接。通过这种方式，我们可以掌握实际项目中所需的关键技能，从而更好地应对各种挑战。

首先，我们深入研究讯飞星火认知大模型，了解其强大的语义理解和自然语言处理能力。这将为我们提供一个坚实的基础，使我们能够开发出智能和高效的 AI 聊天助手。

接下来，我们利用 Vue3 和 vite4 两个流行的前端框架，搭建一个用户友好的界面。Vue3 作为轻量级的前端框架，具有出色的性能和灵活性，可以帮助我们快速构建功能丰富的应用程序。而 vite4 是一个快速的构建工具，可以大大提高我们的开发效率。

在与 AI 的对接方面，我们利用 webSocket 技术实现实时通信。WebSocket 是一种双向通信协议，可以实现客户端和服务器之间的实时数据传输。通过与 AI 进行 WebSocket 通信，我们可以实现实时的语音识别、语义理解和自然语言生成等功能，为用户提供智能和便捷的聊天体验。

最后，我们重点关注实际项目中所需的关键技能。无论是前端开发、后端开发还是人工智能技术的应用，我们都提供详细的教程和实践案例，帮助大家掌握这些关键技能。通过学习和应用这些技能，我们可以更好地应对项目中的各种挑战，提高项目的质量和效率。

## 2. 技术栈介绍

- **后端技术实现**：无

- **前端技术实现**：主要基于 Vite4 + Vue3 作为前端框架来进行开发，利用 Vue Router 进行路由管理，webscoket 等技术和工具。为了统一页面风格，我们还使用了 Element UI 组件库。除此之外，为了实现代码块等文本的预览功能，我们引入了 v-md-editor 编辑器组件，提供了良好的用户体验和便捷性。

| 框架         | 说明                              | 版本   |
| ------------ | --------------------------------- | ------ |
| Vite         | web 应用程序的构建工具            | 4.4.11 |
| Vue          | Vue 框架                          | 3.3.4  |
| TypeScript   | JavaScript 的超集                 | 5.2.0  |
| sass         | CSS 预处理器                      | 1.69.5 |
| vue-router   | Vue 路由                          | 4.2.5  |
| axios        | 基于 Promise 的现代化 HTTP 客户端 | 1.6.2  |
| Element Plus | Vue UI 框架                       | 2.4.3  |
| moment       | JavaScript 日期处理库             | 2.29.4 |

## 3. 项目目录结构

```
/
├── public
│   ├── favicon.ico         # vue官方自带标识
│   └── logo.svg            # 浏览器标签页logo
├── src                     # 项目源代码
│    ├── api                # 用于存放与后端 API 相关的接口定义。
│    ├── assets             # 用于存放项目所需的静态资源文件，例如图片、字体等。
│    ├── components         # 用于存放可复用的组件。
│    ├── lib                # 用于存放sdk等JavaScript库。
│    ├── router             # 路由的定义和配置
│    ├── styles             # 样式文件
│    │     └── main.scss    # 全局的 SCSS 变量等
│    ├── utils              # 工具类文件
│    ├── views              # 页面组件
│    │    ├──components     # 页面所需组件
│    │    └──xxx.vue        # 页面
│    ├── app.vue            # 应用程序根组件
│    ├── config.ts          # 应用程序根组件
│    └── main.ts            # 应用程序入口
├── .gitinore               # git忽略配置文件
├── env.d.ts                # 用于声明环境变量的类型
├── index.html              # 整个应用的入口HTML文件
├── package-lock.json       # 用于锁定安装时的依赖版本
├── package.json            # 应用的配置文件，其中包含了项目的依赖、脚本命令等信息。
├── README.md               # 项目的说明文档，通常包含了项目的介绍、安装和使用方法等信息。
├── tsconfig.app.json       # 用于前端应用程序的TypeScript编译配置
├── tsconfig.json           # TypeScript 项目的配置文件
├── tsconfig.node.json      # 用于后端（服务器端）应用程序的TypeScript编译配置
└── vite.config.js          # Vite 的配置文件
```

## 4. 引入 插件 介绍

- 本项目中采用 v-md-editor 对 markdown 语法进行解析并预览。

  **参考文档：** [v-md-editor 预览组件](https://ckang1229.gitee.io/vue-markdown-editor/zh/examples/preview-demo.html#%E5%9C%A8-vue3-%E4%B8%AD%E5%BC%95%E5%85%A5)

- 时间处理：moment.js 库

  **参考文档：** [Moment.js](https://momentjs.cn/)

## 5. 封装工具介绍

### 5.1 时间格式化

path: `src\utils\timeUtil.ts`

- `timeUtil.dateFormat` 时间格式化

## 6. 推荐的 IDE 设置

- [VSCode](https://code.visualstudio.com/)

- [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (TypeScript + Vue 插件，禁用 Vetur)

## 7. 安装和使用

### 7.1 安装依赖

```sh
npm install
```

### 7.2 编译和运行（开发环境）

```sh
npm run dev
```

### 7.3 打包（生产环境）

```sh
npm run build
```

## 8. 自定义配置

参见[Vite 配置文档](https://vitejs.dev/config/).

## 9. 常见问题处理

### 9.1. node 和 npm 版本问题

建议：Vite 4 需要 Node.js 版本 ≥ 16.0.0，npm 版本 ≥ 8.0.0。但是，某些模板需要更高的 Node.js 版本才能工作，如果您的包管理器发出警告，请升级。

### 9.2. 依赖安装失败

- 报错：ERESOLVE unable to resolve dependency tree

解决：npm 强制安装 ，`npm install -f` 或 ` npm install --legacy-peer-deps`
