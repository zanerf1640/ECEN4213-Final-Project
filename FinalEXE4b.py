#This is a basic script to host a webpage at the IP specified
# By the 'IP_Address' variable

# Import library to create webserver to host webpage
from flask import Flask, render_template
from flask import Flask, render_template, Response,redirect,request, url_for
import itertools
# import time
from camera_pi import Camera
import socket
import time
from threading import Thread
import threading

app = Flask(__name__)


server_address_1 =  ('127.0.0.2', 8001)
sock_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_1.bind(server_address_1)



server_address =  ('127.0.0.1', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(5)
connection, address = sock.accept()


#Find the IP Address of your device
#Use the 'ifconfig' terminal command, the address should be in the format  "XX.XXX.XXX.XXX"
IP_Address = '10.227.13.100'
PORT = 8080
#Connect the *.html page to the server and run as the default page
bumper_data = "b0c0d0"

def receive_bumper_data():
    global bumper_data
    while True:
        try:
            data = connection.recv(1024).decode('utf-8')
            if data:
                bumper_data = data.strip()
                print("Received bumper data:", bumper_data)
        except Exception as e:
            print("Socket read error:", e)
            break

threading.Thread(target=receive_bumper_data, daemon=True).start()

@app.route('/joystick')
def joystick():
    x = float(request.args.get('x', 0))
    y = float(request.args.get('y', 0))
    cmd = f"j{x:.2f} {y:.2f}"
    connection.send(cmd.encode('utf-8'))
    return render_template('Joystick.html')


@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            global bumper_data
            while True:
                yield f"data: {bumper_data}\n\n"
                time.sleep(0.5)
        return Response(events(), content_type='text/event-stream')
    return render_template('FinalEXE3.html')



    
def gen(camera):
    max_len = 65507
    frame = ''
    while True:
        # receive image to the client: frame = .....
        frame,_ = sock_1.recvfrom(max_len)

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')


def launch_socket_server(connection):
    global info, frame
    print('Listening...')
    a='b0c0d0'
    while True:        
        info = connection.recv(6).decode("utf-8")
        print('info:', info)
        if info != a and len(info)>0:
            a = info


@app.route('/UpFunction')
def UpFunction():
    print('In UpFunction')
    cmd = 'u'
    connection.send(cmd.encode('utf-8'))  
    return "None"

# define the rest of the functions to handle the left, right, down and stop buttons (4 functions)
@app.route('/LeftFunction')
def LeftFunction():
    cmd = 'l'
    connection.send(cmd.encode('utf-8'))
    print('In LeftFunction')
    return "Left"

@app.route('/RightFunction')
def RightFunction():
    cmd = 'r'
    connection.send(cmd.encode('utf-8'))
    print('In RightFunction')
    return "Right"

@app.route('/StopFunction')
def StopFunction():
    cmd = 's'
    connection.send(cmd.encode('utf-8'))
    print('In StopFunction')
    return "Stop"

@app.route('/DownFunction')
def DownFunction():
    cmd = 'd'
    connection.send(cmd.encode('utf-8'))
    print('In DownFunction')
    return "Down"

#Start the server
if __name__ == "__main__":
    t = Thread(target=launch_socket_server,args=(connection,))
    t.daemon = True
    t.start()

    app.run(debug=True, host=IP_Address, port=PORT, use_reloader=False)