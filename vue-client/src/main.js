import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
const options = { path: '/socket.io/' }; //Options object to pass into SocketIO

Vue.use(new VueSocketIO({
  debug: true,
  connection: SocketIO('http://localhost:5000/test', options), //options object is Optional
})
);

new Vue({
  render: h => h(App)
}).$mount('#app')