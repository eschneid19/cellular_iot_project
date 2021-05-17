"""
Created 6/29/2020
By Erik Schneider
Testing pyserial and AT commands
"""

import serial
import io

"""Open the serial port"""
ser = serial.Serial(port = '/dev/ttyUSB2',\
                    baudrate = 115200,\
                    rtscts = False,\
                    parity = serial.PARITY_NONE,\
                    stopbits = serial.STOPBITS_ONE,\
                    bytesize = serial.EIGHTBITS,\
                    timeout = 0)

def at_print(output):
    """This funtion cleans up and prints the AT outputs"""

    cleaned = str(output.strip(), 'utf-8')
    print(cleaned)

def at_send(command):
    """format and sends AT commands to modem"""

    ser.write(bytes(command+'\r','ascii'))

def serial_output():
    """This funtion prints the serial output"""

    while True: 
        result = ser.readline()
        if result != b'' and result != b'\r\n':  #formatting characters
            if result == b'OK\r\n' or result == b'ERROR\r\n': #all outputs end
                at_print(result)                              #with OK or ERROR
                print('')
                break
            else:
                at_print(result)
                
def check_sim():
    """ This funtion checks if the SIM card is inserted"""

    at_send("AT+QSIMSTAT?")
    serial_output()     #may have to manually put serial output code in each
                        #function to put output in readable terms
                
def network_registration():
    """Checks whether the SIM is registered onto a network and also returns
        the lac, cid, and technology"""

    at_send("AT+CREG?")
    serial_output()

def ps_attachment():
    """Returns the status of ps (data) registration and gives option to
    either attach or detach"""

    choice = ''
    at_send("AT+CGATT?")
    serial_output()
    print("What would you like to do? \n \
    1) Attach to PS \n \
    2) Detach from PS \n \
    3) Exit \n")
    while True:
        choice = input("Input selection: ")
        print('')
        if choice == '1':
            at_send("AT+CGATT=1")
            serial_output()
            break
        elif choice == '2':
            at_send("AT+CGATT=0")
            serial_output()
            break
        elif choice == '3':
            break
        else:
            print("Invalid selection, please try again")

def debug_mode():
    """This function turns the debug mode on/off
    which will either print all the info from the serial port
    or just the user-friendly answer"""

    global debug
    debug = not(debug)
    print(debug)

def sms_format():
    """This function sets the format used for
    reading and sending messages"""
    
    at_send("AT+CMGF?")
    serial_output()
    print("What would you like to do? \n \
    1) Set to Text mode \n \
    2) Set to PDU mode \n \
    3) Exit \n")
    while True:
        choice = input("Input selection: ")
        print('')
        if choice == '1':
            at_send("AT+CMGF=1")
            serial_output()
            break
        elif choice == '2':
            at_send("AT+CMGF=0")
            serial_output()
            break
        elif choice == '3':
            break
        else:
            print("Invalid selection, please try again")

def storage_location():
    """This function checks the preffered message storage location"""

    at_send("AT+CPMS?")
    serial_output()
    
    
    
debug = True            #Default show all info from serial port

print("Connected to: " + ser.portstr)

options = {1 : check_sim,
           2 : network_registration,
           3 : ps_attachment,
           4 : sms_format,
           5 : storage_location,
           9 : debug_mode}

while True:     #Run loop for user
    choice = ''
    print("What would you like to do?\n \
    1) Check Sim Card Status\n \
    2) Check Network Registration Status \n \
    3) Check/Change PS Attachment \n \
    4) Set SMS Message Format \n \
    5) Check Message Storage Location \n \
    9) Turn On/Off Debug Mode \n \
    0) Exit")
    choice = input("Input number of choice: ")
    print('')
    if choice == '0':
          print('Goodbye!')
          break
    options[int(choice)]()

ser.close()
        
