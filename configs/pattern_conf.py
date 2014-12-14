#import all patterns availble for use.
from patterns.Patterns import *

led_ceiling_matrix_ip = "pixelmatrix"
michiel_laptop = "10.42.4.12"
local_host = "127.0.0.1"

TARGETS = {
	#led_ceiling_matrix_ip:OldTron(),
	#led_ceiling_matrix_ip:Tron(),
	local_host:MatrixLife(),
	led_ceiling_matrix_ip:MatrixLife(),	
	#led_ceiling_matrix_ip:GraphicsCircleTest(),
	#led_ceiling_matrix_ip:GraphicsCircleTest(),
	#led_ceiling_matrix_ip:GraphicsRectTest(),
	#led_ceiling_matrix_ip:GraphicsLineTest(),
	#led_ceiling_matrix_ip:GraphicsPixelTest(),
}
