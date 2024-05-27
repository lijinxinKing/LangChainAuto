import axios, { type AxiosResponse } from "axios";
import { ElMessage } from "element-plus";

// 电子书信息
export interface BookInfo {
  /** 书籍Id */
  id: number;
  /** 书籍标题 */
  title: string;
  /** 书籍描述 */
  describe: string;
  /** 书籍封面图 */
  coverImage: string;
  /** 是否删除 0-否 1-是 */
  isDeleted: number;
}

// 章节内容锚点
export interface MdCatalogItem {
  /** 标题 */
  title: string;
  /** 标题序号 */
  lineIndex: string | null;
  /** 标题等级 */
  indent: number;
}

// 章节内容
export interface BookChapterItem {
  /**章节 id */
  id: number;
  /** 书籍id */
  electronicBookId: number;
  /** 章节标题 */
  name: string;
  /** 章节描述 */
  describe: string;
  /** 章节内容 */
  content: string;
  /** 是否删除 0-否 1-是 */
  isDeleted: number;
  /** 章节排序 */
  sortOrder: number;
  /** 章节目录锚点 */
  anchors?: MdCatalogItem[];
}

/**
 * 查询电子书列表
 * @returns
 */
export function queryBookList(): Promise<BookInfo[]> {
  return new Promise((resolve, reject) => {
    axios
      .get(`/electronicBook/queryElectronicBookList`)
      .then((res: AxiosResponse) => {
        if (res.data.code === 200) {
          resolve(res.data.data);
        } else {
          ElMessage.error("获取电子书列表失败");
        }
      });
  });
}

/**
 * 查询电子书详情
 * @returns
 */
export function queryBookDetail(bookId: number): Promise<BookInfo> {
  return new Promise((resolve, reject) => {
    axios
      .get(`/electronicBook/queryElectronicBookById/id/${bookId}`)
      .then((res: AxiosResponse) => {
        if (res.data.code === 200) {
          resolve(res.data.data);
        } else {
          ElMessage.error("获取电子书详情失败");
        }
      });
  });
}

/**
 * 查询电子书章节列表
 * @returns
 */
export function queryBookChapterList(
  bookId: number
): Promise<BookChapterItem[]> {
  return new Promise((resolve, reject) => {
    axios
      .get(`/electronicBookItem/queryElectronicBookItemList/bookId/${bookId}`)
      .then((res: AxiosResponse) => {
        if (res.data.code === 200) {
          resolve(res.data.data);
        } else {
          ElMessage.error("获取电子书章节列表失败");
        }
      });
  });
}
