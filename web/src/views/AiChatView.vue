<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, reactive, watch } from "vue";
import { UserFilled } from "@element-plus/icons-vue";
import { ElMessage, type FormInstance } from "element-plus";
import {
  type ChatItem,
  type WSReqParams,
  type WSResParams,
  getWebsocketUrl,
  wsSendMsgFormat,
} from "@/views/AiChatWebsocket.ts";
import { sparkConfig } from "@/config";
import { copyToClipboard } from "@/utils/commonUtil.ts";
import axios from 'axios'
import { fa } from "element-plus/es/locales.mjs";
import accIcon from "../assets/AI.png"
// 聊天列表ref
const aiChatListRef = ref();

// 会话列表的观察对象（观察子元素变化，用来提示用户体验，当会话有变化时，自动滚动到变化位置）
let chatListObserver: MutationObserver;
// 会话列表
let chatList = ref<ChatItem[]>([]);
// 当前加载回答的index
let loadingIndex = ref<number | null | undefined>();
let getIcon = accIcon

// 连接星火的WebSocket实例
onMounted(() => {
  // 创建 聊天列表 变化的观察者对象
  //createMutationObserver(aiChatListRef.value);
});

/**
 * 创建 聊天列表 变化的观察者对象：监听目标元素的高度变化
 * @param targetElement：要观察的目标元素
 */

const createMutationObserver = (targetElement: Element) => {
  // 创建一个新的 MutationObserver 实例
  chatListObserver = new MutationObserver((mutationsList, observer) => {
    // 当子元素发生变化时，获取元素的滚动区域高度
    const scrollHeight = targetElement.scrollHeight;
    // 滚动的处理
    scrollHandle(scrollHeight);
  });

  // 启动观察器并配置所需的观察选项
  chatListObserver.observe(targetElement, { childList: true, subtree: true });
};

/**
 * 滚动定位处理
 * @param val
 */
const scrollHandle = (val: number) => {
  aiChatListRef.value?.scrollTo({
    top: val,
    behavior: "smooth", // 表示滚动行为，支持参数 smooth(平滑滚动),instant(瞬间滚动),默认值 auto
  });
};

// 提问文字
let problemText = ref<string>("");
// 提问最大字数
const maxCharCount = ref<number>(300);

/**
 * 监听提问文字
 */
const problemTextWatcher = watch(
  () => problemText.value,
  () => {
    // 限制最大字数
    if (problemText.value.length > maxCharCount.value) {
      problemText.value = problemText.value.slice(0, maxCharCount.value);
    }
  }
);

// 发送按钮的禁用状态
const sendBtnDisabled = ref(false);
// webSocket 响应数据状态
let wsMsgReceiveStatus = ref<"receiveIng" | "receiveFinshed">();
const sendQuestion = () => {
  if (sendBtnDisabled.value) {
    // 发送按钮禁用状态
    return;
  }
  if (problemText.value?.trim()?.length <= 0) {
    // 输入问题文字是空字符串
    ElMessage.warning({ message: "请输入您想了解的内容..." });
    return;
  }

  // 不是在接收消息的时候才可以发送问题
  if (wsMsgReceiveStatus.value !== "receiveIng") {
    chatList.value.push({
      role: "user",
      content: problemText.value,
    });
    sendBtnDisabled.value = true;
    askSpark();
  }
};

/**
 * 连接星火WebSocket并发送问题
 * @param question
 */
const askSpark = () => {
  // 1. 生成鉴权URL
  // let wsUrl = getWebsocketUrl(sparkConfig);
  // console.log("wsUrl", wsUrl);
  // console.log("sparkConfig", sparkConfig);
  // 2. 判断浏览器是否支持WebSocket
  // 用Axios 和 Flask 间进行通信
  // axios.get('https://iwenwiki.com/api/blueberrypai/getChengpinDetails.php').then(res=>{
  //   console.log(res.data)
  // })

  // 用Axios 和 Flask 间进行通信
  // 进行 Falsk 间的数据传递
  console.log('chatList.value:')
  let getData = ''
  axios.post('http://10.119.150.151:5000/ask',JSON.stringify(chatList.value)).then(res=>{
    console.log(res.data)
    getData = res.data
    if(res){
        chatList.value.push({
        role: "assistant",
        content: "",
      });
      loadingIndex.value = chatList.value.length - 1;
    }
    let resObj = res.data;
    
    // 响应数据 WSResParams
    if (res.data === '') {
      ElMessage.error("提问失败");
      console.error(
        `提问失败:${resObj.header.code} - ${resObj.header.message}`
      );      
    } else {
      wsMsgReceiveHandle(resObj);
    }
    // 处理连接失败
    if(getData === '') {
      ElMessage.error("WebSocket连接失败");
    }
  })
}

/**
 * 处理WebSocket响应回来的数据
 * @param res WSResParams
 */
const wsMsgReceiveHandle = (res: WSResParams) => {
  // 开始接收消息
  // if (res.payload.choices.status === 0) {
  //   problemText.value = "";
  //   wsMsgReceiveStatus.value = "receiveIng";
  // }
  console.log(res)
  wsMsgReceiveStatus.value = "receiveIng";
  //let dataArray = res?.payload?.choices?.text || [];
  // for (let i = 0; i < dataArray.length; i++) {
  //     chatList.value[chatList.value.length - 1].content += dataArray[i].content;
  // }
  chatList.value[chatList.value.length - 1].content += res;
  // 继续接收消息
  // if (res.payload.choices.status === 1) {
  //   wsMsgReceiveStatus.value = "receiveIng";
  //   let dataArray = res?.payload?.choices?.text || [];
  //   for (let i = 0; i < dataArray.length; i++) {
  //     chatList.value[chatList.value.length - 1].content += dataArray[i].content;
  //   }
  // }

  // 完成接收消息
  // if (res.payload.choices.status === 2) {
  //   wsMsgReceiveStatus.value = "receiveFinshed";
  //   loadingIndex.value = null;
  //   sendBtnDisabled.value = false;
  // }
  wsMsgReceiveStatus.value = "receiveFinshed"
  loadingIndex.value = null
  sendBtnDisabled.value = false
};

/**
 * 拷贝会话记录到剪贴板
 * @param item
 * @param index
 */
const copyRecord = (item: { content: any }, index: any) => {
  const content = item.content;
  copyToClipboard({
    content,
    success() {
      ElMessage({
        message: "复制成功",
        type: "success",
      });
    },
    error() {
      ElMessage({
        message: "复制失败",
        type: "error",
      });
    },
  });
};

/**
 * 删除记录
 * @param item
 * @param index
 */
const deleteRecord = (index: number) => {
  if (!sendBtnDisabled.value) {
    chatList.value.splice(index, 1);
  }
};

/**
 * 重新回答
 * @param item 如果被点击的会话项
 * @param index
 */
const reReply = (index: number) => {
  if (wsMsgReceiveStatus.value !== "receiveIng") {
    if (chatList.value.length - 1 === index) {
      // 如果是最后一条重新回答,则直接删除最后一条记录重新作答
      deleteRecord(index);
      sendBtnDisabled.value = true;
      askSpark();
    } else {
      // 如果不是是最后一条重新回答,则后面重新添加问题继续进行询问
      // 有可能上一条回答内容被直接删除，所以需要循环往前找最近的一条问题记录。找到之后则以这条问题记录为准回答
      let i = index - 1;
      while (i >= 0) {
        if (chatList.value[i].role === "user" && chatList.value[i].content) {
          // 符合条件：角色是用户，有问题内容
          chatList.value.push({
            role: "user",
            content: chatList.value[index - 1].content,
          });
          sendBtnDisabled.value = true;
          askSpark();
          break;
        }
        i--;
      }
    }
  }
};

/**
 * AI回答内容中代码块的复制
 */
const handleCopyCodeSuccess = () => {
  ElMessage({
    message: "复制成功",
    type: "success",
  });
};

/**
 * 组件销毁时
 */
onBeforeUnmount(() => {
  // 停止属性监听
  problemTextWatcher();
  // 停止对会话列表的观察变动
  //chatListObserver.disconnect();
});
</script>

<template>
  <div class="ai-chat-view">
    <ul ref="aiChatListRef" class="ai-chat-list">
      <li class="ai-chat-item">
        <div class="ai-chat-avatar">
          <el-avatar
            :size="50"
            fit='contain'
            :src="getIcon"
          />
        </div>

        <div class="ai-chat-content-box init-box">
          <div class="ai-chat-title">CSW AI Auto Agent</div>
          <div class="ai-chat-text">为CSW自动化测试定制AI 1.0版本，支持多轮对话，能回答有关项目的问题</div>
          <div class="ai-chat-text">
          </div>
        </div>
      </li>
      <li
        v-for="(item, index) of chatList"
        class="ai-chat-item"
        :class="item.role + '-item'"
      >
        <div class="ai-chat-avatar">
          <el-avatar
            v-if="item.role === 'assistant'"
            :size="50"
            fit="fit"
            :src="getIcon"
          />
          <el-avatar
            v-if="item.role === 'user'"
            :size="50"
            :icon="UserFilled"
          />
        </div>
        <div
          v-if="item.role === 'user'"
          class="ai-chat-content-box"
          :class="item.role + '-box'"
        >
          {{ item.content }}
        </div>
        <div
          v-if="item.role === 'assistant'"
          class="ai-chat-content-box"
          :class="item.role + '-box'"
        >
          <v-md-preview
            :text="item.content"
            @copy-code-success="handleCopyCodeSuccess"
          ></v-md-preview>
          <div v-if="loadingIndex === index" class="loading-icon-box">
            <el-icon size="24"><Loading /></el-icon>
          </div>
          <div class="ai-chat-operate">
            <span
              class="re-reply-btn"
              :class="{
                disabled: sendBtnDisabled,
              }"
              @click="reReply(index)"
            >
              重新回答
            </span>
            <div
              class="operate-icon-box"
              :class="{
                disabled: sendBtnDisabled,
              }"
            >
              <el-icon>
                <DocumentCopy @click="copyRecord(item, index)" />
              </el-icon>
              <el-icon @click="deleteRecord(index)">
                <Delete />
              </el-icon>
            </div>
          </div>
        </div>
      </li>
    </ul>

    <div class="ai-chat-form-wrapper">
      <div class="ai-chat-form-box">
        <textarea
          v-model="problemText"
          :rows="4"
          placeholder="在此输入您想了解的内容..."
          @keydown.enter.exact.prevent="sendQuestion"
          @keydown.enter.shift.exact.prevent="problemText += '\n'"
        ></textarea>

        <div class="chat-form-footer">
          <div class="btns">
            <span class="content-tips">
              {{ problemText.length }} / {{ maxCharCount }}
            </span>
            <span>
              <el-button
                type="primary"
                :disabled="sendBtnDisabled"
                @click="sendQuestion"
              >
                发送
              </el-button>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.ai-chat-view {
  background-color: #fff;
  padding: 40px 150px 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  // 对话列表
  .ai-chat-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;

    // 去掉滚动条
    /* Firefox */
    scrollbar-width: none;
    /* IE10+ */
    -ms-overflow-style: none;
    /* Firefox */
    overflow: -moz-scrollbars-none;
    /* webkit */
    &::-webkit-scrollbar {
      display: none;
    }

    // 会话项
    .ai-chat-item {
      display: flex;
      align-items: flex-start;
      margin-bottom: 40px;
    }

    // 会话头像
    .ai-chat-avatar {
      margin-right: 24px;
    }

    // 会话内容盒子
    .ai-chat-content-box {
      padding: 16px 30px;

      // 会话加载图标盒子
      .loading-icon-box {
        .el-icon {
          transform: translate(0, 0);
          animation: rotate 3s linear infinite;
        }

        @keyframes rotate {
          0% {
            transform: translate(0, 0) rotate(0deg);
          }
          100% {
            transform: translate(0, 0) rotate(360deg);
          }
        }
      }

      // 会话列表初始化盒子
      &.init-box {
        width: 100%;
        background: #eff7ff;
        border-radius: 10px;
        background-image: url("https://ydcqoss.ydcode.cn/static/officialhome/ai-chat-init-bg.png");
        background-size: cover;
        background-repeat: no-repeat;

        .ai-chat-title {
          font-size: 1.125rem;
          color: #005fdb;
          margin-bottom: 1rem;
        }

        .ai-chat-count {
          font-size: 0.875rem;
          color: #fff;
        }
        .ai-chat-text {
          font-size: 0.875rem;
          color: #666666;
          line-height: 1.8;
        }
      }

      // 会话列表用户盒子
      &.user-box {
        background: #fff;
        padding-left: 0;
        padding-top: 0;
        line-height: 2;
      }

      //会话列表ai回复盒子
      &.assistant-box {
        width: 100%;
        background: #eff7ff;
        border-radius: 10px;
      }
    }

    // 会话操作
    .ai-chat-operate {
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;

      // 重新回答
      .re-reply-btn {
        font-size: 14px;
        color: #2984ff;

        &.disabled {
          color: #ccc;
        }
      }

      //  操作图标
      .operate-icon-box {
        display: flex;
        align-items: center;
        .el-icon {
          color: #7094c4;
          font-size: 20px;
          margin-left: 16px;
          cursor: pointer;
        }

        &.disabled .el-icon {
          color: #ccc;
        }
      }
    }
  }

  // 发送问题表单
  .ai-chat-form-wrapper {
    padding-left: calc(40px + 24px); // 40px:头像的宽度  24px:头像和会话框的距离
    background-color: #fff;
    z-index: 1000;
    .ai-chat-form-box {
      border: 1px solid #526ef9;
      border-radius: 10px;
      position: relative;
    }

    // 多行文本
    textarea {
      width: calc(100% - 4px); // 减去滚动条的宽度
      margin-top: 2px;
      padding: 0.5rem 6rem 1rem 1.25rem;
      padding-bottom: 0;
      border: none;
      outline: none;
      resize: none;
      background: #fbfbfb;
      border-radius: 10px;
      font-family: PingFang SC, Hiragino Sans GB, Arial, Microsoft YaHei,
        Helvetica Neue, sans-serif;
      color: #666;

      &::-webkit-scrollbar {
        width: 3px;
      }
    }

    // 发送问题表单footer
    .chat-form-footer {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      margin-top: -5px;
      background: #fbfbfb;
      position: absolute;
      bottom: 1rem;
      right: 1rem;

      // 内容字数提示
      .content-tips {
        margin-right: 1.25rem;
      }
    }
  }

  // 回答内容中markdown预览的样式
  :deep(.v-md-editor-preview .github-markdown-body) {
    padding: 0;
  }
}
</style>
