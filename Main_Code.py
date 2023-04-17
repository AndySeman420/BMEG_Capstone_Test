## Andy Seman
## WVU BMEG Capstone 22-23

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

import os
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib2 import LCD_1inch47
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

def led():
	GPIO.setwarnings(False) # Ignores warnings
	GPIO.setmode(GPIO.BCM) #Sets pin numbering to Broadcom SOC channel
	GPIO.setup(21,GPIO.OUT)
	while True:
		GPIO.output(21,GPIO.HIGH)
		print("LED is ON")
		time.sleep(3)

# Raspberry pi pin configuration
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

disp = LCD_1inch47.LCD_1inch47()
disp.Init()
disp.clear()

Font1 = ImageFont.truetype("../Font/Font02.ttf",30)
Font2 = ImageFont.truetype("../Font/Font01.ttf",50)
Font3 = ImageFont.truetype("../Font/Font02.ttf",35)
Font4 = ImageFont.truetype("../Font/Font02.ttf",60)

## Welcome Screen
def Welcome_Screen():
	image1 = Image.new("RGB", (disp.width,disp.height), "WHITE")
	draw = ImageDraw.Draw(image1)

	draw.text((12,80), 'WVU', fill = "BLUE", font=Font2)
	draw.text((10,150), 'BMEG Capstone', fill = "BLUE", font=Font1)
	draw.text((7,180), '2022-2023', fill = "BLUE", font=Font3)
	draw.rectangle([(0,0),(200,40)],fill = "GOLD")
	draw.rectangle([(0,280),(300,400)],fill = "GOLD")

	image1 = image1.rotate(0)
	disp.ShowImage(image1)
	time.sleep(3)

## Confirm Screen
def Confirm_Screen():
	image2 = Image.new("RGB", (disp.width,disp.height), "WHITE")
	draw2 = ImageDraw.Draw(image2)

	draw2.text((35,90), 'Ready to', fill = "GREEN", font=Font3)
	draw2.text((20,120), 'begin test?', fill = "GREEN", font=Font3)
	draw2.text((25,200), 'Press button', fill = "GREEN", font=Font1)
	draw2.text((50,230), 'to start', fill = "GREEN", font=Font1)


	image2 = image2.rotate(0)
	disp.ShowImage(image2)

## Test Screen
def Test_Screen():
	Button = 22
	Switch = 0

	GPIO.setwarnings(False) # Ignores warnings
	GPIO.setmode(GPIO.BCM) #Sets pin numbering to Broadcom SOC channel
	GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	dataS=0
	bsold=0
	bpressed=0

	while bpressed <2:
		bs = GPIO.input(Button)
		if bs == 0 and bsold == 1:
			dataS = not dataS
			bpressed=bpressed+1
			
		if dataS == True:
			image3 = Image.new("RGB", (disp.width,disp.height), "GREEN")
			draw3 = ImageDraw.Draw(image3)

			draw3.text((35,90), 'Begin', fill = "WHITE", font=Font4)
			draw3.text((25,200), 'Press Button', fill = "WHITE", font=Font1)
			draw3.text((50,230), 'to stop', fill = "WHITE", font=Font1)

			image3 = image3.rotate(0)
			disp.ShowImage(image3)
			
		bsold=bs


## Stop Screen
def Stop_Screen():
	image4 = Image.new("RGB", (disp.width,disp.height), "RED")
	draw4 = ImageDraw.Draw(image4)

	draw4.text((35,90), 'STOP', fill = "WHITE", font=Font4)

	image4 = image4.rotate(0)
	disp.ShowImage(image4)
	time.sleep(3)

## End Screen
def End_Screen():
	image5 = Image.new("RGB", (disp.width,disp.height), "WHITE")
	draw5 = ImageDraw.Draw(image5)

	draw5.text((15,90), 'Test', fill = "GREEN", font=Font3)
	draw5.text((10,120), 'Complete', fill = "GREEN", font=Font3)

	image5 = image5.rotate(0)
	disp.ShowImage(image5)


	disp.module_exit()
	logging.info("quit:")

x = []
y = []
t = 0

## Gathers data from analog voltage source
def getdata():
	
	global x
	global y
	global t
	Button = 22
	Switch = 0
	
	GPIO.setwarnings(False) # Ignores warnings
	GPIO.setmode(GPIO.BCM) #Sets pin numbering to Broadcom SOC channel
	GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	# Create SPI bus
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
	
	# Create chip select
	cs = digitalio.DigitalInOut(board.D5)
	
	# Create mcp object
	mcp = MCP.MCP3008(spi, cs)
	
	# Create analog input channel
	chan = AnalogIn(mcp, MCP.P0)
	
	x = []
	y = []
	t = 0
	
	dataS=0
	bsold=0
	bpressed=0
	
	while bpressed <2:
		bs = GPIO.input(Button)
		if bs == 0 and bsold == 1:
			dataS = not dataS
			bpressed=bpressed+1
			
		if dataS == True:
			print("Raw ADC Value: ", chan.value)
			print("ADC Voltage: " + str(chan.voltage) + "V")
			sleep(0.1)
			volt = chan.voltage
			t = t+1
			y.append(volt)
			x.append(t)
			
		bsold=bs
		

		
		
## Creating plot of data
def plotdata():
	plt.plot(x,y)
	plt.xlabel('Time(Sec)')
	plt.ylabel('Voltage (mV)')
	plt.title("Voltage vs. Time")
	
	plt.savefig("Voltage_vs_Time_Graph.pdf")
	plt.show()
	
	
## Creating Email
def sendemail():
	
	# Creating varialbe for email address and password
	Email_Address = "BMEGRespiratory@gmail.com"
	Email_Password = "qptxhgrqpezcdprf"
	Email_Reciever = "ads0081@mix.wvu.edu"
	
	# Creating message
	msg = EmailMessage()
	msg['Subject'] = "Voltage vs. Time Graph"
	msg['From'] = Email_Address
	msg['To'] = Email_Reciever
	msg.set_content("I really hope this goes through")
	
	# Calling pdf (PDF file must be in same directory as script)
	files = ["Main_Code.py"]
	
	for file in files:
		with open(file, 'rb') as f:
			file_data = f.read()
			file_name = f.name
			
		# Attaching 1 or more PDF files to email message
		msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
		
	# Sending message
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(Email_Address, Email_Password) # logs into email server
		
		smtp.send_message(msg)
		
	print("Sent")
	
## Runner
#led()
#Welcome_Screen()
#Confirm_Screen()
#Test_Screen()
#getdata()
#Stop_Screen()
#plotdata()
sendemail()
#End_Screen()
		
from subprocess import call
#call("sudo shutdown --poweroff", shell=True)
