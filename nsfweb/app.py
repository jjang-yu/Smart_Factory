import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify, make_response
from flask_socketio import SocketIO
from threading import Lock

import paramiko
import serial, time, json
import atexit

import db
#import callssh

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

lock = Lock()
ser = None

# cam 변수 설정
resultImage = None
resultColor = None
resultShape = None
resultQR = None


resultSeq = 2

def read_serial_data():
    global ser
    global resultImage, resultColor, resultShape, resultQR
    global resultSeq
    try:
        ser = serial.Serial("/dev/ttyS0", 9600, timeout=10)
        print("Serial Port Opened")
    except serial.SerialException as e:
        print(f"Cannot open serial port: {e}")
        return

    while True:
        with lock:
            if ser.in_waiting > 0:
                serial_message = ser.readline().decode('utf-8').strip()
                print(serial_message)

                time.sleep(1)

                current = db.get_current_product()
                if current:
                    if current['Status'] == 'S':
                        if serial_message == "switchR":
                            socketio.emit('update_switch', {'data': 'Red'}, namespace='/user')
                        if serial_message == "switchG":
                            socketio.emit('update_switch', {'data': 'Green'}, namespace='/user')
                        if serial_message == "switchB":
                            socketio.emit('update_switch', {'data': 'Blue'}, namespace='/user')
                        if serial_message == "switchY":
                            socketio.emit('update_switch', {'data': 'Yellow'}, namespace='/user')

                        if serial_message == "sensorCam":
                            try:
                                resultCam = execute_remote_sh('192.168.1.199', 22, 'nsf', '1234', '/home/nsf/cv_test/QR_Shape.sh')
                                json_str = resultCam.replace("'", '"')
                                data = json.loads(json_str)
                                resultQR = data['QR']
                                resultShape = data['Shape']
                                print(f"resultQR: {resultQR}, resultShape: {resultShape}")

                                resultCam2 = execute_remote_sh('192.168.1.199', 22, 'nsf', '1234', '/home/nsf/cv_test/Detect.sh')
                                json_str = resultCam2.replace("'", '"')
                                data = json.loads(json_str)
                                resultImage = data['Image']
                                resultColor = data['Color']

                                resultColor = resultColor.replace("Z", "G").replace("B.", "B")

                                print(f"resultImage: {resultImage}, resultColor: {resultColor}")
                            except json.JSONDecodeError as err:
                                print(f"decode error : {err}")
                                #pass
                            finally:
                                ser.write(f'forceStart:{resultQR}\n'.encode())

                        #if serial_message.startswith('robot'):
                        #    print(f'return: {serial_message}')
                        #    ser.write(b'robotQ\n')

                        if serial_message == "restart":
                            print("restart in")
                            time.sleep(2)
                            ser.write(b'convayorStart\n')

                        if serial_message == "sensorRobot":
                            print('sensorRobot in')
                            socketio.emit('update_error', {'data': '1'}, namespace='/user')

                            if resultQR is None or resultQR == '':
                                ser.write(b'robotQ\n')
                            elif resultShape is None or resultShape == '':
                                ser.write(b'robotE\n')
                            elif resultImage is None or resultImage == '':
                                ser.write(b'robotI\n')
                            elif resultColor is None or resultColor == '':
                                ser.write(b'robotC\n')
                            else:
                                ser.write(b'robotQ\n')


                        if serial_message.startswith('servo'):
                            print(f'return: {serial_message}')
                            time.sleep(5)
                            ser.write(f'{serial_message}:off\n'.encode())
                    else:
                        if serial_message.startswith('servo'):
                            print(f'return2: {serial_message}')
                            time.sleep(1)
                            ser.write(f'{serial_message}:off\n'.encode())

                        if serial_message.startswith('switch'):
                            print(f'return2: {serial_message}')
                            socketio.emit('serial_data', {'message':serial_message}, namespace='/admin')


                eventlet.sleep(0)

            time.sleep(0.1)

@socketio.on('send_serial_data')
def handle_send_serial_data(data):
    global ser
    print(f"send_serial_data : {data}")
    ser.write(f'{data}\n'.encode())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    current = db.get_current_product()
    return render_template('user.html', current = current)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/get_serial_data')
def get_serial_data():
    global serial_message
    print(f"get_serial_data : {serial_message}")
    return serial_message


@app.route('/start_classification', methods=['POST'])
def start_classification():
    data = request.get_json()
    goalRed = data.get('goalRed', 0)
    goalGreen = data.get('goalGreen', 0)
    goalBlue = data.get('goalBlue', 0)
    goalYellow = data.get('goalYellow', 0)

    db.start_product_classification(goalRed, goalGreen, goalBlue, goalYellow)
    return jsonify({"message": "Classification started successfully"})

@app.route('/pause_classification', methods=['POST'])
def pause_classification():
    db.pause_product_classification()
    return jsonify({"message": "Classification paused successfully"})

@app.route('/finish_classification', methods=['POST'])
def finish_classification():
    db.finish_product_classification()
    return jsonify({"message": "Classification finished successfully"})

@app.route('/update_product', methods=['POST'])
def update_product():
    data = request.get_json()
    columnName = data.get('columnName', '')
    count = data.get('count', 0)

    db.update_product_count(columnName, count)
    return jsonify({"message": "Update Product Count successfully"})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('connect', namespace='/user')
def handle_connect():
    print('Client connected to /user namespace')

@socketio.on('connect', namespace='/admin')
def handle_connect():
    print('Client connected to /admin namespace')

@socketio.on('sendTestStatus')
def handle_sendTestStatus(data):
    global ser
    message = data['message']
    print('Received data from client:', message)

    ser.write(f'{message}\n'.encode())

def execute_remote_sh(ssh_host, ssh_port, ssh_user, ssh_password, remote_script_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)
    stdin, stdout, stderr = client.exec_command(f'bash {remote_script_path}')
    output = stdout.read().decode()
    client.close()
    return output

def shutdown_handler():
    db.pause_product_classification()
    print('server shutdown')

atexit.register(shutdown_handler)

if __name__ == '__main__':
    read_serial_data_thread = eventlet.spawn(read_serial_data)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)


