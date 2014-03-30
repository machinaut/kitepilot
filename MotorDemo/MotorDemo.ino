#define POWER_SAVE_BS 1

const int led = 4; // onboard debug LED
int ledState = LOW; // current LED state
long previous_step = 0; // last time we stepped the motor (us)
long previous_accel = 0; // last time we changed velocity (us)
long previous_ctrl = 0; // last time we ran control (us)

const int dirPin = 3; // direction
int dirState = LOW;
const int enPin = 2; // enable

const int potPin = 0;

const int PwrPin = 9;

const int stop1Pin = 5;
const int stop2Pin = 6;
long stop1Pos = 0;
long stop2Pos = 0;
boolean got1 = false; // got stop1 first (true means stop1 is positive)

long pos = 0;
long goalp = 0; 

// "ups" stands for "usec per step", basically 1/velocity
long usec_per_step = 0; // 0 is special and means stop
long goal_ups = 0; // current goal
const long max_ups = 1700; // min speed before stopping
const long min_ups = 500; // max speed
const long usec_per_ups = 200; // "acceleration?" (usec / (usec/step))
const long usec_per_ctrl = 100000; // control rate for serial i/o etc
const long close_pos = 200;
const long pwr_timeout = 500000; // power save timeout
long pwr_time_start = 0;

void calibrate() {
  int stop1;
  int stop2;
  got1 = false;

  pos = 0; // wherever we start, that's 0

  digitalWrite(dirPin, HIGH);
  stop1 = !digitalRead(stop1Pin);
  stop2 = !digitalRead(stop2Pin);
  while(!stop1 && !stop2) {
    delay(1);
    digitalWrite(led, HIGH);
    digitalWrite(led, LOW);
    pos++;
    stop1 = !digitalRead(stop1Pin);
    stop2 = !digitalRead(stop2Pin);
  }
  if(stop1) { 
    stop1Pos = pos; 
    got1 = true; 
    Serial.print("POS1 ");
    Serial.println(pos);
  }
  if(stop2) { 
    stop2Pos = pos; 
    Serial.print("POS2 ");
    Serial.println(pos);
  }

  digitalWrite(dirPin, LOW);
  delay(100);

  while((!stop1 || got1) && (!stop2 || !got1)) {
    delay(1);
    digitalWrite(led, HIGH);
    digitalWrite(led, LOW);
    pos--;
    //Serial.println(pos);
    stop1 = !digitalRead(stop1Pin);
    stop2 = !digitalRead(stop2Pin);
  }
  if(got1) {
    stop2Pos = pos;
    Serial.print("POS2 ");
    Serial.println(pos);
  } else {
    stop1Pos = pos;
    Serial.print("POS1 ");
    Serial.println(pos);
  }

}

void setup() {
  pinMode(led, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stop1Pin, INPUT);
  pinMode(stop2Pin, INPUT);
  pinMode(PwrPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(PwrPin, HIGH);
  digitalWrite(dirPin, HIGH);
  digitalWrite(led, LOW);
  digitalWrite(enPin, HIGH); // active low
  Serial.begin(9600);
  // wait for signal to begin
  while(!Serial.available()) ;
  Serial.println("Let's go!");
  digitalWrite(enPin, LOW); // active low
  calibrate();
}

void loop() {
  unsigned long current = micros();

  unsigned long interval_ctrl = (current - previous_ctrl);
  // run control i/o
  if(interval_ctrl > usec_per_ctrl) {
    previous_ctrl = current;
    int potpos = analogRead(potPin);
    //double goalv = ((potpos - 512)/512.0)*maxv;
    goalp = (potpos/1024.0)*(stop2Pos-stop1Pos) + stop1Pos;

    //Serial.print(goalp);
    //Serial.print("     ");
    //Serial.print(pos);
    //Serial.print("     ");
    //Serial.print(goal_ups);
    //Serial.print("     ");*/
    //Serial.println(usec_per_step);
    //Serial.print("     ");
    //Serial.println("");
  }

  //Serial.println(usec_per_step);

  unsigned long interval_step = (current - previous_step);
  // drive at current velocity
  if(usec_per_step != 0) { // 0 means stop!
    if (interval_step > abs(usec_per_step)) {
      previous_step = current;
      //usec_per_step = (usec_per_step>0?1:-1)*interval_step;
      /*if(interval_step > max_ups)
       usec_per_step = (usec_per_step>0?1:-1)*max_ups;
       else
       usec_per_step = (usec_per_step>0?1:-1)*interval_step;*/
      digitalWrite(led, HIGH);
      digitalWrite(led, LOW);
      if(dirState == HIGH) pos++;
      else pos--;
    }
  }

  //Serial.println(usec_per_step);

  unsigned long interval_accel = (current - previous_accel);
  // update velocity according to max acceleration
  if (interval_accel > usec_per_ups){
    previous_accel = current;
    
    // set goal velocity
    // head toward goal position until close enough
    long dist = pos-goalp;
    if(abs(dist)>close_pos) {
      if(dist < 0) goal_ups = min_ups;
      else if(dist > 0) goal_ups = -min_ups;
    }
    else goal_ups = 0;
    
    // control velocity ramp based on goal velocity
    if (goal_ups == 0) {
      // going toward stop, go to maximum ups (will be set to stop below)
      if(usec_per_step>0) usec_per_step++;
      if(usec_per_step<0) usec_per_step--;
    } 
    else if ( usec_per_step == 0) {
      // starting from stop, set maximum
      if(goal_ups > 0) usec_per_step = max_ups;
      if(goal_ups < 0) usec_per_step = -max_ups;
    } 
    else if (goal_ups < 0 && usec_per_step < 0 ||
      goal_ups > 0 && usec_per_step > 0 ) {
      // current and goal on same side, simple
      if(goal_ups > usec_per_step) usec_per_step++;
      if(goal_ups < usec_per_step) usec_per_step--;
    } 
    else {
      // current and goal on opposite side, bass-ackwards
      if(goal_ups > usec_per_step) usec_per_step--;
      if(goal_ups < usec_per_step) usec_per_step++;
      // when hit maximum, switch to other side
      if(usec_per_step > max_ups) usec_per_step = -max_ups;
      if(usec_per_step < -max_ups) usec_per_step = max_ups;
    }

    if(abs(usec_per_step) > max_ups) usec_per_step = 0; // stop!
    if(abs(usec_per_step) < min_ups && usec_per_step != 0) usec_per_step = min_ups; // ceiling

    if(usec_per_step < 0) dirState = LOW;
    else dirState = HIGH;

    digitalWrite(dirPin, dirState);
  }
  
  // emergency stop!
  if(!digitalRead(stop1Pin)) {
    long slip = pos-stop1Pos;
    if(got1 && slip < 0 || !got1 && slip > 0) {
      Serial.print("Hit STOP1, slip=");
      Serial.println(slip);
      // correct slip
      pos -= slip;
    }
    
    // disallow movement in bad direction
    if(got1 && usec_per_step > 0 || !got1 && usec_per_step < 0) {
      usec_per_step = 0;
    }
  }
  if(!digitalRead(stop2Pin)) {
    long slip = pos-stop2Pos;
    if(got1 && slip > 0 || !got1 && slip < 0) {
      Serial.print("Hit STOP2, slip=");
      Serial.println(slip);
      // correct slip
      pos -= slip;
    }
    
    // disallow movement in bad direction
    if(got1 && usec_per_step < 0 || !got1 && usec_per_step > 0) {
      usec_per_step = 0;
    }
  }
  
  if(POWER_SAVE_BS) {
    if(usec_per_step == 0) {
      if(current-pwr_time_start > pwr_timeout) digitalWrite(enPin, HIGH); // active low
    } else {
      pwr_time_start = current;
      digitalWrite(enPin, LOW); // active low
    }
  }

}







