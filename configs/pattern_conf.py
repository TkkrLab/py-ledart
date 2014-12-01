#import all patterns availble for use.
from patterns.Patterns import *

led_ceiling_matrix_ip = "10.42.255.255"

TARGETS = {
	led_ceiling_matrix_ip:RainPattern(chance=0.2)
	#led_ceiling_matrix_ip:PolicePattern()
}
