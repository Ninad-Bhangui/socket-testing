<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <!-- <button @click="send_to_socket()">Click me to send to socket server!!</button><br> -->
    <button @click="echo()">Echo</button><br>
    <input
      type="text"
      placeholder="Enter Room"
      v-model="room_name"
    >
    <button @click="join_room()">Click me to Join room!!</button><br>
    <input
      type="text"
      placeholder="Enter Message"
      v-model="message"
    >
    <select
      v-if="rooms.length !=0"
      type="text"
      placeholder="Send to Room"
      v-model="selected_room"
    >
      <option
        :key="room"
        v-for="room in rooms"
      >{{room}}</option>
    </select>
    <span v-else>No Rooms found!!
    </span>
    <button @click="send_to_room()">Click me to send to socket server!!</button><br>
    <button @click="socketmsg=[]">Clear Messages!!</button>
    <div
      :key="idx"
      v-for="(msg,idx) in socketmsg"
    >{{idx}}. {{msg}}</div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      socketmsg: [],
      rooms: [],
      message: undefined,
      room_name: undefined,
      selected_room: undefined
    }
  },
  props: {
    msg: String
  },
  methods: {
    echo () {
      this.$socket.emit('echo', { data: 'echo from client' });
    },
    send_to_room () {
      console.log(`Sending to ${this.selected_room}..`);
      this.$socket.emit('room_send', { room: this.selected_room, data: this.message })

    },
    join_room () {
      console.log(`Joining ${this.room_name}..`);
      this.$socket.emit('join', { room: this.room_name });
      this.room_name = undefined;
    }
  },
  sockets: {
    connect () {
      console.log("Socket connection established");
      console.log(this.$socket);
    },
    my_response (data) {
      console.log('test');
      console.log(data.data);
      this.socketmsg.push(data.data);
    },
    joined_room (data) {
      console.log('adding room')
      data['rooms'].forEach(room => {
        if (!this.rooms.includes(room)) {
          this.rooms.push(room);
        }
      })
    },
    echoed (data) {
      console.log('got echo!!');
      this.socketmsg.push(data.data);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
