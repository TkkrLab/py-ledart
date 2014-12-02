py-art-net
==========

Python art net interface. with patterns you can run for the ledpoles and the ledmatrix fridgefire made.


I made it easier to config and run patters with python code.


#### what to do if you want to run it ?

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

Then to run the actual patterns you run from the command line:

```shell
	:$ python runPatternJob.py -d <delay> -c <config>
```

for example:

```shell
	:$ python runpatternJob.py -d 0.2 -c myLamps_conf.py
```

both delay and config are optional,
the default delay is 15ms which is the delay that dictates how fast the refresh is ran.

and the default config is default_conf.py
which won't work if you didn't put the right things in it. like the right ip.

etc etc.


#### usefull tools in art-net_C are:

artmonitor <ip>		#tells a bit more info on the device like mac address and more.

artpoll <broadcast> 	#finds all the devices on the network. writes that data to a file. make sure field-devices exist (file)

artdmxtest <ip>		#runs a fading pattern, usefull for testing if the art-net device works.



#### on the todo list:

break out patterns in patterns.py in to seperate files.

fridgefire's matrix might be fun to make a pong implementation on.

or a snake might be fun to implement for it.

I think it would be helpfull to implement a "Graphics" library

everything with multiplayer or not ?

another thing that might be fun to make is a vu meter?

and yet another thing might be a network traffic monitor of kind.

#### other things that might be verry usefull to make or do:

more a hardware todo is make firmware for the ESP8266 wifi module

that does art net. no need for utp cables any more.




