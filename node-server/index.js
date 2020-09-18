var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 5000;

const nsp = io.of('/test');
app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});

nsp.on('connection', function (socket) {
    socket.on('chat message', function (msg) {
        nsp.emit('chat message', msg);
    });
});

http.listen(port, function () {
    console.log('listening on *:' + port);
});
