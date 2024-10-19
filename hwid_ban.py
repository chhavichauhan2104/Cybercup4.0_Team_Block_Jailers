import wmi
import hashlib


def get_hwid():
    # Create WMI object to query system information
    c = wmi.WMI()
    
    # Get the serial number of the motherboard
    motherboard_serial = ""
    for board in c.Win32_BaseBoard():
        motherboard_serial = board.SerialNumber
        break  # Only consider the first entry
    
    # Get the serial number of the primary hard drive
    hard_drive_serial = ""
    for disk in c.Win32_DiskDrive():
        hard_drive_serial = disk.SerialNumber
        break  # Only consider the first entry
    
    # Get the serial number of the BIOS
    bios_serial = ""
    for bios in c.Win32_BIOS():
        bios_serial = bios.SerialNumber
        break  # Only consider the first entry

    # Get the serial number of CPU of the device
    processor_serial = ""
    for processor in c.Win32_Processor():
        processor_serial = processor.ProcessorId
        break  # Only consider the first entry

    # Get the MAC address of the primary network adapter
    mac_serial = ""
    for mac in c.Win32_NetworkAdapterConfiguration():
        if mac.MACAddress is not None:
            mac_serial = mac.MACAddress
            break  # Only consider the first entry with a MAC address

    # Combine them to create a unique HWID
    hwid = motherboard_serial + hard_drive_serial + bios_serial + processor_serial + mac_serial
    return hwid

def hash_hwid(hwid):
    return hashlib.sha256(hwid.encode()).hexdigest()

def is_banned(hwid):
    hashed_hwid = hash_hwid(hwid)
    return hashed_hwid in banned_hwids

# Predefined list of banned HWIDs (for testing, can later be stored in a database)
banned_hwids = [
    "8aef14195b8ae56620caeaf83df34b532253709851997fbabd3454676092f238", 
    "MP27RYCQ0025_38D3_21D1_FE29.MP27RYCQBFEBFBFF000806C2C4:75:AB:3B:13:DE"
]

if __name__ == "__main__":
    hwid = get_hwid()
    print(f"HWID: {hwid}")
    hashed_hwid = hash_hwid(hwid)
    print(f"Hashed HWID: {hashed_hwid}")

    if is_banned(hwid):
        print("Access Denied: Your HWID is banned.")
    else:
        print("Access Granted.")
