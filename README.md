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
	:$ python runPatternJob.py --delay=<delay> --config=<config>
```

for example:

```shell
	:$ python runpatternJob.py --delay=0.2 --config=myLamps_conf.py
```

both delay and config are optional,

the default delay is 15ms which is the delay that dictates how fast the refresh is ran.

and the default config is default_conf.py

which won't work if you didn't put the right things in it. like the right ip.

etc etc.

if you want to run the code with the build in simulator just add --matrixSim=enabled

to the command line options and it will run localy on your screen.

for exampe:
```shell
	:$ python runpatternJob.py --delay=0.2 --config=myLamps_conf.py --matrixSim=enabled
```


but ofcourse this would look right if you config file contains code for anything other than a matrix display.

but you can view the display as a string of pixels though, cause basicly in reality it is just that.


#### usefull tools in art-net_C are:

artmonitor <ip>		#tells a bit more info on the device like mac address and more.

artpoll <broadcast> 	#finds all the devices on the network. writes that data to a file. make sure field-devices exist (file)

artdmxtest <ip>		#runs a fading pattern, usefull for testing if the art-net device works.



#### on the todo list:

*FallingStars [it is broken it worked it was done and now it doesn't even run. only half the code is there. probably a commit thing happend.]

*pong [Done]

*snake [Done]

*tron <W.I.P>

*tetris 

*arcadia

*game of life (conway) [Done it's called PixelLife]

*VU meter

*network monitor 

*make mario appear on the matrix or other mobs from the game or any other image from other games.

*problem with pwm not being linear (the amount of power it gives per pulse)

*thus implement a scale which does make it linear. so fading is nice and even.

*link that gave me the Yes that's it! moment:

*http://forum.arduino.cc/index.php?PHPSESSID=fiq8nr1j9sstegstf2o6btdgq2&topic=286351.0

break out patterns in patterns.py in to seperate files.

I think it would be helpfull to implement a "Graphics" library [This is done the class is called Graphics]

also implemented a color library, and classes for making color objects. handy for pallets and much more.

everything with multiplayer or not ? [probably not]

another thing that might be fun to make is a vu meter?

and yet another thing might be a network traffic monitor of kind.

#### other things that might be verry usefull to make or do:

more a hardware todo is make firmware for the ESP8266 wifi module

that does art net. no need for utp cables any more.




