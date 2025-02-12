import qrcode

data = "https://yourserver.com/pairing?device=cart123"  # URL สำหรับจับคู่
qr = qrcode.make(data)
qr.save("cart_qr.png")  # บันทึกเป็นไฟล์
