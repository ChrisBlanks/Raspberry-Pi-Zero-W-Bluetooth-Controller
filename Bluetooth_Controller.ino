#include <SoftwareSerial.h>
#include<LiquidCrystal.h>

const int bb_led = 8;
const int rs = 12, en = 11, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs,en,d4,d5,d6,d7);

const int buzzer = 9;
const int bluetoothTx = 2;  // TX-O pin of bluetooth mate, Arduino D2
const int bluetoothRx = 3;  // RX-I pin of bluetooth mate, Arduino D3
SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);
// bluetoothTx -> software Rx && bluetoothRx -> software Tx

const byte max_chars = 30;
char rcvd_msg[max_chars];
boolean next_msg = false;
char msg;

void setup(){
  pinMode(bb_led,OUTPUT);
  lcd.begin(16,2);
  Serial.begin(9600);  // Begin the serial monitor at 9600bps

  bluetooth.begin(115200);  // The Bluetooth Mate defaults to 115200bps
  bluetooth.print("$");  // Print three times individually
  bluetooth.print("$");
  bluetooth.print("$");  // Enter command mode
  delay(100);  // Short delay, wait for the Mate to send back CMD
  bluetooth.println("U,9600,N");  // Temporarily Change the baudrate to 9600, no parity
  // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
  bluetooth.begin(9600);  // Start bluetooth serial at 9600
}

void loop()
{
  getBluetoothMsg();
  processNewCmd();
}

//testing function
void initSimpleBluetoothMode(void){
  if(bluetooth.available()){
    msg = bluetooth.read();
    if(msg == '9'){ Serial.println("Got data!"); }
    else{ Serial.print(msg); }
  }
}

//reads a message sent over bluetooth 
void getBluetoothMsg(void){
    static boolean isReceiving = false;
    static byte index = 0;
    
    char msg_start = '<';
    char msg_end = '>';
    char rcvd;
    
    while (bluetooth.available() > 0 && next_msg == false) {
        rcvd = bluetooth.read();
        if (isReceiving == true) {
            if (rcvd != msg_end) {
                rcvd_msg[index] = rcvd;
                index++;
                if (index >= max_chars) {index = max_chars - 1;}//rewrites last index until done
            } 
            else {
                rcvd_msg[index] = '\0'; // terminate the string
                isReceiving = false;
                index = 0;
                next_msg = true;
            }
        }
        else if (rcvd == msg_start) { isReceiving = true; }
     }
 }


void processNewCmd(void) {
    if (next_msg == true) {
        Serial.print("New Message:");
        Serial.println(rcvd_msg);
        next_msg = false;
        String cmd = rcvd_msg;
        doCommand(cmd);
    }
}

void blinkLED(void){
    digitalWrite(bb_led,HIGH);
    delay(500);
    digitalWrite(bb_led,LOW);
    delay(250);
    digitalWrite(bb_led,HIGH);
    delay(500);
    digitalWrite(bb_led,LOW);
  }
  
void doCommand(String cmd){
      if(cmd == "test"){
        lcd.clear();
        lcd.print("Testing.");
        Serial.println("Blinking led now...");
        blinkLED();
        blinkLED();  
      } 
      else if(cmd == "insult"){
        lcd.clear();
        blinkLED();
        blinkLED();
        lcd.print("Your mom is fat.");
      }
      else if(cmd == "noise"){
        lcd.clear();
        lcd.print("Making noise!");
        blinkLED();
        for(int i = 0; i <20;i++){
          tone(buzzer,900+(i*20),250);
          delay(200+(i*20));
          noTone(buzzer);
        }
        for(int i = 0; i <20;i++){
          tone(buzzer,900-(i*20),250);
          delay(200+(i*20));
          noTone(buzzer);
        }
        blinkLED();
      }
      else if (cmd.startsWith("display")){
          int index_of_msg = cmd.indexOf("\'");
          String display_string = cmd.substring(index_of_msg+1,cmd.length()-1);
          lcd.clear();
          blinkLED();
          Serial.print(display_string);
          lcd.print(display_string);
      }
      else{ Serial.println("Not a known command ");}
 }
