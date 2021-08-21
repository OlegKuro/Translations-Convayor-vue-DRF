import Vue from 'vue';
import io from 'socket.io-client';

const socket = io('http://localhost:4000');

Vue.prototype.$socketIO = {
  subscribe(channel) {
    return socket.emit('subscribe', channel);
  },
  unsubscribe(channel) {
    return socket.emit('unsubscribe', channel);
  },
  get socket() {
    return socket;
  }
};
