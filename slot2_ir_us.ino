// Libraries 
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <EMailSender.h>
#include <ThingSpeak.h>;

//Pins
const int trigPin = 5;  //D1
const int echoPin = 4;  //D2
const int irsensor = 16; //D0

BlynkTimer timer;

// defines variables
long duration;
int distance;
int dist = 2;
int button_state = 0;
String email = "dummy@gmail.com";

const char* apiWritekey = "9OQ23QSE0BKSS0O1";
const char* server = "api.thingspeak.com";
unsigned long channelnumber = 1603600;

char auth[] = "Rs-6lpuooSG_IBwXtGeJjGQhrsubtNXl";
char ssid[ ] = "samsungA50";
char pass[ ] = "tanmay123";
WiFiClient client;
EMailSender emailSend("secureparking053iot@gmail.com","tanmay053");

void ir(){
  int state = digitalRead(irsensor);
  if(state == LOW){
    ThingSpeak.writeField(channelnumber, 2, state , apiWritekey);
    Serial.println("Slot 2 is full");
    ultra_sonic();
  }
  else {
    ThingSpeak.writeField(channelnumber, 2, state , apiWritekey);
    Serial.println("Slot 2 is empty");
  }
}

BLYNK_WRITE(V1){
  button_state = param.asInt(); //get the button state from blynk app
}

BLYNK_WRITE(V3){
  email = param.asStr();
}

void ultra_sonic(){
  if(button_state == 1){
  
  // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    long duration = pulseIn(echoPin, HIGH);

    // Calculating the distance
    int distance= duration*0.034/2;
    
    if(dist > distance+2 || dist < distance-2){
      Serial.println("Your car is moving from the slot");
      send_email();
      delay(1000);
    }
    else{
      Serial.println("You car is parked safely");
    }
    dist = distance;
    delay(3000);
  }
  else{
    Serial.println("Waiting for car to park");
  }
}
 

void send_email(){
    EMailSender::EMailMessage message;
    message.subject = "Security Alert";
    message.message = "You vehicle in moving from the slot. Please contact the secuirty gaurd if you are not in the vehicle";
 
    EMailSender::Response resp = emailSend.send(email.c_str(), message);
 
    Serial.println("Sending status: ");
 
    Serial.println(resp.status);
    Serial.println(resp.code);
    Serial.println(resp.desc);
}

void setup() {
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
pinMode(irsensor, INPUT); //IR sensor input
Serial.begin(9600); // Starts the serial communication
Blynk.begin(auth, ssid, pass);
ThingSpeak.begin(client);
timer.setInterval(3000L, ir);
}

void loop() {
  Blynk.run();
  timer.run();
}
