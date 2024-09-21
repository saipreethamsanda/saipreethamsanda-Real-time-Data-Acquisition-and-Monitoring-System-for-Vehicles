#include <Arduino.h>
#include <DHT.h>

// Pin Definitions
#define BUTTON_PIN D3          // Pin connected to the brake button
#define WATER_SENSOR_PIN A0    // Pin connected to the water level sensor
#define DHT_PIN D2             // Pin connected to the DHT sensor
#define SENSOR_PIN D4          // Pin connected to the RPM sensor

// DHT Sensor Type
#define DHT_TYPE DHT11         // Define the type of DHT sensor (DHT11)

// Create a DHT object
DHT dht(DHT_PIN, DHT_TYPE);

// Variable Declarations
int buttonState = 0;           // Variable to store the current state of the button
int lastButtonState = HIGH;    // Variable to store the last state of the button
int waterSensorValue = 0;      // Variable to store the value from the water sensor
volatile int counter = 0;      // Counter for RPM calculation (volatile because it's used in an interrupt)
int RPM;                       // Variable to store the calculated RPM
float speedKmph;               // Variable to store the calculated speed in km/h

const float wheelCircumference = 0.5; // Circumference of the wheel in meters

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Configure pins
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // Set the brake button pin as input with internal pull-up
  pinMode(WATER_SENSOR_PIN, INPUT);   // Set the water sensor pin as input
  dht.begin();                        // Initialize the DHT sensor
  pinMode(SENSOR_PIN, INPUT);         // Set the RPM sensor pin as input

  // Attach interrupt to the RPM sensor pin
  attachInterrupt(digitalPinToInterrupt(SENSOR_PIN), count, RISING);

  // Print initialization message
  Serial.println("System Initialized");
}

void loop() {
  // Call functions to perform tasks
  checkBrakes();           // Check the state of the brake button
  readWaterLevel();        // Read the water level sensor
  readTemperature();       // Read the temperature from the DHT sensor
  calculateSpeedAndRPM();  // Calculate and display RPM and speed
  delay(1000);             // Wait for 1 second before repeating
}

// Function to check the state of the brake button
void checkBrakes() {
  buttonState = digitalRead(BUTTON_PIN);  // Read the current state of the button
  if (buttonState == LOW) {               // If the button is pressed
    Serial.println("Brakes are working");
    delay(200);                           // Debounce delay
  }
  lastButtonState = buttonState;          // Update the last button state
  delay(50);                              // Short delay to avoid bouncing
}

// Function to read the water level sensor
void readWaterLevel() {
  waterSensorValue = analogRead(WATER_SENSOR_PIN);  // Read the water sensor value
  Serial.print("Water Level Sensor Value: ");
  Serial.println(waterSensorValue);
  // Determine water level based on sensor value
  if (waterSensorValue < 100) {
    Serial.println("Water Level: Very Low");
  } else if (waterSensorValue < 150) {
    Serial.println("Water Level: Low");
  } else if (waterSensorValue < 350) {
    Serial.println("Water Level: Medium");
  } else if (waterSensorValue < 450) {
    Serial.println("Water Level: High");
  } else {
    Serial.println("Water Level: Very High");
  }
}

// Function to read the temperature from the DHT sensor
void readTemperature() {
  float temperature = dht.readTemperature();  // Read the temperature
  if (isnan(temperature)) {                   // Check if the reading is valid
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println("C");
}

// Function to calculate and display RPM and speed
void calculateSpeedAndRPM() {
  RPM = counter * 60;  // Calculate RPM based on the counter
  speedKmph = (RPM * wheelCircumference * 60) / 1000;  // Calculate speed in km/h
  Serial.print("RPM: ");
  Serial.print(RPM);
  Serial.print(" | Speed: ");
  Serial.print(speedKmph);
  Serial.println(" km/h");
  counter = 0;  // Reset the counter for the next calculation
}

// Interrupt service routine for the RPM sensor
void count() {
  counter++;  // Increment the counter
}
