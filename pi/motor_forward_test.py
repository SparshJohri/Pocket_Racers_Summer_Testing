import time
import board
import busio
from adafruit_pca9685 import PCA9685

# === Constants ===
ESC_CHANNEL = 3
PWM_FREQ_HZ = 60  # Standard ESC expects 50–60Hz
NEUTRAL_US = 1000  # ESC arming pulse (1.5 ms)
FORWARD_US = 2000  # Full throttle (2.0 ms)
STOP_US = 1500     # Back to neutral

# === Utility: Convert pulse width in µs to 16-bit duty cycle ===
def us_to_duty_cycle(pulse_us, freq_hz=PWM_FREQ_HZ):
    period_us = 1_000_000 / freq_hz
    return int((pulse_us / period_us) * 0xFFFF)

# === Setup I2C and PCA9685 ===
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = PWM_FREQ_HZ

try:
	print("Step 1: Arming ESC at neutral (1500 µs)...")
	pca.channels[ESC_CHANNEL].duty_cycle = us_to_duty_cycle(NEUTRAL_US)
	time.sleep(3)  # Give ESC time to arm

	for i in range(1500, 2000, 100):
		print("Step 2: Full forward throttle ({} µs)...".format(i))
		pca.channels[ESC_CHANNEL].duty_cycle = us_to_duty_cycle(i)
		time.sleep(1.5)

	for i in range(2000, 1500, -100):
		print("Step 3: Full forward throttle ({} us)...".format(i))
		pca.channels[ESC_CHANNEL].duty_cycle = us_to_duty_cycle(i)
		time.sleep(1.5)

	print("Step 4: Back to neutral...")
	pca.channels[ESC_CHANNEL].duty_cycle = us_to_duty_cycle(STOP_US)
	time.sleep(2)
	print("✅ Motor test complete.")

finally:
    print("Deinitializing PCA9685...")
    pca.deinit()
