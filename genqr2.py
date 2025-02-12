import qrcode

data = "http://192.168.137.135/register"  # URL ของเซิร์ฟเวอร์บน Raspberry Pi
qr = qrcode.make(data)
qr.save("qrcode.png")
