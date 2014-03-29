int led = 4; // onboard debug LED
int ledState = LOW; // current LED state
long previous = 0; // last time we looped

int dirPin = 3; // direction
int dirState = LOW;
int enPin = 2; // enable
int enState = LOW;

// interval to step on
double vel = 10; // steps / msec
double maxv = 10; // steps / msec
double minv = 0.01; // steps / msec
double accel = .001; // steps / msec / msec
double c_a = -.1;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, HIGH);
  pinMode(enPin, OUTPUT);
  enState = LOW;
  digitalWrite(enPin, enState);
  Serial.begin(9600);
}

void loop() {
  unsigned long current = micros();
  unsigned long interval = (current - previous)/1000; // usec to msec
  if (vel != 0) {
    if (interval > 1/vel) {
      /*Serial.println("Step!\n"); 
      Serial.println(vel); 
      Serial.println(interval); 
      Serial.println(dirState); */
      previous = current;
      digitalWrite(led, ledState = (ledState==LOW)?HIGH:LOW);
      vel += c_a*interval;
      //Serial.println(vel); 
      if (vel < minv) {
        c_a = accel;
        vel = minv;        
        dirState = (dirState == LOW) ? HIGH : LOW;
        digitalWrite(dirPin, dirState);
      } else if (vel > maxv) {
        c_a = -accel;
      }
    }
  }
}
