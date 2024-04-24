from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import SocketIO
from threading import Thread, Lock
import time
import serial

import callssh

app = Flask(__name__)
app.config['DEBUG'] = False
socketio = SocketIO(app)

ser = None
serial_message = ""
lock = Lock()

class SerialReadProgram(Thread):
    def __init__(self):
        super().__init__()
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global ser
        global serial_message
        if ser is None or not ser.is_open:
            ser = serial.Serial("/dev/ttyS0", 9600, timeout=2)
            print("Serial Port Opened")
        else:
            print("Serial Port Already Opened")
        print("Serial Start")
        i = 0
        while self._running:
            with lock:
                try:
                    if ser.in_waiting > 0:
                        serial_message = ser.readline().decode('utf-8').strip()
                        print(serial_message)
                        socketio.emit('newdata', {'data': serial_message})
                        
                        # 
                        if serial_message == "sensor cam" or serial_message == "sensor robot":
                        ser.write(b'sensor start\n')
                        time.sleep(1)
                            #call_action_cam()
                        
                except serial.SerialException as e:
                    print(f"Serial Port Error: {e}")
                    time.sleep(0.5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/serial_data')
def get_serial_data():
    global serial_message
    return jsonify({'data': serial_message})

@app.route('/call_action_cam')
def call_action_cam():
    remote_script_path = '/home/nsf/opencv-venv/opencv/samples/python/test.sh'
    result = callssh.execute_remote_sh('192.168.1.92', 22, 'nsf', '1234', remote_script_path)
    response = make_response(jsonify({'data': result}))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response
    

if __name__ == '__main__':
    serial_read = SerialReadProgram()
    serial_read.start()

    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    # app.run(host='0.0.0.0', port=5000, debug=False)



