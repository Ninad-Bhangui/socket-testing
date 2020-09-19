var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 5000;

const nsp = io.of('/test');
app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});

nsp.on('connection', function (socket) {
    console.log('a user connected');
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });

    socket.on('chat message', (msg) => {
        nsp.emit('chat message', msg);
    });

    socket.on('echo', (msg) => {
        console.log('got echo!');
        nsp.emit('echoed', { data: 'echo!' });
    });

    socket.on('room_send', (msg) => {
        nsp.emit('my_response', { data: msg['data'] }, room = msg['room'])
    });

    socket.on('join', (msg) => {
        console.log(`Joining room ${msg['room']}`)
        socket.join(msg['room']);
        rooms = Object.keys(socket.rooms)
        console.log(`In rooms ${rooms}`)
        nsp.emit('joined_room', { data: `In rooms ${rooms.join()}`, rooms: rooms });
    });
});

http.listen(port, function () {
    console.log('listening on *:' + port);
});
