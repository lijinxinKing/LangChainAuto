import CryptoJS from "crypto-js";
import * as base64 from "base-64";

// Websocke配置

interface WSConfig {
  APPID: string;
  APISecret: string;
  APIKey: string;
  VERSION: string;
}

// 根据版本指定访问的领域
const vDomain: { [key: string]: string } = {
  "v1.1": "general",
  "v2.1": "generalv2",
  "v3.1": "generalv3",
};

// 会话项
export interface ChatItem {
  /** 会话角色：user表示是用户的问题，assistant表示AI的回复 */
  role: "user" | "assistant";
  /** 用户和AI的对话内容,所有content的累计tokens需控制8192以内 */
  content: string;
  index?: number;
  [key: string]: any; // 允许包含额外的属性
}

export interface WSReqParams {
  /** header部分 */
  header: {
    /** 应用appid，从开放平台控制台创建的应用中获取（必传） */
    app_id: string;
    /** 每个用户的id，用于区分不同用户（非必传） */
    uid?: string;
  };
  /**parameter部分 */
  parameter: {
    chat: {
      /**指定访问的领域 */
      domain: string;
      /**模型回答的tokens的最大长度:V1.5取值为[1,4096],V2.0取值为[1,8192]，默认为2048。V3.0取值为[1,8192]，默认为2048。 */
      max_tokens?: number;
    };
  };
  /**payload部分：请求数据块 */
  payload: {
    message: {
      text: ChatItem[];
    };
  };
}

export interface WSResParams {
  /** 协议头部，用于描述平台特性的参数 */
  header: {
    code: number;
    message: string;
    /** 本次会话的id */
    sid: string;
    /** 数据状态 0:start，1:continue，2:end */
    status: number;
  };
  /** 响应数据块:数据段，携带响应的数据 */
  payload: {
    choices: {
      /** 数据状态 0:start，1:continue，2:end */
      status: number;
      /** 数据序号，标明数据为第几块。最小值:0, 最大值:9999999 */
      seq: number;
      /** 文本数据 */
      text: ChatItem[];
    };
    usage: {
      text: {
        /**	问题的Tokens大小 */
        question_tokens: number;
        /**	包含历史问题的总Tokens大小 */
        prompt_tokens: number;
        /** 回答的Token大小 */
        completion_tokens: number;
        /**	promptTokens和completionTokens的和，也是本次交互计费的Tokens大小 */
        total_tokens: number;
      };
    };
  };
}

/**
 * 鉴权URL生成
 * @param  config  配置信息
 * @returns url 鉴权URL
 */
export const getWebsocketUrl = (config: WSConfig): string => {
  //
  let url = `wss://spark-api.xf-yun.com/${config.VERSION}/chat`;
  let host="spark-api.xf-yun.com" //window.location.origin;
  let apiKeyName = "api_key";

  let date = new Date().toUTCString();

  let algorithm = "hmac-sha256";

  let headers = "host date request-line";

  // signature
  let signatureOrigin = `host: ${host}\ndate: ${date}\nGET /${config.VERSION}/chat HTTP/1.1`;
  let signatureSha = CryptoJS.HmacSHA256(signatureOrigin, config.APISecret);
  let signature = CryptoJS.enc.Base64.stringify(signatureSha);

  // authorization参数 组成
  let authorizationOrigin = `${apiKeyName}="${config.APIKey}", algorithm="${algorithm}", headers="${headers}", signature="${signature}"`;

  // authorization参数(base64编码的签名信息)生成
  let authorization = base64.encode(authorizationOrigin);
  url = `${url}?authorization=${authorization}&date=${encodeURI(
    date
  )}&host=${host}`;

  return url;
};

/**
 * 发送数据格式化
 * @param sendData
 * @param sendData
 * @returns (数据结构注解可参考本文件中interface WSReqParams)
 */
export const wsSendMsgFormat = (config: WSConfig, sendData: ChatItem[]) => {
  const formatData = {
    header: {
      app_id: config.APPID,
    },
    parameter: {
      chat: {
        domain: vDomain[config.VERSION],
        max_tokens: 1024,
      },
    },
    payload: {
      message: {
        text: sendData,
      },
    },
  };

  return formatData;
};
