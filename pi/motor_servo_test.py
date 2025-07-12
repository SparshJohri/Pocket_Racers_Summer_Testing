import time
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

# PWM frequency for ESC
FREQ = 60

# Setup I2C bus and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = FREQ

# Use CH1 for throttle (ESC)
channel = 8

# Convert microseconds to 16-bit duty cycle
def pulse_us_to_duty(pulse_us):
    period_us = 1_000_000 / FREQ  # = 16666.67 µs
    return int((pulse_us / period_us) * 0xFFFF)

# Neutral throttle (ESC arming)
neutral = pulse_us_to_duty(1500)
full_forward = pulse_us_to_duty(2000)

try:
    print("Arming ESC at neutral (1500 µs)...")
    pca.channels[channel].duty_cycle = neutral
    time.sleep(3)

    print("Sending full throttle (2000 µs)...")
    pca.channels[channel].duty_cycle = full_forward
    time.sleep(3)

    print("Stopping (back to neutral)...")
    pca.channels[channel].duty_cycle = neutral
    time.sleep(1)

finally:
    pca.deinit()
    print("PWM signal deactivated.")
