import bluetooth
import time
import subprocess

owner_mac = None  # เก็บ MAC Address ของเจ้าของปัจจุบัน
owner_timeout = 10  # วินาทีที่ Raspberry Pi จะรอ ก่อนปลดเจ้าของ

def scan_nearby_devices():
    """ สแกนอุปกรณ์ Bluetooth ที่อยู่ใกล้เคียง """
    print("🔍 กำลังสแกนอุปกรณ์ Bluetooth...")
    devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
    
    if not devices:
        print("❌ ไม่พบอุปกรณ์ใกล้เคียง")
        return None

    best_device = None
    best_rssi = -100  # ค่าเริ่มต้นของ RSSI (สัญญาณอ่อนมาก)

    for addr, name in devices:
        print(f"พบอุปกรณ์: {name} [{addr}]")
        rssi = get_rssi(addr)  # อ่านค่า RSSI
        if rssi > best_rssi:
            best_rssi = rssi
            best_device = addr

    return best_device

def get_rssi(mac_address):
    """ ดึงค่า RSSI ของอุปกรณ์ (ต้องใช้ `hcitool` และ `hcidump`) """
    import subprocess
    try:
        output = subprocess.check_output(f"hcitool rssi {mac_address}", shell=True).decode()
        rssi_value = int(output.split(":")[-1].strip())
        return rssi_value
    except:
        return -100  # ถ้าอ่านค่าไม่ได้ ให้ใช้ค่าต่ำสุด

def is_device_connected(mac_address):
    """ ตรวจสอบว่า Bluetooth Device ที่มี MAC Address นี้ยังเชื่อมต่ออยู่หรือไม่ """
    try:
        # ใช้ `hcitool` เพื่อตรวจสอบว่าอุปกรณ์ที่มี MAC Address นี้ยังเชื่อมต่อหรือไม่
        output = subprocess.check_output(f"hcitool con", shell=True).decode()
        if mac_address in output:
            return True
        return False
    except subprocess.CalledProcessError:
        return False

def main():
    global owner_mac
    while True:
        if owner_mac:
            # ตรวจสอบว่าเจ้าของยังเชื่อมต่ออยู่หรือไม่
            if not is_device_connected(owner_mac):
                print(f"🚫 เจ้าของ {owner_mac} ถูกปลดออกเนื่องจาก Bluetooth ถูกปิดหรือกดลืมการจับคู่")
                owner_mac = None  # ปลดเจ้าของ
            else:
                print(f"🔄 เจ้าของ {owner_mac} ยังเชื่อมต่ออยู่")
        else:
            new_owner = scan_nearby_devices()
            if new_owner:
                owner_mac = new_owner
                print(f"✅ เจ้าของใหม่: {owner_mac}")
        
        time.sleep(owner_timeout)  # รอ 10 วินาทีเพื่อสแกนใหม่

if __name__ == "__main__":
    main()
