int led = 13; // onboard debug LED
int ledState = LOW; // current LED state
long previous = 0; // last time we looped

int dirPin = 12; // direction
int dirState = LOW;
int enPin = 11; // enable
int enState = LOW;

// interval to step on
double interval = 5;
double accel = .1; // 1 or -1

void setup() {
  pinMode(led, OUTPUT);
  pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, HIGH);
  pinMode(enPin, OUTPUT);
  enState = LOW;
  digitalWrite(enPin, enState);
}

void loop() {
  unsigned long current = millis();
  if (current - previous > interval) {
    previous = current;
    digitalWrite(led, ledState = (ledState==LOW)?HIGH:LOW);
    interval += accel;
    if (interval < 1) {
      accel = .1;
      dirState = (dirState == LOW) ? HIGH : LOW;
      digitalWrite(dirPin, dirState);
    } else if (interval > 25) {
      accel = -.1;
    }
  }
}
