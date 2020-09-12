#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context,jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MAIN_NAMESPACE'] = '/'
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace=app.config['MAIN_NAMESPACE'])
        socketio.emit('my_response',
                      {'data': 'Server generated event for test_room', 'count': count},
                      namespace=app.config['MAIN_NAMESPACE'],room="test_room")


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/test_room')
def test_room_message():
    socketio.emit('my_response',{'data':'flask generated msg for sid room'},namespace=app.config['MAIN_NAMESPACE'])
    return jsonify(ok=True)
    
@socketio.on('room_send',namespace=app.config['MAIN_NAMESPACE'])
def room_send(message):
    emit('my_response',{'data':message['data']},namepsace='/',room=message['room'])

@socketio.on('my_event', namespace=app.config['MAIN_NAMESPACE'])
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace=app.config['MAIN_NAMESPACE'])
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace=app.config['MAIN_NAMESPACE'])
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('joined_room',
         {'data': 'In rooms: ' + ', '.join(rooms()),
         'rooms': rooms(),
          'count': session['receive_count']})


@socketio.on('leave', namespace=app.config['MAIN_NAMESPACE'])
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace=app.config['MAIN_NAMESPACE'])
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace=app.config['MAIN_NAMESPACE'])
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace=app.config['MAIN_NAMESPACE'])
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace=app.config['MAIN_NAMESPACE'])
def ping_pong():
    emit('my_pong')


# @socketio.on('connect', namespace=app.config['MAIN_NAMESPACE'])
# def test_connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)
#     emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace=app.config['MAIN_NAMESPACE'])
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
