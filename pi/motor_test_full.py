import argparse
import time
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685



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
NEUTRAL_US = 1000  # ESC arming pulse (1.5 ms)
FORWARD_US = 2000  # Full throttle (2.0 ms)
STOP_US = 1500     # Back to neutral

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
    for angle_pulse in range(1500, 900, -50):
        '''
	for throttle_pulse in range(1000, 2100, 125):
            print(f"Setting servo to {angle_pulse} µs and ESC to {throttle_pulse} µs...")
            pca.channels[SERVO_CHANNEL].duty_cycle = pulse_to_duty(angle_pulse)
            pca.channels[ESC_CHANNEL].duty_cycle = pulse_to_duty(throttle_pulse)
            time.sleep(0.5)

        for throttle_pulse in range(2000, 1600, 100):
            print(f"Setting servo to {angle_pulse} µs and ESC to {throttle_pulse} µs...")
            pca.channels[SERVO_CHANNEL].duty_cycle = pulse_to_duty(angle_pulse)
            pca.channels[ESC_CHANNEL].duty_cycle = pulse_to_duty(throttle_pulse)
            time.sleep(0.5)
	'''
    	pca_channels[SERVO_CHANNEL].duty_cycle = pulse_to_duty(angle_pulse)
    	print('PWM Pulse: {}'.format(angle_pulse))

    print("All tests done. Going back to neutral...")
    pca.channels[ESC_CHANNEL].duty_cycle = pulse_to_duty(STOP_US)
    pca.channels[SERVO_CHANNEL].duty_cycle = pulse_to_duty(STOP_US)


finally:
    pca.deinit()
    print("PWM signal deactivated.")
