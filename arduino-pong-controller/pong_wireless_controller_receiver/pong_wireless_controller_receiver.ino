/*
  pong receiver code
  */
#include <VirtualWire.h>
void setup()
{
  Serial.begin(9600); // Debugging only
  // Initialise the IO and ISR
  vw_set_rx_pin(12);
  vw_set_ptt_inverted(true); // Required for DR3100
  vw_setup(2000); // Bits per sec
  vw_rx_start(); // Start the receiver PLL running
}
void loop()
{
  uint8_t buf[VW_MAX_MESSAGE_LEN];
  uint8_t buflen = VW_MAX_MESSAGE_LEN;
  vw_get_message(buf, &buflen);
  Serial.write(buf[0]);
}


