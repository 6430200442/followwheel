import bluetooth
import time

# ชื่อของ Raspberry Pi ที่จะแสดงในโทรศัพท์มือถือ
device_name = "Raspberry_Pi_Cart"

# รอการเชื่อมต่อจากอุปกรณ์ Bluetooth
def advertise_device():
    # สร้าง Bluetooth server socket
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    # ตั้งชื่ออุปกรณ์ Bluetooth
    bluetooth.advertise_service(server_sock, device_name)

    print("รอการเชื่อมต่อจากอุปกรณ์...")

    # รอการเชื่อมต่อ
    client_sock, client_info = server_sock.accept()
    print(f"เชื่อมต่อกับ {client_info}")

    # ส่ง MAC Address กลับไปให้โทรศัพท์
    mac_address = bluetooth.read_local_bdaddr()
    client_sock.send(mac_address[0])

    # รอการปิดการเชื่อมต่อ
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("ข้อมูลจากอุปกรณ์: ", data)

    # ปิดการเชื่อมต่อ
    print("ยกเลิกการจับคู่")
    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    advertise_device()
