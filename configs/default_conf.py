#import barberpole
from patterns.Patterns import BarberpolePattern

led_ceiling_matrix_ip = "10.42.4.12"

TARGETS = {
	led_ceiling_matrix_ip:BarberpolePattern()
	#led_ceiling_matrix_ip:PolicePattern()
	#led_ceiling_matrix_ip:ColorFadePattern()
	#led_ceiling_matrix_ip:RainPattern(chance=0.2)
}
