from mpu6050 import mpu6050
from pythonosc import udp_client
import time

# send all messages to port 1234 on the local machine
client = udp_client.SimpleUDPClient("127.0.0.1", 1234)

# Create the sensor object using the hex address we confirmed earlier
sensor = mpu6050(0x68)


def norm_acc(v):
    return abs(v) / 9.80665


try:
    while True:
        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        temp = sensor.get_temp()

        harm = norm_acc(accel_data["x"])
        modi = norm_acc(accel_data["y"])
        cutoff = norm_acc(accel_data["z"])

        client.send_message("/rnbo/inst/0/params/harmonicity/normalized", harm)
        client.send_message("/rnbo/inst/0/params/mod_index/normalized", modi)
        client.send_message("/rnbo/inst/0/params/cutoff/normalized", cutoff)

        print("Accelerometer data ---")
        print(
            f"x: {accel_data['x']:.4f} y: {accel_data['y']:.4f} z: {accel_data['z']:.4f}")
        print(f"x: {harm:.4f} y: {modi:.4f} z: {cutoff:.4f} (normalized)")
        print("\nGyroscope data ---")
        print(
            f"x: {gyro_data['x']:.4f} y: {gyro_data['y']:.4f} z: {gyro_data['z']:.4f}")
        print(f"\nTemp: {temp:.3f} Celcius")
        time.sleep(0.1)
        print("\033c", end="")  # wipe screen
except KeyboardInterrupt:
    print("Exiting...")
