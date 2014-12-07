#import all patterns availble for use.
from patterns.Patterns import *

led_ceiling_matrix_ip = "10.42.4.5"
local_host = "127.0.0.1"

TARGETS = {
	#led_ceiling_matrix_ip:RainPattern(chance=0.2),
	local_host:GraphicsPixelTest(),
	#led_ceiling_matrix_ip:PolicePattern(),
	#led_ceiling_matrix_ip:GraphicsCircleTest(),
	#local_host:GraphicsCircleTest(),
	#led_ceiling_matrix_ip:GraphicsRectTest(),
	#led_ceiling_matrix_ip:GraphicsLineTest(),
	#led_ceiling_matrix_ip:GraphicsPixelTest(),
}
