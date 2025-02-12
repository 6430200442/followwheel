from bluetooth import BluetoothSocket, RFCOMM, advertise_service

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

# เปลี่ยนชื่ออุปกรณ์ตามต้องการ
advertise_service(server_sock, "Raspberry_Pi_Cart", service_id=0x1101, service_classes=[0x1101], profiles=[0x1101])

print("รอการเชื่อมต่อ...")
client_sock, client_info = server_sock.accept()
print(f"เชื่อมต่อกับ {client_info}")
