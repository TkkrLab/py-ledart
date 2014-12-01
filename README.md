py-art-net
==========

Python art net interface. with patterns you can run for the ledpoles and the ledmatrix fridgefire made.


I made it easier to config and run patters with python code.


what to do if you want to run it ?
make you pattern, import it into patterns.py
then in configs folder created a config file or edit a existing one.
create it like:
name_conf.py

use a existing config as a template and follow it.
you can run multiple devices from a signle config file.
as wel as multpile patterns like:


```python
TARGETS {
	target1_ip:pattern()
	target2_ip:nextPattern()
	target3_ip:anotherPattern()
}
```

etc etc.

usefull tools in art-net_C are:
artmonitor <ip>		#tells a bit more info on the device like mac address and more.
artpoll <broadcast> 	#finds all the devices on the network. writes that data to a file. make sure field-devices exist (file)
artdmxtest <ip>		#runs a fading pattern, usefull for testing if the art-net device works.

on the todo list:

break out patterns in patterns.py in to seperate files.

might be fun to make a pong implementation.
i think it would be helpfull to implement a "Graphics" library
snake might be fun to implement.

everything with multiplayer ?

other things on the todo:
more a hardware todo is make firmware for the ESP8266 wifi module
that does art net. no need for utp cables any more.
