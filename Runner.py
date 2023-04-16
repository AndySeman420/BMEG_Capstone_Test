import busio
import digitalio
import board
import time
from time import sleep
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import os
import smtplib
import imghdr
from email.message import EmailMessage
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

GPIO.setwarnings(False)  # Ignores warnings
GPIO.setmode(GPIO.BCM)  # Sets pin numbering to Broadcom SOC channel

x = []
y = []

t = 0

## Power Light
ledPOW = 13
while True:
    GPIO.setup(ledPOW, GPIO.OUT)
    GPIO.output(ledPOW, GPIO.HIGH)
    break


## Gathers Data from Analog voltage source
def getdata():
    global t
    global x
    global y
    Button = 22


    GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)

    x = []
    y = []

    t = 0

    # Loop that prints voltages values and adds them to x array
    while True:
        if GPIO.input(Button) == GPIO.HIGH:
            print("Raw ADC Value: ", chan.value)
            print("ADC Voltage: " + str(chan.voltage) + "V")
            sleep(0.5)
            volt = chan.voltage
            t = t + 1
            y.append(volt)
            x.append(t)


## Creating Plot of Data
def plotdata():
    plt.plot(x, y)
    plt.xlabel('Time (Sec)')
    plt.ylabel('Voltage (mV)')
    plt.title("Voltage vs. Time")

    plt.savefig("Voltage_vs_Time_Graph.pdf")
    plt.show()


## Creating Email
def sendemail():
    # Creating variables for email address and password
    Email_Address = "BMEGRespiratory@gmail.com"
    Email_Password = 'qptxhgrqpezcdprf'  # input("Input Email Password")
    Email_Reciever = "example@gmail.com"

    # Creating message
    msg = EmailMessage()
    msg['Subject'] = "Voltage vs. Time Graph"
    msg['From'] = Email_Address
    msg['To'] = Email_Reciever
    msg.set_content('Here is a voltage vs. time graph sent through python.')

    # Calling pdf  (PDF file must be in same directory as script)
    files = ['Voltage_vs_Time_Graph.pdf']

    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name

        # Attaching 1 or more PDF files to email
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Sending message
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Email_Address, Email_Password)  # logs us into email server

        smtp.send_message(msg)

    print("Sent")


# Run
getdata()
plotdata()
sendemail()