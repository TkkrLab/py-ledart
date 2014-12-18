// transmitter.pde
//
// Simple example of how to use VirtualWire to transmit messages
// Implements a simplex (one-way) transmitter with an TX-C1 module
//
// See VirtualWire.h for detailed API docs
// Author: Mike McCauley (mikem@airspayce.com)
// Copyright (C) 2008 Mike McCauley
// $Id: transmitter.pde,v 1.3 2009/03/30 00:07:24 mikem Exp $
#include <VirtualWire.h>

//#define DEBUG

char msg[2] = {0,0};

void setup()
{
  #ifdef DEBUG
    Serial.begin(9600);
  #endif
  // Initialise the IO and ISR
  vw_set_tx_pin(12);
  pinMode(12, OUTPUT);
  vw_set_ptt_inverted(true); // Required for DR3100
  vw_setup(2000); // Bits per sec
  
  pinMode(A0, OUTPUT);
  digitalWrite(A0, HIGH);
  
  pinMode(A4, OUTPUT);
  digitalWrite(A4, LOW);
  
  pinMode(A2, INPUT);
  
}
void loop()
{
  #ifdef DEBUG
    Serial.println(analogRead(A2), DEC);
    Serial.println(*msg, DEC);
  #endif
  
  msg[0] = map(analogRead(A2), 0, 1023, 0, 10)&0xFF;
  vw_send((uint8_t *)msg, 1);
  vw_wait_tx(); // Wait until the whole message is gone
}


