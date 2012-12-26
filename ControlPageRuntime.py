from flask import Flask, render_template
import time
from BurnerLogic import BurnerLogic
from UsbCard import UsbCard

app = Flask(__name__)

ioCard = UsbCard("COM1", 9600)
burner = BurnerLogic(ioCard, time.sleep)

burner.Delay = 1
burner.FanTime = 0.2
burner.ScrewTime = 0.1

burner.FanTerminalName = "5T1"
burner.ScrewTerminalName = "3.T2"

def Routine():
    pass

@app.route('/')
def hello_world():
    msg = ""
    try:
        burner.Execute()
    except Exception as ex:
        msg = ex

    return render_template('index.html', message = msg)

if __name__ == '__main__':
    app.run()
