# test1 ultrasonic

from gpiozero import DistanceSensor

# กำหนดขา GPIO สำหรับ Echo และ Trigger สำหรับแต่ละเซ็นเซอร์
ultrasonic1 = DistanceSensor(echo=18, trigger=23, threshold_distance=0.5, max_distance=2)
ultrasonic2 = DistanceSensor(echo=17, trigger=24, threshold_distance=0.5, max_distance=2)
ultrasonic3 = DistanceSensor(echo=16, trigger=25, threshold_distance=0.5, max_distance=2)

# ฟังก์ชันที่จะทำงานเมื่อเซ็นเซอร์ตรวจจับระยะ
def hello(sensor_num):
    print(f"Hello from Sensor {sensor_num}")

def bye(sensor_num):
    print(f"Bye from Sensor {sensor_num}")

# กำหนดการกระทำเมื่อเซ็นเซอร์อยู่ในหรือออกจากระยะ
ultrasonic1.when_in_range = lambda: hello(1)
ultrasonic1.when_out_of_range = lambda: bye(1)

ultrasonic2.when_in_range = lambda: hello(2)
ultrasonic2.when_out_of_range = lambda: bye(2)

ultrasonic3.when_in_range = lambda: hello(3)
ultrasonic3.when_out_of_range = lambda: bye(3)

# ลูปหลักที่จะรันตลอดเวลา
while True:
    # รอให้วัตถุเข้าหรือออกจากระยะสำหรับแต่ละเซ็นเซอร์
    ultrasonic1.wait_for_in_range()
    # print("Sensor 1 In range")
    ultrasonic1.wait_for_out_of_range()
    # print("Sensor 1 Out of range")

    ultrasonic2.wait_for_in_range()
    # print("Sensor 2 In range")
    ultrasonic2.wait_for_out_of_range()
    # print("Sensor 2 Out of range")

    ultrasonic3.wait_for_in_range()
    # print("Sensor 3 In range")
    ultrasonic3.wait_for_out_of_range()
    # print("Sensor 3 Out of range")
