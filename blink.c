#include <wiringPi.h>

void blink(int hacked){
  int red =  29;
  int green = 28;
  wiringPiSetup();
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);

  	if(hacked == 1){
		digitalWrite(green, HIGH);
		delay(3000);
		digitalWrite(green, LOW);
		delay(3000);
  	}
	else{
		digitalWrite(red, HIGH);
		delay(3000);
		digitalWrite(red, LOW);
		delay(3000);
	}
}

