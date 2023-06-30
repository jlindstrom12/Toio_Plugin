from flask import Flask, render_template
from flask_socketio import SocketIO

import asyncio

from toio.scanner import BLEScanner
from toio.cube import ToioCoreCube


app = Flask(__name__)
#pp.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True

socketio = SocketIO(app, cors_allowed_origins="*")

async def connect_toio():
    dev_list = await BLEScanner.scan(num=1)
    if len(dev_list) > 0:
        cube = ToioCoreCube(dev_list[0].interface)
        await cube.connect()
        print("Connected")
        await asyncio.sleep(1)
        await cube.disconnect()
        print("Disconnected")
    else:
        print("No cubes found")


@app.route('/index')
def index():
    print("Loading index...")
    return render_template('index.html')

@socketio.on('connect-toio')
def handle_message():
    print("received message: ")
    asyncio.run(connect_toio())

if __name__ == '__main__':
    
    socketio.run(app, port=9000)