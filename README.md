# IOT-Enabled-parking-system
Submitted for IOT final codes

## To run the arduino codes

Make the following connections to avoid changing the code
- Ultra Sonic Sensor's Trigger pin to D1
- Ultra Sonic Sensor's Echo Pin to D2
- IR Sensor's Data pin to D0

After that, change the following in the code

1. Replace the password and ssid with your own network.
2. Change the thingspeak read and write api key to your own (Note: Add two data fields for both the slots).
3. Replicate the Blynk interface (Text box and Button). Add the button widget to V1 pin and text box to V3 pin. 
4. Change the Auth Code to your own Blynk project. Both NodeMCU modules will have different auth keys. 
5. Upload slot 1 and slot 2 on different NodeMCU modules. 

If you want to send the security emails from a different email, change the sender email and password to that particular acount. (Note: Currently the smtp server is set only for gmail-gmail interaction)

## To run the python code for number plate detection 

Open the terminal and run the following 

```
sudo apt-get update

sudo apt-get install libhdf5-dev -y 
sudo apt-get install libhdf5-serial-dev –y 
sudo apt-get install libatlas-base-dev –y 
sudo apt-get install libjasper-dev -y
sudo apt-get install libqtgui4 –y
sudo apt-get install libqt4-test –y

pip3 install opencv

sudo dpkg --configure –a
sudo apt-get install tesseract-ocr

pip install pytesseract
pip install pyttsx3
pip3 install imutils
```
Connect the IR sensor's Data pin to GPIO23 pin of Raspberry Pi (BCM Mode)
After installing all the libraries simply run the code. After each succesfull detection, press any key to re-run the frame. 
