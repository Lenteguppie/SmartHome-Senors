#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "DHT.h"
#include "Secrets.h"

#include <WiFiClientSecureBearSSL.h>
// Fingerprint for demo URL, expires on June 2, 2021, needs to be updated well before this date
const uint8_t fingerprint[20] = {0x40, 0xaf, 0x00, 0x6b, 0xec, 0x90, 0x22, 0x41, 0x8e, 0xa3, 0xad, 0xfa, 0x1a, 0xe8, 0x25, 0x41, 0x1d, 0x1a, 0x54, 0xb3};

// Uncomment one of the lines below for whatever DHT sensor type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT21   // DHT 21 (AM2301)
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

/*Put your SSID & Password*/
const char* ssid = SECRET_SSID;  // Enter SSID here
const char* password = SECRET_PASS;  //Enter Password here

// Replace with your unique Thing Speak WRITE API KEY
const char* apiKey = SECRET_WRITE_APIKEY;

const char* resource = "/update?api_key=";

// Thing Speak API server 
const char* server = "api.thingspeak.com";

// Temporary variables
static char temperatureTemp[7];
static char humidityTemp[7];

// DHT Sensor
#define DHTPin 14

// Initialize DHT sensor.
DHT dht(DHTPin, DHTTYPE);

float Temperature;
float Humidity;

// Make an HTTP request to Thing Speak
void makeHTTPRequest() {

  Temperature = dht.readTemperature(); // Gets the values of the temperature
  Humidity = dht.readHumidity(); // Gets the values of the humidity
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    strcpy(temperatureTemp,"Failed");
    strcpy(humidityTemp, "Failed");
    return;    
  }
  else {
    // Computes temperature values in Celsius + Fahrenheit and Humidity
    float hic = dht.computeHeatIndex(t, h, false); 
    // Comment the next line, if you prefer to use Fahrenheit      
    dtostrf(Temperature, 6, 2, temperatureTemp);
                  
          
    dtostrf(Humidity, 6, 2, humidityTemp);

  }
  
  Serial.print("Connecting to "); 
  Serial.print(server);
  
  WiFiClient client;
  int retries = 5;
  while(!!!client.connect(server, 80) && (retries-- > 0)) {
    Serial.print(".");
  }
  Serial.println();
  if(!!!client.connected()) {
     Serial.println("Failed to connect, going back to sleep");
  }
  
  Serial.print("Request resource: "); 
  Serial.println(resource);
  client.print(String("GET ") + resource + apiKey + "&field1=DHT1&field2=0001&field4=" + humidityTemp + "&field3=" + temperatureTemp +
                  " HTTP/1.1\r\n" +
                  "Host: " + server + "\r\n" + 
                  "Connection: close\r\n\r\n");
                  
  int timeout = 5 * 10; // 5 seconds             
  while(!!!client.available() && (timeout-- > 0)){
    delay(100);
  }
  if(!!!client.available()) {
     Serial.println("No response, going back to sleep");
  }
  while(client.available()){
    Serial.write(client.read());
  }
  
  Serial.println("\nclosing connection");
  client.stop();
}

void setup() {
  Serial.begin(115200);
  delay(100);

  pinMode(DHTPin, INPUT);

  dht.begin();

  Serial.println("Connecting to ");
  Serial.println(ssid);

  //connect to your local wi-fi network
  WiFi.begin(ssid, password);

  //check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  // Verbonden.
  Serial.println("WIFI CONNECTED!");

  // Access Point (SSID).
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // IP adres.
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Signaalsterkte.
  long rssi = WiFi.RSSI();
  Serial.print("Signaal sterkte (RSSI): ");
  Serial.print(rssi);
  Serial.println(" dBm");
  Serial.println("");


}

void loop() {
 

//  Serial.print("Temperature: ");
//  Serial.println(Temperature);
//  Serial.print("Humidity: ");
//  Serial.println(Humidity);
//  //  String URL = "https://api.thingspeak.com/update?api_key=" + SECRET_WRITE_APIKEY + "&field1=" + SENSOR_NAME + "&field2=" + SENSOR_ID + "&field3=" + Temperature + "&field4=" + "&field4=" Humidity;
//  String URL = "https://api.thingspeak.com/update?api_key=";
//  URL += SECRET_WRITE_APIKEY;
//  URL += "&field1=";
//  URL += SENSOR_NAME;
//  URL += "&field2=";
//  URL += SENSOR_ID;
//  URL += "&field3=";
//  URL += String(Temperature);
//  URL += "&field4=";
//  URL += String(Humidity);
//  Serial.println(URL);

  makeHTTPRequest();

//  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
//
//    std::unique_ptr<BearSSL::WiFiClientSecure>client(new BearSSL::WiFiClientSecure);
//
//    client->setFingerprint(fingerprint);
//
//    HTTPClient https;
//
//    Serial.print("[HTTPS] begin...\n");
//    if (https.begin(*client, URL)) {  // HTTPS
//
//      Serial.print("[HTTPS] GET...\n");
//      // start connection and send HTTP header
//      int httpCode = https.GET();
//
//      // httpCode will be negative on error
//      if (httpCode > 0) {
//        // HTTP header has been send and Server response header has been handled
//        Serial.printf("[HTTPS] GET... code: %d\n", httpCode);
//
//        // file found at server
//        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
//          String payload = https.getString();
//          Serial.println(payload);
//        }
//      } else {
//        Serial.printf("[HTTPS] GET... failed, error: %s\n", https.errorToString(httpCode).c_str());
//      }
//      https.end();
//    }
//  } else {
//    Serial.println("Error in WiFi connection");
//  }
  delay(10000); //Send a request every 60 seconds
}
