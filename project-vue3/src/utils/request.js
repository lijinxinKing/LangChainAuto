import axios from 'axios'
//mport querystring from 'querystring'
const instance = axios.create({
    // 网络请求的公共配置
    timeout:5000
})
// 参考文档 axios 看云
// 发送数据之前 拦截器
// instance.interceptors.request.use(
//     config=>{
//         if(config.method === 'post'){
//             config.data = querystring.stringify(config.data)
//         }
//         return config
//     },
//     error =>{
//         return Promise.reject(error)
//     }
// )
// 获取数据之前
// instance.interceptors.response.use(
//     response =>{
//         return response.status === 200? Promise.resolve(response):Promise.reject(response)     
//     },
//     error => {
//         const {response} = error
//         errorHandle(response.status,response.info)
//     }
// )
// const errorHandle=(status,info) =>{
//     console.log(status)
//     switch(status){
//         case 400:
//             console.log(info)
//             break
//     }
// }

export default instance