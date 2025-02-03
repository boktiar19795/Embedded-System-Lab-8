import RPi.GPIO as GPIO
import time

RoAPin = 11    # pin11	-> Connected to CLK
RoBPin = 12    # pin12	-> Connected to DT
RoSPin = 13    # pin13	-> Connected to SW

globalCounter = 0

flag = 0
Last_RoB_Status = 0    # two variables for pin B’s value	
Current_RoB_Status = 0		

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RoAPin, GPIO.IN)    # input mode
    GPIO.setup(RoBPin, GPIO.IN)
    GPIO.setup(RoSPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Bottom pin
    rotaryClear()

def rotaryDeal():
    global flag
    global Last_RoB_Status
    global Current_RoB_Status
    global globalCounter
    Last_RoB_Status = GPIO.input(RoBPin)    # Read in data from DT
    while not GPIO.input(RoAPin):
        Current_RoB_Status = GPIO.input(RoBPin)
        flag = 1
    if flag == 1:
        flag = 0
        if Last_RoB_Status == 0 and Current_RoB_Status == 1:
            globalCounter = globalCounter + 1
            print('globalCounter = %d' % globalCounter)
        if Last_RoB_Status == 1 and Current_RoB_Status == 0:
            globalCounter = globalCounter - 1
            print('globalCounter = %d' % globalCounter)

def clear(ev=None):
    global globalCounter
    globalCounter = 0
    print('globalCounter = %d' % globalCounter)
    time.sleep(1)

def rotaryClear():
    GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) 	
    # wait for falling

def loop():
    while True:
        rotaryDeal()

def destroy():
    GPIO.cleanup()             # Release resource

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
        destroy()
