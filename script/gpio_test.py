from gpiozero import LED
from time import sleep

print('Running GPIO test...')

num = 17

pin = LED(num)

while True:
    print('On..')
    pin.on()
    sleep(5)
    print('Off..')
    pin.off()
    sleep(5)
