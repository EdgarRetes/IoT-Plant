#include <WiFi.h>
#include <HTTPClient.h>
#include <LiquidCrystal.h>
#include <DHTesp.h>

// Conexion a Ubidots
const char *WIFI_SSID = "Tec-IoT";     
const char *WIFI_PASS = "spotless.magnetic.bridge";
const char *UBIDOTS_TOKEN = "BBUS-CCfJC6iG3YCoXz9IJESjsb9VPJuOJV";     
const char *DEVICE_LABEL = "IoT_Plant";
const char *VARIABLE_LABEL_1 = "Temperatura"; 
const char *VARIABLE_LABEL_2 = "Humedad-Relativa"; 
const char *VARIABLE_LABEL_3 = "Humedad-Tierra"; 

// Conexion del circuito
LiquidCrystal lcd(22, 23, 5, 18, 19, 21);
int pinDHT = 25;
DHTesp dht;
int distancia = 0;
int contador = 0;
int pinEcho = 32;
int pinTrig = 33;
int pinHum = 34;
int pinBuzzer = 26;
int pinLED1 = 4;
int pinLED2 = 2;

// Función para obtener la distancia del sensor de ultrasonido
long leerDistanciaUltrasonido(int pinTrigger, int pinEcho) {
  pinMode(pinTrigger, OUTPUT);
  digitalWrite(pinTrigger, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrigger, LOW);
  pinMode(pinEcho, INPUT);
  return pulseIn(pinEcho, HIGH);
}

// Función para centrar los mensajes en la pantalla LCD
void printCentered(String text, int row) {
  int padding = (16 - text.length()) / 2;
  lcd.setCursor(padding, row);
  lcd.print(text);
}

// Función para enviar datos a Ubidots
void enviarDatosUbidots(float temp, float humRelativa, float humTierra) {
  HTTPClient http;
  String url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + String(DEVICE_LABEL) + "/";
  http.begin(url); 
  http.addHeader("Content-Type", "application/json"); 
  http.addHeader("X-Auth-Token", UBIDOTS_TOKEN); 

  // Formar el cuerpo del mensaje JSON con las 3 variables
  String jsonData = "{\"" + String(VARIABLE_LABEL_1) + "\": " + String(temp) +
                    ", \"" + String(VARIABLE_LABEL_2) + "\": " + String(humRelativa) +
                    ", \"" + String(VARIABLE_LABEL_3) + "\": " + String(humTierra) + "}";

  int httpResponseCode = http.POST(jsonData); 

  if (httpResponseCode > 0) {
    String response = http.getString();  
    Serial.println("Datos enviados a Ubidots");
    Serial.println("Respuesta: " + response);
  } else {
    Serial.println("Error enviando los datos a Ubidots: " + String(httpResponseCode));
  }

  http.end(); 
}

void setup() {
  // Inicio del circuito
  Serial.begin(115200);
  lcd.begin(16, 2);
  dht.setup(pinDHT, DHTesp::DHT11);
  pinMode(pinBuzzer, OUTPUT);
  pinMode(pinLED1, OUTPUT);
  pinMode(pinLED2, OUTPUT);  

  lcd.clear();
  printCentered("!BIENVENIDO!", 0);
  for (int i = 0; i < 16; i++) {
    lcd.scrollDisplayRight();
    delay(300);
  }
  
  lcd.clear();
  printCentered("INICIANDO...", 0);
  digitalWrite(pinLED1, HIGH);
  delay(500);
  digitalWrite(pinLED1, LOW);
  delay(500);
  
  lcd.clear();
  lcd.setCursor(0, 1);
  tone(pinBuzzer, 262);
  delay(500);
  tone(pinBuzzer, 294);
  delay(500);
  tone(pinBuzzer, 330);
  delay(500);
  tone(pinBuzzer, 350);
  delay(500);
  tone(pinBuzzer, 380);
  delay(500);  
  noTone(pinBuzzer);
  digitalWrite(pinLED2, HIGH);

  // Conectar a WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConectado a WiFi");
}

void loop() {
  TempAndHumidity datos = dht.getTempAndHumidity();
  distancia = 0.01723 * leerDistanciaUltrasonido(pinTrig, pinEcho);
  Serial.print("Distancia: ");
  Serial.print(distancia);
  Serial.println(" cm");
  int sensorHumedad = analogRead(pinHum);
  float humedadTierra = (sensorHumedad / 4095.0) * 100;
  
  if (distancia < 15) {
    contador++;
    if (contador > 3) {
      contador = 0;
    }
  }
  
  lcd.clear();
  if (contador == 0) {
    printCentered("CRECIENDO VIDA", 0);
    printCentered("CON ARMONIA", 1);
  } 
  else if (contador == 1) {
    printCentered("TEMPERATURA", 0);
    printCentered(String(datos.temperature, 2) + " C", 1);
  } 
  else if (contador == 2) {
    printCentered("HUMEDAD RELATIVA", 0);
    printCentered(String(datos.humidity, 2) + " %", 1);
  }
  else if (contador == 3){
    printCentered("HUMEDAD TIERRA", 0);
    printCentered(String(humedadTierra) + " %", 1);
  } 

  // Alerta por humedad
  if (datos.humidity < 20 || datos.humidity > 70) {
    lcd.clear();
    digitalWrite(pinLED1, HIGH); 
    tone(pinBuzzer, 1000);
    delay(1000);
    noTone(pinBuzzer);
    digitalWrite(pinLED1, LOW);
    digitalWrite(pinLED2, LOW);
    printCentered("ALERTA HUMEDAD!", 0);
    printCentered(String(datos.humidity, 2) + " %", 1);
  }

  // Alerta por temperatura
  if (datos.temperature < 20 || datos.temperature > 30) {
    lcd.clear();
    digitalWrite(pinLED1, HIGH); 
    tone(pinBuzzer, 1000);
    delay(1000);
    noTone(pinBuzzer);
    digitalWrite(pinLED1, LOW);
    digitalWrite(pinLED2, LOW);
    printCentered("ALERTA TEMP!", 0);
    printCentered(String(datos.temperature, 2) + " C", 1);
  }

  // Enviar los datos a Ubidots
  enviarDatosUbidots(datos.temperature, datos.humidity, humedadTierra);

  delay(1500);
  lcd.clear();
}
