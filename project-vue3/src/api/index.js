import axios from 'axios'
import path from './path'

const api = {
    //成品详情地址
    getChengpin(){
        return axios.get(path.baseUrl + path.getChengpin)
    }
}
export default api