/*
	author: Duality

	Controller software for wireless pong controllers.
	transmitter code. more "pipes" needed if adding more controllers to the
	network.
	only 6 allowed by RF24 software.
*/

#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "printf.h"

RF24 radio(7,8);

const uint64_t cntrl1 [2] = {0xABCDABCD71LL, 0x544d52687CLL};
const uint64_t cntrl2 [2] = {0xABCDABCD72LL, 0x544d52687DLL};

byte value;

void setup(void)
{
	Serial.begin(115200);
	printf_begin();

	radio.begin();
	radio.setAutoAck(1);
	radio.setRetries(0,15);
	radio.setPayloadSize(1);

	//open our connection as controller1/2
	//setup for transmitting.
	radio.openWritingPipe(cntrl2[0]);
	radio.openReadingPipe(1, cntrl2[1]);

	radio.stopListening();
	radio.printDetails();

	//setup potmeter pins. A0 = VCC
	//A2 = Input pin.
	pinMode(A2, INPUT);
	pinMode(A0, OUTPUT);
	digitalWrite(A0, LOW);
}

void loop(void)
{
	//read the potmeter and map value to 0-255
	value = (byte)(map(analogRead(A2), 0,1023, 0,255));
	//wait for out value to be transmitted.
	while(!radio.write(&value, 1));
}