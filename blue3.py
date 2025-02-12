import subprocess
import bluetooth

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
    try:
        output = subprocess.check_output(f"hcitool rssi {mac_address}", shell=True).decode()
        rssi_value = int(output.split(":")[-1].strip())
        return rssi_value
    except:
        return -100  # ถ้าอ่านค่าไม่ได้ ให้ใช้ค่าต่ำสุด

def pair_device(mac_address):
    """ จับคู่กับอุปกรณ์ Bluetooth ที่มี MAC Address """
    try:
        print(f"📶 กำลังจับคู่กับอุปกรณ์ {mac_address}...")
        
        # ใช้คำสั่ง bluetoothctl ผ่าน subprocess
        subprocess.run(["bluetoothctl", "power", "on"], check=True)  # เปิด Bluetooth
        subprocess.run(["bluetoothctl", "agent", "on"], check=True)  # เปิด agent สำหรับจับคู่
        subprocess.run(["bluetoothctl", "default-agent"], check=True)  # ตั้งค่า agent เป็น default
        
        # คำสั่งจับคู่กับอุปกรณ์
        subprocess.run(["bluetoothctl", "pair", mac_address], check=True)
        subprocess.run(["bluetoothctl", "connect", mac_address], check=True)
        
        print(f"✅ จับคู่กับอุปกรณ์ {mac_address} สำเร็จ")
    except subprocess.CalledProcessError as e:
        print(f"❌ ไม่สามารถจับคู่กับอุปกรณ์ {mac_address}: {e}")

def main():
    best_device = scan_nearby_devices()
    if best_device:
        pair_device(best_device)
    else:
        print("❌ ไม่มีอุปกรณ์ที่อยู่ใกล้เคียงสำหรับการจับคู่")

if __name__ == "__main__":
    main()
