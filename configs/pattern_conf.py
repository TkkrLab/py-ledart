#import all patterns availble for use.
from patterns.Patterns import *

led_ceiling_matrix_ip = "10.42.4.6"

TARGETS = {
	#led_ceiling_matrix_ip:RainPattern(chance=0.2)
	#led_ceiling_matrix_ip:PolicePattern()
	#led_ceiling_matrix_ip:GraphicsCircleTest()
	#led_ceiling_matrix_ip:GraphicsRectTest()
	#led_ceiling_matrix_ip:GraphicsLineTest()
	led_ceiling_matrix_ip:GraphicsPixelTest()
}
