import moment from "moment";
moment.locale("zh-cn");
const timeUtil = {
  dateFormat: (unix: number, formatStr: string) => {
    return moment.unix(unix).format(formatStr);
  },
};
export default timeUtil;
