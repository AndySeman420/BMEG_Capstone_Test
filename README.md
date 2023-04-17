# BMEG_Capstone_Test
# Creator: Andy Seman
# Created: 4/16/2023

Hello, this is a code to operate the Breath'o Metric (Temporary name) remote testing device
This code will gathered by a sensor, graph it, and then email the graph to a specified email address

Please use these commands to download the rest of the required code

sudo apt-get install unzip -y
sudo wget https://www.waveshare.com/w/upload/8/8d/LCD_Module_RPI_code.zip
sudo unzip ./LCD_Module_RPI_code.zip 
cd LCD_Module_RPI_code/RaspberryPi/
(After downloading these files you must place the files 'lib' and 'Font' that are located within the LCD_Module... folder in the directory directly above the the one where the Main_Code.py is located)

sudo pip3 install adafruit-circuitpython-mcp3xxx
sudo pip3 install matplotlib
sudo apt-get install libatlas-base-dev
