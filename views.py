from flask import Blueprint, request, flash, jsonify, render_template
from flask_login import login_required, current_user
from . import db
import pymodbus
from pymodbus.client import ModbusSerialClient as ModbusClient
import json
from pymodbus.client import ModbusTcpClient as tcp

views = Blueprint('views', __name__)


# @views.route('/', methods=['GET','POST'])
# @login_required
# def pt100():
#     return render_template("pt100.html", user=current_user)

def setClient(ip_address):
    client = tcp(ip_address)
    return client

@views.route('/', methods=['GET','POST'])
@login_required
def connect_rs854_pt100():
    print("I am in the function")
    #client = ModbusClient(method='rtu', port='COM9', baudrate=19200,timeout=0.1)
    client = setClient('10.3.47.243')
    print(client.connect())

    try:
        read = client.read_holding_registers(address=0, count=8, slave=4)
        Ch0 = round(read.registers[0]*0.1,1)
        Ch1 = round(read.registers[1]*0.1,1)
        Ch2 = round(read.registers[2]*0.1,1)
        Ch3 = round(read.registers[3]*0.1,1)
        Ch4 = round(read.registers[4]*0.1,1)
        Ch5 = round(read.registers[5]*0.1,1)
        Ch6 = round(read.registers[6]*0.1,1)
        Ch7 = round(read.registers[7]*0.1,1)
        
    except:
        print("Error in connection slave 4")
        Ch0 = 26.9
        Ch1 = 25.4
        Ch2 = 26.4
        Ch3 = 27.3
        Ch4 = 29.1
        Ch5 = 26.5
        Ch6 = 23.5
        Ch7 = 28.3
    client.close()   

    context = {
        "temperature_Ch0":json.dumps(Ch0),
        "temperature_Ch1":json.dumps(Ch1),
        "temperature_Ch2":json.dumps(Ch2),
        "temperature_Ch3":json.dumps(Ch3),
        "temperature_Ch4":json.dumps(Ch4),
        "temperature_Ch5":json.dumps(Ch5),
        "temperature_Ch6":json.dumps(Ch6),
        "temperature_Ch7":json.dumps(Ch7),
        
    }

    return render_template('pt100.html', **context) 