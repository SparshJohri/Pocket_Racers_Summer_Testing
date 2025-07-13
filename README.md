The local folder contains 3 main files

1) The IP address of the Raspberry Pi (this needs to be updated if the car changes locations).
2) An ssh script so that people don't have to memorize the IP address of their car (./ssh_to_pi.sh USERNAME ip_addr)
3) A script to pull photos from a directory on the pi to a directory on the local machine (./pull_recent_photos.sh PI_USER ip_addr remote/directory local/directory)

Note: For the remote directory, do NOT use ~; instead, to go to the home directory, you should use /home/PI_USER


The pi folder also contains 3 main files; they should be used in the following way:
1) python3 motor_forward_test.py --esc ESC_CHANNEL_ON_PCA_BOARD
2) python3 motor_servo_test.py --servo SERVO_CHANNEL_ON_PCA_BOARD
3) python3 motor_test_full.py --esc ESC_CHANNEL_ON_PCA_BOARD --servo SERVO_CHANNEL_ON_PCA_BOARD

Hopefully, it is self-explanatory what these scripts do.




If you want to take pictures, first type the following command into the pi: libcamera-jpeg -o example_image.jpg.
Then, on the local machine, call the pull_recent_photos shell script.
Finally, you can (optionally) delete the image from the raspberry pi so that you don't clutter its memory with unnecessary photos.
