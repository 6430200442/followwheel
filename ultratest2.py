# test2 ultrasonic

import RPi.GPIO as GPIO
import time

# ตั้งค่า GPIO สำหรับแต่ละเซ็นเซอร์
SENSORS = [
    {"TRIG": 23, "ECHO": 18},  # เซ็นเซอร์ตัวที่ 1
    {"TRIG": 24, "ECHO": 17},  # เซ็นเซอร์ตัวที่ 2
    {"TRIG": 25, "ECHO": 16}   # เซ็นเซอร์ตัวที่ 3
]

# ตั้งค่า GPIO Mode
GPIO.setmode(GPIO.BCM)

# ตั้งค่าขา GPIO สำหรับทุกเซ็นเซอร์
for sensor in SENSORS:
    GPIO.setup(sensor["TRIG"], GPIO.OUT)
    GPIO.setup(sensor["ECHO"], GPIO.IN)

# ฟังก์ชันวัดระยะทางของแต่ละเซ็นเซอร์
def measure_distance(TRIG, ECHO):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 ไมโครวินาที
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # คำนวณระยะทาง (cm)
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2

    return distance

try:
    while True:
        for i, sensor in enumerate(SENSORS):
            dist = measure_distance(sensor["TRIG"], sensor["ECHO"])
            print(f"Sensor {i+1}: {dist:.2f} cm")
        print("-" * 30)
        time.sleep(1)  # อ่านค่าทุก 1 วินาที

except KeyboardInterrupt:
    print("Stopping...")
    GPIO.cleanup()
