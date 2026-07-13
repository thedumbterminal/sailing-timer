from gpiozero import LED
from time import sleep

pin = LED(20)
print("on")
pin.on()
sleep(5)
print("off")
pin.off()
