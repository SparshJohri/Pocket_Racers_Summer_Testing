import argparse
import time
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
import numpy as np


parser = argparse.ArgumentParser(description="Test ESC and Servo via PCA9685")
parser.add_argument('-e', '--esc', type=int, default=1, help='ESC channel (default: 1)')
parser.add_argument('-s', '--servo', type=int, default=0, help='Servo channel (default: 0)')
parser.add_argument('-i', '--initialize', type=int, default = "", help='Initialize (default: 0)')
args = parser.parse_args()

ESC_CHANNEL = args.esc
SERVO_CHANNEL = args.servo
arm_ESC = args.initialize


# === Constants ===
FREQ = 60  # Standard ESC expects 50–60Hz
NEUTRAL = 1500
MAX = 1900
MIN = 1200

# Setup I2C bus and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = FREQ

def pulse_to_duty(pulse_us):
    period_us = 1_000_000 / FREQ  # = 16666.67 µs
    return int((pulse_us / period_us) * 0xFFFF)


try:
    if (arm_ESC == 1):
        print("Arming the ESC...")
        pca.channels[ESC_CHANNEL].duty_cycle = pulse_to_duty(STOP_US)
        time.sleep(2)
        print("ESC armed. Initiating test...")
        time.sleep(0.5)

    angle_range = [i for i in np.linspace(NEUTRAL, MAX, 3, endpoint = False, dtype = int)] + [i for i in np.linspace(MAX, MIN, 4, endpoint = False, dtype = int)] + [i for i in np.linspace(MIN, NEUTRAL, 4, dtype = int)]
    throttle_range = [i for i in np.linspace(NEUTRAL, MAX, 3, endpoint = False, dtype = int)] + [i for i in np.linspace(MAX, NEUTRAL, 3, dtype = int)] 

    print("      ", end = "", flush = True)
    for i in throttle_range:
        print(" ", i, end="", flush = True)
    print()
    for angle_pulse in angle_range:
        print(angle_pulse, end = "")
        for throttle_pulse in throttle_range:
            print("     X", end = "", flush = True)
            pca.channels[ESC_CHANNEL].duty_cycle = pulse_to_duty(throttle_pulse)
            pca.channels[SERVO_CHANNEL].duty_cycle = pulse_to_duty(angle_pulse)
            time.sleep(0.25)
        print()
    print("\n\n\n")


    print("      ", end = "", flush = True)
    for i in angle_range:
        print("", i, end="", flush = True)
    print()
    for throttle_pulse in throttle_range:
        print(throttle_pulse, end = "", flush = True)
        for angle_pulse in angle_range:
            print("    X", end = "", flush = True)
            pca.channels[ESC_CHANNEL].duty_cycle = pulse_to_duty(throttle_pulse)
            pca.channels[SERVO_CHANNEL].duty_cycle = pulse_to_duty(angle_pulse)
            time.sleep(0.25)
        print()
    
    pca.channels[ESC_CHANNEL].duty_cycle = pulse_to_duty(1500)
    pca.channels[SERVO_CHANNEL].duty_cycle = pulse_to_duty(1500)

finally:
    pca.deinit()
    print("PWM signal deactivated.")
