import time
import board
import busio
from adafruit_pca9685 import PCA9685

def us_to_duty(us, freq=60):
    period_us = 1_000_000 / freq
    return int((us / period_us) * 0xFFFF)

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)

# ✅ SET FREQUENCY or PWM won't be sent
pca.frequency = 60

# Set CH1 (ESC) to neutral 1500us
duty = us_to_duty(1500)
pca.channels[1].duty_cycle = duty

print("PWM signal sent to CH1: 1500us")
time.sleep(5)

pca.deinit()
