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

byte values[2];
byte prot_values[2] = {0,0};
byte pipno, gotbyte;

void setup(void)
{
    Serial.begin(115200);
    printf_begin();

    radio.begin();
    radio.setAutoAck(1);
    radio.setRetries(0,15);
    radio.setPayloadSize(1);

    //open our connection as controller1/2
    //setup for reading.
    radio.openWritingPipe(cntrl1[1]);
    radio.openReadingPipe(1, cntrl1[0]);

    radio.openWritingPipe(cntrl2[1]);
    radio.openReadingPipe(2, cntrl2[0]);

    radio.startListening();
    //radio.printDetails();
}

int interval = 10;
unsigned long previous = 0;
unsigned long current = 0;

void loop(void)
{
    //listen for first controller.
    radio.openReadingPipe(1, cntrl1[0]);
    if(radio.available(&pipno))
    {
        while(radio.available(&pipno))
        {
            radio.read(values, 1);
        }
        if(pipno == 1)
        {   
            prot_values[0] = values[0];
        }
    }
    
    //listen for second controller
    radio.openReadingPipe(2, cntrl2[0]);
    if(radio.available(&pipno))
    {
        while(radio.available(&pipno))
        {
            radio.read((values+1), 1);
        }
        if(pipno == 2)
        {   
            prot_values[1] = values[1];
        }
    }
    if(Serial.available() > 0)
    {
        byte inbyte = Serial.read();
        if(inbyte == 'n')
        {
            Serial.write(prot_values[0]);
            Serial.write(prot_values[1]);
        }
    }
    //Serial.write(prot_values[0]);
    //Serial.write(prot_values[1]);
}